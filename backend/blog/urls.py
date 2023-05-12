from django.urls import path
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('home', views.home, name='home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('post/<int:post_id>/comment/create/', views.create_comment, name='create_comment'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/', views.profile, name='profile'),
    path('', RedirectView.as_view(url='http://localhost:3000'), name='redirect-landing'),
]
