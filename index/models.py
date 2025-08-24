from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
def user_avatar_path(instance, filename):
    """设置头像储存路径"""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex[:8]}.{ext}"  #避免路径上的用户id重复
    return os.path.join("avatars", str(instance.id), new_filename)


class User(AbstractUser):
    """用户表"""
    email = models.EmailField(max_length=254, unique=True)
    nickname = models.CharField(max_length=120,default='游客')  #昵称
    bio = models.TextField(null=True, blank=True, verbose_name='简介') #简介
    last_login_ip = models.GenericIPAddressField(null=True, blank=True) #最后登录ip
    last_login = models.DateTimeField(null=True, blank=True)  #最后登录时间
    created_at = models.DateTimeField(auto_now_add=True)      #注册时间
    avatar = models.ImageField(upload_to=user_avatar_path, verbose_name="头像", blank=True, null=True,default='avatars/default/申鹤.jpg')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='index_user_groups',  # 添加 related_name 以避免冲突
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='index_user_groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='index_user_permissions',  # 添加 related_name 以避免冲突
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='index_user',
    )

    class Meta:
        db_table = 'user'
        verbose_name = '用户信息'

@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    """在保存新头像前删除旧头像文件"""
    if instance.pk:  # 仅处理已存在的用户（更新操作）
        try:
            old_user = User.objects.get(pk=instance.pk)
            # 检查旧头像是否存在且与新头像不同
            if old_user.avatar and old_user.avatar != instance.avatar:
                # 删除旧头像文件
                if os.path.isfile(old_user.avatar.path):
                    os.remove(old_user.avatar.path)
        except User.DoesNotExist:
            pass  # 新用户无需处理


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=200,db_index=True,unique=True) #名称且唯一
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)          #是否启用

    class Meta:
        db_table = 'category'
        verbose_name = '分类表'

    def __str__(self):
        return self.name


class Post(models.Model):
    """帖子相关"""
    STATUS_CHOICES = (
        ('draft','草稿'),
        ('published','发布'),
    )
    title = models.CharField(max_length=200,db_index=True) #标题，索引
    content = models.TextField()                           #内容
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')  #作者外键。一对多，且当作者被删除时，所有相关的帖子都被删除
    category = models.ManyToManyField(Category,related_name='post',blank=True) #分类外键，多对多
    favourite = models.ManyToManyField(User,related_name='favourite_post',blank=True)   #该帖子的收藏用户
    likes = models.ManyToManyField(User,through='PostLike',related_name='like_post',blank=True)           #该帖子的点赞用户
    created_at = models.DateTimeField(auto_now_add=True)   #创建时间
    updated_at = models.DateTimeField(auto_now=True)       #更新时间
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') #状态，默认草稿
    views = models.PositiveIntegerField(default=0)         #浏览量

    class Meta:
        db_table = 'post'
        verbose_name = '帖子'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment') #帖子外键
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment') #评论用户
    content = models.TextField()  #评论内容
    parent = models.ForeignKey('self',on_delete=models.CASCADE,related_name='children',null=True,blank=True) #父级评论，嵌套
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)  #点赞数，只能是整数

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'

    def __str__(self):
        return self.content


class PostLike(models.Model):
    """帖子点赞 中间表"""
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post','user')   #防止重复点赞
        db_table = 'post_like'
        verbose_name = '具体点赞情况'


def user_file_path(instance, filename):
    """设置用户文件储存路径"""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex[:8]}.{ext}"  #避免路径上的用户id重复
    return os.path.join("file", str(instance.user.id), new_filename)

class UserFile(models.Model):
    """用户文件"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_file_path)  # 普通文件表
    upload_time = models.DateTimeField(auto_now_add=True)

