from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import BlogPostSitemap, BlogCategorySitemap, StaticViewSitemap
from core.news_views import google_news_sitemap

sitemaps = {
    'blog_posts': BlogPostSitemap,
    'blog_categories': BlogCategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador/', include('core.admin_urls')),  # Admin dashboard
    path('blog/', include('core.blog_urls')),  # Blog
    path('portfolio/', include('portfolio.urls')),
    path('clients/', include('clients.urls')),
    path('api/debug/', include('core.urls_debug')),  # Debug APIs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-news.xml', google_news_sitemap, name='google_news_sitemap'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
