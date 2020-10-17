from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    """User blog"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return 'Blog ' + str(self.owner.username)


class Post(models.Model):
    """Blog posts"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=160)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Post ' + (self.blog.owner.username) + ' ' + self.date.__str__()

    class Meta:
        ordering = ('-date',)


class ActionPost(models.Model):
    """User actions on a post"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='action_post')
