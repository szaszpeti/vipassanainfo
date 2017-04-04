from django import forms
from django.contrib.auth.models import User
from .models import Post


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password')



class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = [
            "title",
            'image',
            "content",
            'draft',
            'publish'

        ]