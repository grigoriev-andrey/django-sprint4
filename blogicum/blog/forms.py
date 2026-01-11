from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'image', 'pub_date')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)





