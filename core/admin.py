from django.contrib import admin
from .models import Service, Testimonial, ContactMessage, BlogCategory, BlogPost

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'active', 'order')
    list_editable = ('active', 'order')
    list_filter = ('active', 'rating')
    search_fields = ('name', 'company', 'quote')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'read')
    list_editable = ('read',)
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_news', 'published_at', 'views_count')
    list_filter = ('status', 'is_news', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'content', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    filter_horizontal = ('related_posts',)
    list_editable = ('is_news',)
    
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content', 'featured_image', 'featured_image_alt')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url'),
            'classes': ('collapse',)
        }),
        ('Redes Sociales (Open Graph)', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Google News', {
            'fields': ('is_news', 'news_location', 'news_keywords_extra'),
            'classes': ('collapse',),
            'description': 'Marcar como noticia para aparecer en Google News. Solo artículos de últimos 2 días son indexados.'
        }),
        ('Publicación', {
            'fields': ('status', 'published_at')
        }),
        ('Metadata', {
            'fields': ('schema_type', 'reading_time', 'views_count', 'tags', 'related_posts', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
