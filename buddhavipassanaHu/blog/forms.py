from django import forms
from django.contrib.auth.models import User
from .models import Post, Document
from pagedown.widgets import PagedownWidget


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password')



class PostForm(forms.ModelForm):
    # show_preview, pictures wont show up on the create form
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
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
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
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

