from django import forms
from . import models

class AddPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','content','status']

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username','password']

class AddCommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput())  # 添加 parent_id 字段
    class Meta:
        model = models.Comment
        fields = ['content']