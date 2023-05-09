from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, TeamProfile
from .forms import PostForm, CommentForm
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, LoginForm


def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'home.html', {'posts': posts})

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
def delete_post(request, post_id):
    if request.user.is_superuser:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    if request.user.is_superuser:
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['is_team']:
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
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


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
