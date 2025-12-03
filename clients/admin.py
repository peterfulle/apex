from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    CustomUser, Project, ProjectCategory, ProjectTechnology, 
    ProjectTechnologyRelation, ProjectUpdate, ProjectMessage,
    ServiceRequest, ClientNotification
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin for CustomUser model"""
    list_display = ('username', 'email', 'get_full_name', 'company', 'is_client', 'is_staff', 'date_joined')
    list_filter = ('is_client', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Client Information', {
            'fields': ('phone', 'company', 'position', 'avatar', 'is_client')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Client Information', {
            'fields': ('email', 'phone', 'company', 'position', 'is_client')
        }),
    )

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """Admin for ProjectCategory model"""
    list_display = ('name', 'icon', 'color', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}

@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    """Admin for ProjectTechnology model"""
    list_display = ('name', 'category', 'icon', 'color')
    list_filter = ('category',)
    search_fields = ('name', 'category')

class ProjectUpdateInline(admin.TabularInline):
    """Inline admin for ProjectUpdate"""
    model = ProjectUpdate
    extra = 0
    readonly_fields = ('created_at',)

class ProjectMessageInline(admin.TabularInline):
    """Inline admin for ProjectMessage"""
    model = ProjectMessage
    extra = 0
    readonly_fields = ('created_at',)

class ProjectTechnologyInline(admin.TabularInline):
    """Inline admin for ProjectTechnology relationship"""
    model = ProjectTechnologyRelation
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for Project model"""
    list_display = (
        'title', 'client', 'status', 'priority', 'progress_percentage', 
        'get_status_badge', 'created_at'
    )
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description', 'client__username', 'client__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'client', 'title', 'description', 'category')
        }),
        ('Project Details', {
            'fields': ('status', 'priority', 'budget_range', 'estimated_duration', 'progress_percentage')
        }),
        ('Dates', {
            'fields': ('start_date', 'deadline', 'completion_date')
        }),
        ('Files', {
            'fields': ('requirements_document',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ProjectTechnologyInline, ProjectUpdateInline, ProjectMessageInline]
    
    def get_status_badge(self, obj):
        color_map = {
            'draft': 'gray',
            'submitted': 'blue',
            'in_review': 'yellow',
            'approved': 'green',
            'in_development': 'purple',
            'testing': 'orange',
            'completed': 'emerald',
            'on_hold': 'amber',
            'cancelled': 'red',
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    get_status_badge.short_description = 'Status Badge'

@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    """Admin for ProjectUpdate model"""
    list_display = ('title', 'project', 'progress_percentage', 'created_by', 'created_at')
    list_filter = ('created_at', 'progress_percentage')
    search_fields = ('title', 'description', 'project__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(ProjectMessage)
class ProjectMessageAdmin(admin.ModelAdmin):
    """Admin for ProjectMessage model"""
    list_display = ('project', 'sender', 'get_message_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message', 'project__title', 'sender__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def get_message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    get_message_preview.short_description = 'Message Preview'

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin for ServiceRequest model"""
    list_display = (
        'title', 'client', 'service_type', 'status', 'urgency', 
        'get_status_badge', 'created_at'
    )
    list_filter = ('service_type', 'status', 'urgency', 'created_at')
    search_fields = ('title', 'description', 'client__username', 'client__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'client', 'service_type', 'title', 'description')
        }),
        ('Request Details', {
            'fields': ('status', 'urgency', 'budget_range', 'timeline')
        }),
        ('Quote Information', {
            'fields': ('quote_amount', 'quote_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_status_badge(self, obj):
        color_map = {
            'pending': 'yellow',
            'in_review': 'blue',
            'quoted': 'purple',
            'approved': 'green',
            'rejected': 'red',
            'converted': 'emerald',
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    get_status_badge.short_description = 'Status Badge'

@admin.register(ClientNotification)
class ClientNotificationAdmin(admin.ModelAdmin):
    """Admin for ClientNotification model"""
    list_display = ('title', 'client', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'client__username', 'client__email')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notificaciones marcadas como leídas.')
    mark_as_read.short_description = 'Marcar como leídas'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notificaciones marcadas como no leídas.')
    mark_as_unread.short_description = 'Marcar como no leídas'
