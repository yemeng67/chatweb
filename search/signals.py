# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from index.models import User,Category,Post
# from .documents import (UserDocument, CategoryDocument,PostDocument,)
#
# @receiver(post_save, sender=User)
# def update_user_in_post_index(sender, instance, **kwargs):
#     for post in instance.post.all():
#         PostDocument().update(post)
#
# @receiver(post_delete, sender=Category)
# def delete_category(sender, instance, **kwargs):
#     for post in instance.post.all():
#         PostDocument().update(post)
