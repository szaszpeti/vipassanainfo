from django import forms
from django.contrib.auth.models import User
from .models import Post, Document


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

class DocumentForm(forms.ModelForm):
    class Meta():
        model = Document
        fields = [
            "post",
            "title",
            "image",
            "content",
            "draft",
            "publish"

        ]

