from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'main/home.html')


def sign_up(request):
    # If its a post request then insert data fromform
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # If form is valid then save user and login
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to home page once signed in
            return redirect('/home')
    else:
        # If its a get request then create a form
        form = RegisterForm()

    return render(request,'registration/sign_up.html', {'form': form})

