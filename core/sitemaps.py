from django.contrib import sitemaps
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from core.models import BlogPost, BlogCategory

class BlogPostSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return BlogPost.objects.filter(status='published').order_by('-published_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class GoogleNewsSitemap(sitemaps.Sitemap):
    """Sitemap específico para Google News - Solo artículos de últimos 2 días"""
    changefreq = "hourly"
    priority = 1.0
    protocol = 'https'
    limit = 1000

    def items(self):
        # Google News solo indexa contenido de últimos 2 días
        two_days_ago = timezone.now() - timedelta(days=2)
        return BlogPost.objects.filter(
            status='published',
            is_news=True,
            published_at__gte=two_days_ago
        ).order_by('-published_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

    # Google News specific attributes
    def news_publication_name(self):
        return "Aplyfly Tech News"

    def news_publication_language(self):
        return "es"

    def news_genres(self):
        return "Blog, OpinionAndAnalysis"

    def news_keywords(self, obj):
        keywords = obj.meta_keywords if obj.meta_keywords else ""
        if obj.news_keywords_extra:
            keywords += ", " + obj.news_keywords_extra
        return keywords

    def news_stock_tickers(self):
        return ""


class BlogCategorySitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return BlogCategory.objects.all()

    def lastmod(self, obj):
        # Get most recent post in category
        latest_post = BlogPost.objects.filter(
            category=obj, 
            status='published'
        ).order_by('-updated_at').first()
        return latest_post.updated_at if latest_post else obj.created_at

    def location(self, obj):
        return f'/blog/categoria/{obj.slug}/'

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['index', 'services', 'servicios_ia', 'blog:list']

    def location(self, item):
        return reverse(item)
