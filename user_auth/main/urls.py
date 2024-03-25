from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('user-list', views.user_list, name='user_list'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('users/<int:user_id>/posts/', views.user_posts, name='user_posts'),
    path('ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban/<int:user_id>/', views.unban_user, name='unban_user'),
]