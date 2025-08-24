from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate, login
from index.models import User

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            # 使用 create_user 确保密码哈希
            user = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=form.cleaned_data['password1']
            )
            user.save()
            login(request, user, backend='accounts.backends.EmailBackend')
            return redirect('chat:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)  # 清除用户会话
    return redirect('chat:index')  # 重定向到主页页


# def login_view(request):
#     next_url = request.GET.get('next', 'chat:index')  # 从请求中获取next参数
#
#     if request.method == "POST":
#         print(2)
#         form = LoginForm(request.POST)
#         print(3)
#         print(form)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             user = authenticate(request, username=username, password=password)
#             print(4)
#
#             if user:
#                 if user.is_active:  # 检查用户是否激活
#                     login(request, user)
#                     return redirect(next_url or 'chat:index')
#         else:
#             print(form.errors)
#             print(5)
#     else:
#         print(1)
#         form = LoginForm()
#
#     return render(request, 'registration/login.html', {
#         'form': form,
#         'next_url': next_url,  # 传递给模板
#     })