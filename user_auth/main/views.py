from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PostForm
from django.contrib.auth import authenticate, login, logout
# To only allow user access to home page if logged in
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import Post
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from django.contrib import messages

from django.http import HttpResponseRedirect




# @login tells it where to redirect us if we are not logged in
# Home page
@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        # Gets POST ID
        post_id = request.POST.get('post-id')
        # Get User ID
        user_id = request.POST.get('user-id')
        # If its a post_id then run below
        if post_id:
            # Confirm that this user owns this post by filtering by ID and grabbing the first element
            post = Post.objects.filter(id=post_id).first()
            # Check if the post exists
            # If user the permission to delete post, allow it
            if post and (post.author == request.user or request.user.has_perm('main.delete_post')):
                post.delete()

        elif user_id:
            # Confirm that this user owns this post by filtering by ID and grabbing the first element
            user = User.objects.filter(id=user_id).first()
            # Check if the post exists
            # If user the permission to delete post, allow it

            # Bann Users 
            if user and request.user.is_superuser:
                user.is_banned = True
                user.save()
                # Remove from groups to ban users
                # Default group
                try:
                    group = Group.objects.get(name='Default')
                    group.user_set.remove(user)
                except:
                    pass
                # Mod group
                try:
                    group = Group.objects.get(name='Mod')
                    group.user_set.remove(user)
                except:
                    pass
    
    # context = {
    # 'posts': posts,
    # 'messages': messages.get_messages(request) 
    # }
    return render(request, 'main/home.html', {'posts': posts})


# Deleteing Post
def delete_post(request):
  if request.method == 'POST':
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)
    if request.user == post.author or request.user.is_superuser:
      post.delete()
  return redirect('home')



# Ban User
def ban_user(request, user_id):
    # Confirm that this user owns this post by filtering by ID and grabbing the first element
    user = User.objects.filter(id=user_id).first()
    # Check if the post exists
    # If user the permission to delete post, allow it
    # Bann Users 
    if user and request.user.is_superuser:
        user.is_banned = True
        user.save()
        # Remove from groups to ban users
        # Default group
        try:
            group = Group.objects.get(name='Default')
            group.user_set.remove(user)
        except:
            pass
        # Mod group
        try:
            group = Group.objects.get(name='Mod')
            group.user_set.remove(user)
        except:
            pass

    return redirect('user_list')
        

# Unban user
def unban_user(request, user_id):
  user = User.objects.get(id=user_id)
  user.is_banned = False
  user.save()
  
  default_group = Group.objects.get(name='Default') 
  default_group.user_set.add(user)

  return redirect('user_list')



# Posts
@login_required(login_url='/login')
# Restrictor based on permission 
# If no permission it will redirect you to /login page
# Will raise an exception if you dont have permission
@permission_required('main.add_post', login_url='/login', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Need to add a user to the post before submitting - thats why commit = False
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request,'main/create_post.html', {'form': form})


# Signup form
def sign_up(request):
    # If its a post request then insert data fromform
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # If form is valid then save user and login
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to home page once signed in
            return redirect('home')
    else:
        # If its a get request then create a form
        form = RegisterForm()

    return render(request,'registration/sign_up.html', {'form': form})


# All users display for superuser
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
  users = User.objects.all()

  for user in users:
    if user.is_banned:
      user.username += " (Banned)"
    else:
      user.username += " (Active)"

  return render(request, 'main/user_list.html', {'users': users})


# Display all posts for a specified user
def user_posts(request, user_id):
  user = User.objects.get(id=user_id) 
  posts = Post.objects.filter(author=user)
  return render(request, 'main/user_posts.html', {'posts': posts})


# Confirmation message for deleting and confirmation message for deletion success
# @login_required
# def delete_post(request):
#   post = Post.objects.get(id=post_id) 
#   if request.method == 'POST':
#     post_id = request.POST.get('post_id')
#     try:
#         # post = Post.objects.get(id=post_id)
#         post = Post.objects.filter(id=post_id, author=request.user).first() 
#         post.delete()
#     except Post.DoesNotExist:
#         messages.error(request, 'That post does not exist')
#         return redirect('home')
