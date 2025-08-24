from django.contrib.auth.forms import UserCreationForm
from django import forms
from index.models import User

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    email = forms.EmailField(required=True)  # 显式添加 email 字段
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class SignUpForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已被注册")
        return email

    class Meta:
        model = User  # 使用get_user_model()获取的模型
        fields = ('username', 'email', 'password1', 'password2')

