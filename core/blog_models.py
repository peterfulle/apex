from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogCategory(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog posts with advanced SEO"""
    
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('archived', 'Archivado'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200, help_text="Título del artículo (SEO: 50-60 caracteres)")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    
    # Content
    excerpt = models.TextField(max_length=300, help_text="Resumen corto (SEO: 150-160 caracteres)")
    content = models.TextField(help_text="Contenido completo del artículo (formato HTML)")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True, help_text="Texto alternativo para SEO")
    
    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO Title (50-60 caracteres)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Meta description (150-160 caracteres)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Palabras clave separadas por comas")
    canonical_url = models.URLField(blank=True, help_text="URL canónica si aplica")
    
    # Open Graph / Social Media
    og_title = models.CharField(max_length=100, blank=True, help_text="Título para redes sociales")
    og_description = models.CharField(max_length=200, blank=True, help_text="Descripción para redes sociales")
    og_image = models.ImageField(upload_to='blog/og/', blank=True, null=True, help_text="1200x630px")
    
    # Schema.org / Structured Data
    schema_type = models.CharField(max_length=50, default='Article')
    
    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Analytics
    views_count = models.IntegerField(default=0)
    reading_time = models.IntegerField(default=5, help_text="Tiempo de lectura en minutos")
    
    # Related Content
    tags = models.CharField(max_length=255, blank=True, help_text="Tags separados por comas")
    related_posts = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-fill SEO fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        if not self.og_title:
            self.og_title = self.title[:100]
        if not self.og_description:
            self.og_description = self.excerpt[:200]
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_reading_time(self):
        """Calculate reading time based on content"""
        words = len(self.content.split())
        minutes = max(1, words // 200)  # Average 200 words per minute
        return minutes
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
