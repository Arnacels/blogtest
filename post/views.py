from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import Post, Blog


# Create your views here.
class HomePageView(generic.list.ListView):
    """Home page. Simple view list all post"""
    model = Post
    paginate_by = 5
    template_name = 'post/home.html'


class BlogDetail(HomePageView):
    """Feed page. Override context data for control button viewed.
    Extends class HomePage"""
    template_name = 'post/blog.html'

    def get_queryset(self):
        return Post.objects.filter(blog__owner__username=self.kwargs.get('username'))


class PostDetail(generic.detail.DetailView):
    """Post detail. Filter username and id"""
    model = Post
    template_name = 'post/post.html'

    def get_queryset(self):
        return Post.objects.filter(blog__owner__username=self.kwargs.get('username'), id=self.kwargs.get('pk'))


class FeedUserView(LoginRequiredMixin, BlogDetail, ):
    """User Feed. Extends LoginRequiredMixin and BlogDetail."""
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    template_name = 'post/feed.html'

    def get_queryset(self):
        return Post.objects.filter(blog__subscribers=self.request.user)


class UpdateVisionView(LoginRequiredMixin, UpdateView):
    model = Post
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        post.views.add(request.user)
        return HttpResponseRedirect(reverse('my_feed'))

    def get_success_url(self):
        return reverse('my_feed')


class SubscribeUnsubscribeView(LoginRequiredMixin, UpdateView):
    model = Blog
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, id=request.POST.get('blog_id'))
        user = self.request.user
        if user in blog.subscribers.all():
            blog.subscribers.remove(user)
            list(map(lambda post: post.views.remove(user), Post.objects.filter(blog=blog)))
        else:
            blog.subscribers.add(user)
        return HttpResponseRedirect(reverse('my_feed'))

    def get_success_url(self):
        return reverse('my_feed')
