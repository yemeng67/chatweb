from django.http.response import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post,Category,PostLike,Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json
from django.utils import timezone

timestamp = timezone.now().timestamp()


# Create your views here.
def base(request):
    """导航栏"""
    user = request.user
    return render(request,'base.html',{'user':user})


def index(request):
    """初始化加载页面数据"""
    categories = Category.objects.all()

    # 获取默认排序和分类
    default_sort = request.GET.get('sort', 'views')
    selected_category = request.GET.get('category', 0)

    context = {
        'categories': categories,
        'default_sort': default_sort,
        'selected_category': selected_category
    }
    return render(request, 'index.html', context)


def index_data(request):
    """动态加载帖子数据"""
    # 获取排序参数，默认为'views'
    sort_by = request.GET.get('sort', 'views')
    # 获取分类参数，默认为0（全部）
    category_id = request.GET.get('category', 0)
    # 获取页码参数，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集
    post_query = Post.objects.filter(status='published')

    # 分类过滤
    if category_id == '0':
        post_query = post_query

    else:
        post_query = post_query.filter(category__id = category_id)

    # 排序处理
    valid_sort_fields = {'views', 'likes', 'created_at'}

    # 先注解点赞数，确保排序和显示使用相同的计算方式
    post_query = post_query.annotate(
        comment_count=Count('comment'),
        like_count=Count('likes', distinct=True)
    )

    # 排序处理
    if sort_by == 'likes':
        sort_field = '-like_count'
    elif sort_by == 'views':
        sort_field = '-views'
    elif sort_by == 'created_at':
        sort_field = '-created_at'
    else:
        sort_field = '-created_at'

    post_query = post_query.order_by(sort_field)

    # 分页处理
    paginator = Paginator(post_query, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # 构造返回数据
    return JsonResponse({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'content': post.content[:100] + '...',  # 摘要
            'author_name': post.author.username,
            'author_avatar': post.author.avatar.url if post.author.avatar else '',
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
            'views': post.views,
            'likes': post.like_count,  # 使用注解的like_count，确保与排序一致
            'category': [cat.name for cat in post.category.all()]
        } for post in posts],
        'pagination': {
            'current_page': posts.number,
            'total_pages': paginator.num_pages,
            'has_next': posts.has_next(),
            'has_previous': posts.has_previous()
        }
    })


@login_required
def post_detail(request, post_id):
    """帖子详情"""
    post = Post.objects.select_related('author').get(id=post_id)
    post.views += 1       #增加浏览量
    post.save(update_fields=['views'])

    print(post.status)

    # # 获取当前用户的点赞状态
    # is_liked = False
    # if request.user.is_authenticated:
    #     is_liked = PostLike.objects.filter(user=request.user, post=post).exists()

    context = {
        'post': post,
        'like_count': post.likes.count(),
        'categories': post.category.all(),
    }
    return render(request,'post_detail.html',context)

@login_required
def like_post(request, post_id):
    """点赞管理"""

    post = Post.objects.get(id=post_id)

    # 获取原始字节流并解码为字符串
    json_data = request.body.decode('utf-8')

    # 解析为 Python 字典
    data = json.loads(json_data)

    is_init = data.get('is_init')

    if is_init and request.user.is_authenticated:
        is_liked = PostLike.objects.filter(user=request.user, post=post).exists()
        action = 'null'

    elif request.method == 'POST' and request.user.is_authenticated and not is_init:
        post = Post.objects.get(id=post_id)
        like,created = PostLike.objects.get_or_create(user=request.user, post=post)#记录存在就返回False和响应的列表
        if not created:
            like.delete()
            action = 'dislike'
        else:
            action = 'like'

        is_liked = PostLike.objects.filter(user=request.user, post=post).exists()
    else:
        return JsonResponse({'status': 'error'})

    return JsonResponse({'status':'success',
                         'like_count':post.likes.count(),
                         'action':action,
                         'is_liked':is_liked},
                        status=200)

@login_required
def add_post(request):
    """添加帖子"""
    if request.method != "POST":
        # form = AddPostForm()
        context = {'categories': Category.objects.all(),
                   'STATUS_CHOICES': Post.STATUS_CHOICES
                   }
        return render(request,'create_post.html',context)
    else:
        try:
            if not request.POST.get('content'):
                return JsonResponse({'status': 'error', 'message': '内容不能为空'}, status=400)

            if not request.POST.getlist('category'):
                return JsonResponse({'status': 'error', 'message': '分类不能为空'}, status=400)

            content = request.POST.get('content')
            author = request.user
            title = request.POST.get('title')
            status = request.POST.get('status')
            category_id = request.POST.getlist('category')  # 注意category是多个对象，所以用getlist，get只能获取到一个
            categories = Category.objects.filter(id__in=category_id)

            post = Post.objects.create(title=title, content=content, author=author, status=status)
            for category in categories:
                post.category.add(category)

            return JsonResponse({'status': 'success', 'message': '添加成功'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        # form = AddPostForm(data=request.POST)
        # if form.is_valid():
        #     new_post = form.save(commit=False)  # 暂时不保存
        #     new_post.author = request.user
        #     form.save()
        #     return redirect('chat:index')

@login_required
def edit_post_html(request, post_id):
    """渲染编辑帖子的html"""
    post = Post.objects.get(id=post_id)

    context = {
        'categories': Category.objects.all(),
        'post_categories': post.category.all(),
        'post': post,
        'STATUS_CHOICES': Post.STATUS_CHOICES,
    }

    return render(request,'edit_post.html', context)

@login_required
def edit_post(request, post_id):
    """编辑帖子的功能"""

    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': '只接受POST请求'}, status=405)

    else:
        try:
            post = Post.objects.get(id=post_id)
            content = request.POST.get('content')
            title = request.POST.get('title')
            status = request.POST.get('status')
            category = request.POST.getlist('category') #注意category是多个对象，所以用getlist，get只能获取到一个

            if not content:
                return JsonResponse({'status': 'error', 'message': '内容不能为空'}, status=400)

            post.title = title
            post.content = content
            post.status = status
            category_objs = Category.objects.filter(id__in=category)
            post.category.set(category_objs)  # 替换直接赋值操作
            post.save()  # 保存修改到数据库

            return JsonResponse({'status': 'success', 'message': '修改成功'})

        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '文章不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def comment(request, post_id):
    """评论区管理"""

    #评论分页
    post = Post.objects.get(id=post_id)
    # comments = post.comment.filter(parent__isnull=True).order_by('-created_at')  # 一级评论
    comments = post.comment.order_by('-created_at')  # 评论
    paginator = Paginator(comments, 4)  # 4条1页

    comment_page = request.GET.get('comment_page', 1)
    comment_obj = paginator.get_page(comment_page)

    data={
        'comments': list(comment_obj.object_list.values('id', 'content','user','user__username','user__avatar')), #value指定查询对象
        'comment_page': comment_page,
        'has_previous': comment_obj.has_previous(),
        'has_next': comment_obj.has_next(),
        'total_pages': paginator.num_pages
    }

    return JsonResponse(data)


@login_required
def add_comment(request, post_id):
    """添加评论"""
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': '只接受POST请求'}, status=405)

    try:
        user = request.user  # 直接使用request.user，无需再次查询
        post = Post.objects.get(id=post_id)
        content = request.POST.get('content')

        if not content:
            return JsonResponse({'status': 'error', 'message': '评论内容不能为空'}, status=400)

        Comment.objects.create(post=post, content=content, user=user)
        return JsonResponse({'status': 'success', 'message': '评论添加成功'})

    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '文章不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# def add_comment(request, post_id):
#     """添加评论"""
#     if request.method != 'POST':
#         comment_form = AddCommentForm()
#
#     elif request.method == 'POST' and request.user.is_authenticated:
#         comment_form = AddCommentForm(request.POST)
#         if comment_form.is_valid():
#             content = comment_form.cleaned_data['content']  # 从表单获取 content
#             # parent_id = form.cleaned_data.get('parent_id')  # 从表单获取 parent_id
#             # 获取 Post 对象
#             post = get_object_or_404(Post, id=post_id)
#             # # 处理 parent_id
#             # if parent_id:
#             #     parent = get_object_or_404(Comment, id=parent_id)
#             # else:
#             #     parent = None
#             # form.save()
#
#             new_comment = comment_form.save(commit=False)  # 暂时不保存
#             new_comment.user = request.user
#             new_comment.post = post
#             new_comment.content = content
#             new_comment.save()
#             comment_form.save()
#             return redirect('chat:post_detail', post_id=post_id)


