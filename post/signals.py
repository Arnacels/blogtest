from django.db.models import signals
from django.contrib.auth.models import User
from .models import Blog, Post
from .task import *


def create_user_blog(sender, instance, created, **kwargs):
    user_blog = Blog(owner=instance)
    user_blog.save()


signals.post_save.connect(receiver=create_user_blog, sender=User)


def send_notifications_subscribe(sender, instance, created, **kwargs):
    send_mail(instance)


signals.post_save.connect(receiver=create_user_blog, sender=Post)
