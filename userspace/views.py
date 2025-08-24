from django.shortcuts import render
from django.urls import reverse

from index.models import Post,Comment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user = request.user
    user_posts = Post.objects.filter(author=user) #用户自己发布的帖子
    comments = Comment.objects.filter(user=user)  #用户发表的评论
    like_posts = user.like_post.all()

    context = {
        'user': user,
        'user_posts': user_posts,
        'comments': comments,
        'like_posts': like_posts,
    }

    return render(request, 'userspace_index.html', context)

@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        user = request.user
        avatar_file = request.FILES.get('avatar')

        if avatar_file:
            if avatar_file.size > 10 * 1024 * 1024:  # 限制5MB
                return JsonResponse({'success': False, 'message': '文件过大'})
            if not avatar_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                return JsonResponse({'success': False, 'message': '不支持的文件格式'})

            user.avatar.save(
                f'avatars/{user.id}/{avatar_file.name}',
                avatar_file,
                save=False  # 先不保存到数据库
            )
            user.save()  # 触发头像路径生成

        return JsonResponse({'success': True, 'redirect_url': reverse('userspace:index')}) #前端根据redirect_url进行跳转

    return JsonResponse({'success': False, 'message': '无效请求'})

@csrf_exempt
def update_bio(request):
    if request.method == 'POST':
        user = request.user
        bio = request.POST.get('bio')
        user.bio = bio
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': '无效请求'})
