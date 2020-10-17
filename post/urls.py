from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(),  name='home'),
    path('my_feed/', views.FeedUserView.as_view(),  name='my_feed'),
    path('blog/<username>/', views.BlogDetail.as_view(),  name='blog'),
    path('blog/<username>/<pk>/', views.PostDetail.as_view(),  name='blog_detail'),
    path('subscribed/', views.SubscribeUnsubscribeView.as_view(),  name='subscribe'),
    path('viewed/', views.UpdateVisionView.as_view(),  name='view'),
]