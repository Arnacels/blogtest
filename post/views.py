from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import Post, ActionPost, Blog


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_queryset()
        context['actions'] = [act.post for act in ActionPost.objects.filter(user=self.request.user, post__in=post)]
        return context

    def get_queryset(self):
        return Post.objects.filter(blog__owner__username=self.kwargs.get('username'))


class PostDetail(generic.detail.DetailView):
    """Post detail. Filter username and id"""
    model = Post
    template_name = 'post/post.html'

    def get_queryset(self):
        return Post.objects.filter(blog__owner__username=self.kwargs.get('username'), id=self.kwargs.get('pk'))


class FeedUserView(LoginRequiredMixin, BlogDetail,):
    """User Feed. Extends LoginRequiredMixin and BlogDetail."""
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    template_name = 'post/feed.html'

    def get_queryset(self):
        return Post.objects.filter(blog__subscribers=self.request.user)


class UpdateVisionView(LoginRequiredMixin, UpdateView):
    model = ActionPost
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        action = ActionPost.objects.get_or_create(post=post, user=request.user)
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
            action = ActionPost.objects.filter(post__blog=blog, user=user)
            action.delete()
        else:
            blog.subscribers.add(user)
        return HttpResponseRedirect(reverse('my_feed'))

    def get_success_url(self):
        return reverse('my_feed')
