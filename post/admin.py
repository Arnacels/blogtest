from django.contrib import admin
from .models import Post, Blog


# Register your models here.
admin.site.register((Blog, Post))