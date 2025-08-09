from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, help_text="Nombre del ícono de Font Awesome")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    class Meta:
        ordering = ['order']

class ContactMessage(models.Model):
    PROJECT_TYPES = [
        ('saas-app', 'Desarrollo de Aplicaciones y Software SaaS'),
        ('mobile-app', 'Aplicación Móvil'),
        ('enterprise', 'Sistema Empresarial'),
        ('api', 'API/Backend'),
        ('ai-architecture', 'Arquitectura de Software con IA'),
        ('other', 'Otro'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, choices=PROJECT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"
    
    class Meta:
        ordering = ['-created_at']
