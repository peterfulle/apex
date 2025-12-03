from django.urls import path
from . import blog_views

app_name = 'blog'

urlpatterns = [
    path('', blog_views.blog_list, name='list'),
    path('categoria/<slug:slug>/', blog_views.blog_category, name='category'),
    path('<slug:slug>/', blog_views.blog_detail, name='post_detail'),
]
