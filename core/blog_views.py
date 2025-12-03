from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import BlogPost, BlogCategory


def blog_list(request):
    """Blog list view with pagination and filters"""
    posts = BlogPost.objects.filter(status='published', published_at__lte=timezone.now()).select_related('author', 'category')
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Tag filter
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__icontains=tag)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categories for sidebar
    categories = BlogCategory.objects.all()
    
    # Recent posts for sidebar
    recent_posts = BlogPost.objects.filter(
        status='published', 
        published_at__lte=timezone.now()
    ).order_by('-published_at')[:5]
    
    # Popular posts
    popular_posts = BlogPost.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-views_count')[:5]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tag': tag,
    }
    
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    """Blog post detail view with SEO optimization"""
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category'),
        slug=slug,
        status='published',
        published_at__lte=timezone.now()
    )
    
    # Increment views
    post.increment_views()
    
    # Related posts
    related_posts = post.related_posts.filter(
        status='published',
        published_at__lte=timezone.now()
    )[:3]
    
    # If no related posts, get from same category
    if not related_posts.exists() and post.category:
        related_posts = BlogPost.objects.filter(
            category=post.category,
            status='published',
            published_at__lte=timezone.now()
        ).exclude(id=post.id)[:3]
    
    # Recent posts for sidebar
    recent_posts = BlogPost.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).exclude(id=post.id).order_by('-published_at')[:5]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'blog/detail.html', context)


def blog_category(request, slug):
    """Category view"""
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(
        category=category,
        status='published',
        published_at__lte=timezone.now()
    ).select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categories for sidebar
    categories = BlogCategory.objects.all()
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    }
    
    return render(request, 'blog/category.html', context)
