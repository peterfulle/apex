from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from core.models import BlogPost


def google_news_sitemap(request):
    """
    Genera un sitemap específico para Google News con formato XML correcto
    Google News requiere: publication name, publication date, title
    Solo indexa contenido de últimos 2 días
    """
    # Obtener artículos de noticias de últimos 2 días
    two_days_ago = timezone.now() - timedelta(days=2)
    news_posts = BlogPost.objects.filter(
        status='published',
        is_news=True,
        published_at__gte=two_days_ago
    ).order_by('-published_at')[:1000]  # Límite de Google News
    
    # Construir XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"')
    xml.append('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
    
    for post in news_posts:
        xml.append('  <url>')
        xml.append(f'    <loc>https://aplyfly.com{post.get_absolute_url()}</loc>')
        
        # Google News específico
        xml.append('    <news:news>')
        xml.append('      <news:publication>')
        xml.append('        <news:name>Aplyfly Tech News</news:name>')
        xml.append('        <news:language>es</news:language>')
        xml.append('      </news:publication>')
        
        # Fecha de publicación (formato W3C)
        pub_date = post.published_at.strftime('%Y-%m-%dT%H:%M:%S%z')
        xml.append(f'      <news:publication_date>{pub_date}</news:publication_date>')
        
        # Título (escapar caracteres especiales)
        title = post.title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        xml.append(f'      <news:title>{title}</news:title>')
        
        # Keywords para Google News
        if post.meta_keywords or post.news_keywords_extra:
            keywords = post.meta_keywords or ""
            if post.news_keywords_extra:
                keywords = keywords + ", " + post.news_keywords_extra if keywords else post.news_keywords_extra
            # Limpiar y limitar a 10 keywords
            keywords_list = [k.strip() for k in keywords.split(',')][:10]
            keywords_clean = ', '.join(keywords_list)
            xml.append(f'      <news:keywords>{keywords_clean}</news:keywords>')
        
        xml.append('    </news:news>')
        
        # Imagen destacada (opcional pero recomendado)
        if post.featured_image:
            xml.append('    <image:image>')
            xml.append(f'      <image:loc>https://aplyfly.com{post.featured_image.url}</image:loc>')
            if post.featured_image_alt:
                caption = post.featured_image_alt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                xml.append(f'      <image:caption>{caption}</image:caption>')
            xml.append(f'      <image:title>{title}</image:title>')
            xml.append('    </image:image>')
        
        # Last modified
        lastmod = post.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z')
        xml.append(f'    <lastmod>{lastmod}</lastmod>')
        xml.append(f'    <changefreq>hourly</changefreq>')
        xml.append(f'    <priority>1.0</priority>')
        
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    return HttpResponse('\n'.join(xml), content_type='application/xml; charset=utf-8')
