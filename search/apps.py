# from django.apps import AppConfig
#
# class SearchConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'search'
#
#     #启用信号监听
#     def ready(self):
#         import search.signals
#         from django_elasticsearch_dsl.registries import registry
#         registry.get_indices()  # 强制加载所有文档索引
