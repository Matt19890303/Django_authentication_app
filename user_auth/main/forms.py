from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Post

# creating a user form
# Can add other fields here for user information/credentials
class RegisterForm(UserCreationForm):
    # added an email field for the signup form
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
# To create posts
# So what this does for us is create an instance of this form,pass it to a template and the template displays the form that has the 'title and the 'description'
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']