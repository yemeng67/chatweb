# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
# from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
# from elasticsearch_dsl import Q
# from django.http.response import JsonResponse
# from index.models import User
# from rest_framework import serializers
# from .documents import PostDocument
# from django.shortcuts import render
#
#
# def search(request):
#     return render(request,'search_results.html')
#
# # 使用 Django REST framework 的分页
# class CustomPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100
#
#
# class PostDocumentSerializer(serializers.Serializer):
#     # 基础字段映射
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     content_excerpt = serializers.SerializerMethodField()  # 自定义摘要字段
#
#     # 关联字段处理
#     author_info = serializers.SerializerMethodField()
#     category_names = serializers.ListField(child=serializers.CharField())
#
#     # 统计字段
#     views = serializers.IntegerField()
#     likes_count = serializers.IntegerField()
#
#     class Meta:
#         document = PostDocument
#         fields = [
#             'id', 'title', 'content_excerpt', 'author_info',
#             'category_names', 'views', 'likes_count', 'created_at'
#         ]
#
#     def get_content_excerpt(self, obj):
#         """生成内容摘要（带高亮）"""
#         return obj.meta.highlight.content[0]if obj.meta.highlight else obj.content[:50]  # 作者信息处理
#
#     def get_author_info(self, obj):
#         try:
#             user = User.objects.get(id=obj.author.id)
#             return {
#                 'username': user.username,
#                 'avatar': user.avatar.url,
#                 'nickname': user.nickname
#             }
#         except User.DoesNotExist:
#             return {}
#
#     # 时间格式化
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
#         return data
#
#     # 实时获取点赞数
#     def get_likes_count(self, obj):
#         return obj.likes.count()
#
#
# class PostSearchViewSet(DocumentViewSet):
#     document = PostDocument
#     serializer_class = PostDocumentSerializer  # 需要自定义序列化器
#     pagination_class = CustomPagination    #分页
#     lookup_field = 'id'
#
#     def get_queryset(self):
#         # 构建基础查询
#         query = Q(
#             "multi_match",
#             query=self.request.query_params.get('q', ''),
#             fields=['title^3', 'content'],  # 标题权重更高
#             type="best_fields"
#         ) & Q("term", status="published")  # 过滤已发布状态
#
#         return self.document.search().query(query)
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         search_hits = response.hits.hits
#
#         # 高亮配置
#         return JsonResponse({
#             'results': [{
#                 **hit.meta.source,  #基础字段
#                 '_highlight': hit.highlight,  #高亮数据
#                 'author_info': self._get_author_info(hit.meta.source.author_id),
#                 'category_names': hit.category_names
#             } for hit in search_hits],
#             'total': response.hits.total.value
#         })
#
#     def _get_author_info(self, author_id):
#         """通过ID查询作者信息"""
#         try:
#             user = User.objects.select_related('avatar').get(id=author_id)
#             return {
#                 'username': user.username,
#                 'nickname': user.nickname,
#                 'avatar': user.avatar.url if user.avatar else None
#             }
#         except User.DoesNotExist:
#             return {}
#
