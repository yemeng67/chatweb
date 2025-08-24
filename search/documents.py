# from django_elasticsearch_dsl import Document, Index, fields
# from django_elasticsearch_dsl.registries import registry
# from index.models import User, Post, Category
#
# # 帖子索引
# @registry.register_document
# class PostDocument(Document):
#     category_names = fields.ListField(fields.KeywordField())
#
#     def prepare_category_names(self, instance):
#         return [cat.name for cat in instance.category.all()]
#
#     author = fields.ObjectField(
#         properties={
#             'id': fields.IntegerField(),
#             'username': fields.TextField(),
#             'avatar': fields.TextField(attr='avatar.url'),  # 处理头像路径
#             'nickname': fields.TextField(),
#             'email': fields.TextField()
#         },
#         related_model=User #明确关联模型
#     )
#
#     class Index:
#         name = 'posts'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#             'analysis': {
#                 'analyzer': {
#                     'ik_smart': {
#                         'type': 'custom',
#                         'tokenizer': 'ik_smart'
#                     }
#                 }
#             }
#         }
#
#     class Django:
#         model = Post
#         fields = [
#             'id',
#             'title',
#             'content',
#             'status',
#             'views',
#             'created_at'
#         ]
#         related_models = [User, Category]
#
#     # 添加高亮字段
#     @classmethod
#     def prepare_highlight(cls, instance):
#         return {
#             'fields': {
#                 'title': {'pre_tags': ['<em>'], 'post_tags': ['</em>']},
#                 'content': {'pre_tags': ['<em>'], 'post_tags': ['</em>']}
#             }
#         }
#
#     @classmethod
#     def get_related_posts(cls, related_instance):
#         """
#         根据传入的 User 或 Category 实例，返回相关的 Post 实例。
#         """
#         if isinstance(related_instance, User):
#             return related_instance.post.all()
#         elif isinstance(related_instance, Category):
#             return related_instance.post.all()
#         else:
#             return cls().get_queryset().none()
#
#     @classmethod
#     def get_instances_from_related(cls, related_instance):
#        """
#        根据 User 或 Category 实例返回相关的 Post 文档。
#        这个方法用于 elasticsearch_dsl 的信号同步机制。
#        """
#        return cls.get_related_posts(related_instance)
#
#
#
# # 用户索引
# @registry.register_document
# class UserDocument(Document):
#     username = fields.KeywordField()
#     email = fields.KeywordField()
#     nickname = fields.TextField()
#
#     class Index:
#         name = 'users'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 0}
#
#     class Django:
#         model = User
#
# # 分类索引
# @registry.register_document
# class CategoryDocument(Document):
#     name = fields.KeywordField()
#
#     class Index:
#         name = 'categories'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 0}
#
#     class Django:
#         model = Category