"""
Marcar artículo de IA como noticia de Google News
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
django.setup()

from core.models import BlogPost

# Actualizar artículo
post = BlogPost.objects.get(slug='agentes-ia-empresas-2025-automatizacion-productividad')

post.is_news = True
post.news_location = "Bogotá, Colombia"
post.news_keywords_extra = "noticias tecnología, última hora ia, breaking news inteligencia artificial, actualidad empresarial, innovación 2025"

post.save()

print(f"✓ Artículo marcado como NOTICIA para Google News")
print(f"  Título: {post.title}")
print(f"  Ubicación: {post.news_location}")
print(f"  Keywords News: {post.news_keywords_extra}")
print(f"  URL Sitemap: http://127.0.0.1:8005/sitemap-news.xml")
print(f"\n✓ El artículo aparecerá en Google News (válido por 2 días desde publicación)")
