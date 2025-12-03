from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_client = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

class ProjectCategory(models.Model):
    """Categories for different types of projects"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-code')
    color = models.CharField(max_length=20, default='blue')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Project Categories"
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """Client projects"""
    PROJECT_STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('submitted', 'Enviado'),
        ('in_review', 'En Revisión'),
        ('approved', 'Aprobado'),
        ('in_development', 'En Desarrollo'),
        ('testing', 'En Pruebas'),
        ('completed', 'Completado'),
        ('on_hold', 'En Pausa'),
        ('cancelled', 'Cancelado'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Budget fields
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_range = models.CharField(max_length=50, blank=True, null=True)  # Keep for compatibility
    
    # Timeline fields
    estimated_duration = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    progress_percentage = models.IntegerField(default=0)
    
    # Additional requirements
    requirements = models.TextField(blank=True, help_text="Requisitos técnicos y funcionalidades")
    reference_urls = models.TextField(blank=True, help_text="URLs de referencia (una por línea)")
    special_notes = models.TextField(blank=True, help_text="Notas y restricciones especiales")
    
    # Documents
    requirements_document = models.FileField(upload_to='requirements/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.client.get_full_name()}"
    
    def get_absolute_url(self):
        return reverse('clients:project_detail', kwargs={'pk': self.pk})
    
    def get_status_color(self):
        status_colors = {
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
        return status_colors.get(self.status, 'gray')

class ProjectAttachment(models.Model):
    """Attachments for projects (multiple files support)"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='project_attachments/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.IntegerField(default=0, help_text="Size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.file_name}"
    
    def get_file_size_display(self):
        """Return file size in human readable format"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

class ProjectTechnology(models.Model):
    """Technologies/tools used in projects"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)  # frontend, backend, database, etc.
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, default='blue')
    
    def __str__(self):
        return self.name

class ProjectTechnologyRelation(models.Model):
    """Many-to-many relationship between projects and technologies"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    technology = models.ForeignKey(ProjectTechnology, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('project', 'technology')

class ProjectUpdate(models.Model):
    """Updates and progress reports for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    description = models.TextField()
    progress_percentage = models.IntegerField(default=0)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(upload_to='project_updates/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"

class ProjectMessage(models.Model):
    """Messages between client and development team"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='messages/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.sender.get_full_name()}"

class ServiceRequest(models.Model):
    """Requests for specific services"""
    SERVICE_TYPES = [
        ('web_development', 'Desarrollo Web'),
        ('mobile_app', 'Aplicación Móvil'),
        ('ai_service', 'Servicios IA'),
        ('webapp', 'WebApp Avanzada'),
        ('consulting', 'Consultoría'),
        ('maintenance', 'Mantenimiento'),
        ('other', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_review', 'En Revisión'),
        ('quoted', 'Cotizado'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('converted', 'Convertido a Proyecto'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='service_requests')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    urgency = models.CharField(max_length=10, choices=Project.PRIORITY_CHOICES, default='medium')
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quote_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.client.get_full_name()}"
    
    def get_status_color(self):
        status_colors = {
            'pending': 'yellow',
            'in_review': 'blue',
            'quoted': 'purple',
            'approved': 'green',
            'rejected': 'red',
            'converted': 'emerald',
        }
        return status_colors.get(self.status, 'gray')

class ClientNotification(models.Model):
    """Notifications for clients"""
    NOTIFICATION_TYPES = [
        ('project_update', 'Actualización de Proyecto'),
        ('message', 'Nuevo Mensaje'),
        ('status_change', 'Cambio de Estado'),
        ('quote_ready', 'Cotización Lista'),
        ('deadline_reminder', 'Recordatorio de Fecha Límite'),
        ('system', 'Notificación del Sistema'),
    ]
    
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    related_service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client.get_full_name()} - {self.title}"
