from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    #主页
    path("index/",views.index,name="index"),
    path("index_data/",views.index_data,name="index_data"),

    #帖子相关
    path("post_detail/<int:post_id>",views.post_detail,name="post_detail"),
    path("add_post/",views.add_post,name="add_post"),
    path("edit_post/<int:post_id>",views.edit_post,name="edit_post"),
    path('edit_post_html/<int:post_id>', views.edit_post_html, name='edit_post_html'),
    path('like_post/<int:post_id>', views.like_post, name='like_post'),

    #评论相关
    path("add_comment/<int:post_id>",views.add_comment,name="add_comment"),
    path("comment/<int:post_id>",views.comment,name="comment"),

    #基础
    path("base/",views.base,name="base"),

]
