from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, TeamProfile, UserProfile
from .forms import PostForm, CommentForm, ProfileImageForm
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, LoginForm


def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    context = {
        'posts': posts,
    }
    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            userprofile = UserProfile.objects.create(user=request.user)
        context['userprofile'] = userprofile
    return render(request, 'home.html', context=context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        post.dislikes.remove(user)

    return redirect('home')

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.dislikes.add(user)
        post.likes.remove(user)

    return redirect('home')


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not post.user_can_modify(request.user):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_superuser or request.user == post.author:
        post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))



@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not comment.user_can_modify(request.user):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.is_superuser or request.user == comment.author:
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['register_as_team']:
                team_name = form.cleaned_data['team_name']
                TeamProfile.objects.create(user=user, team_name=team_name)
            login(request, user)
            return redirect('home')
        else:
            form.add_error(None, "Invalid registration details")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error_message = None
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            error_message = "Invalid username or password"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})




def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    user_comments = Comment.objects.filter(author=user)  # Change this line
    user_liked_posts = user.liked_posts.all()

    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'user_liked_posts': user_liked_posts,
    }
    
    return render(request, 'user_profile.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)

        form = ProfileImageForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'user_profile': profile})


def landing(request):
    return render(request, 'index.html')

