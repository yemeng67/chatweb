from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from index.models import Post,Category,PostLike,Comment
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http.response import JsonResponse


def search_index(request):
    """搜索入口视图"""
    keyword = request.GET.get('q', '')
    return render(request, 'search_results.html', {'keyword': keyword})


def search_data(request):
    """搜索数据接口"""
    # 参数校验
    keyword = request.GET.get('q', '').strip()
    if not keyword:
        return JsonResponse({'error': '关键词不能为空'}, status=400)

    if len(keyword) > 10:
        return JsonResponse({'error': '关键词过长'}, status=400)

    # 查询构建
    search_terms = keyword.split()
    q_objects = Q()
    for term in search_terms:
        q_objects |= Q(title__icontains=term) | Q(content__icontains=term)

    # 获取排序参数，默认为'views'
    sort_by = request.GET.get('sort', 'views')

    # 先进行注解，确保排序和显示使用相同的计算方式
    posts = Post.objects.filter(q_objects) \
        .annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comment', distinct=True)
    )

    # 排序处理
    valid_sort_fields = {'views', 'likes', 'created_at'}
    if sort_by == 'likes':
        sort_field = '-like_count'
    elif sort_by == 'views':
        sort_field = '-views'
    elif sort_by == 'created_at':
        sort_field = '-created_at'
    else:
        sort_field = '-created_at'

    posts = posts.order_by(sort_field)

    # 分页处理
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    # 构造响应数据
    return JsonResponse({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'content': post.content[:100] + '...',
            'author_avatar': post.author.avatar.url if post.author.avatar else '',
            'author': post.author.username,
            'views': post.views,
            'likes': post.like_count,  # 使用注解的like_count，确保与排序一致
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M')
        } for post in posts_page],
        'pagination': {
            'current_page': posts_page.number,
            'total_pages': paginator.num_pages,
            'has_next': posts_page.has_next(),
            'has_previous': posts_page.has_previous()
        }
    })
