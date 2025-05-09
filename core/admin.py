from django.contrib import admin
from .models import Service, Contact, Testimonial

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order']
    search_fields = ['title', 'description']
    list_editable = ['order']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'read']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['read', 'created_at']
    readonly_fields = ['created_at']
    list_editable = ['read']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'active', 'order']
    search_fields = ['name', 'company', 'quote']
    list_filter = ['active', 'rating']
    list_editable = ['active', 'order']