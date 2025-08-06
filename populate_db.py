#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
django.setup()

from portfolio.models import Category, Technology, Project
from core.models import Service, Testimonial

def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear categorías
    web_category, _ = Category.objects.get_or_create(
        name="Desarrollo Web",
        slug="desarrollo-web"
    )
    
    mobile_category, _ = Category.objects.get_or_create(
        name="Aplicaciones Móviles",
        slug="aplicaciones-moviles"
    )
    
    # Crear tecnologías
    django_tech, _ = Technology.objects.get_or_create(
        name="Django",
        icon="fab fa-python"
    )
    
    react_tech, _ = Technology.objects.get_or_create(
        name="React",
        icon="fab fa-react"
    )
    
    python_tech, _ = Technology.objects.get_or_create(
        name="Python",
        icon="fab fa-python"
    )
    
    js_tech, _ = Technology.objects.get_or_create(
        name="JavaScript",
        icon="fab fa-js"
    )
    
    postgres_tech, _ = Technology.objects.get_or_create(
        name="PostgreSQL",
        icon="fas fa-database"
    )
    
    aws_tech, _ = Technology.objects.get_or_create(
        name="AWS",
        icon="fab fa-aws"
    )
    
    # Crear proyectos de ejemplo
    project1, created = Project.objects.get_or_create(
        title="E-Commerce Platform",
        slug="ecommerce-platform",
        defaults={
            'description': "Plataforma de comercio electrónico completa desarrollada con Django y React. Incluye sistema de pagos, gestión de inventario, panel de administración y analytics en tiempo real. La aplicación maneja más de 10,000 productos y procesa cientos de transacciones diarias.",
            'short_description': "Plataforma de e-commerce escalable con Django y React",
            'client': "TechCorp Solutions",
            'completed_date': "2024-12-01",
            'category': web_category,
            'url': "https://example-ecommerce.com",
            'featured': True
        }
    )
    
    if created:
        project1.technologies.set([django_tech, react_tech, python_tech, postgres_tech, aws_tech])
    
    project2, created = Project.objects.get_or_create(
        title="Task Management App",
        slug="task-management-app",
        defaults={
            'description': "Aplicación móvil para gestión de tareas y productividad personal. Desarrollada con React Native, incluye sincronización en tiempo real, notificaciones push, modo offline y integración con calendarios. Más de 5,000 usuarios activos.",
            'short_description': "App móvil de productividad con React Native",
            'client': "StartupXYZ",
            'completed_date': "2024-10-15",
            'category': mobile_category,
            'url': "https://taskapp-demo.com",
            'featured': True
        }
    )
    
    if created:
        project2.technologies.set([react_tech, js_tech, aws_tech])
    
    project3, created = Project.objects.get_or_create(
        title="AI Analytics Dashboard",
        slug="ai-analytics-dashboard",
        defaults={
            'description': "Dashboard inteligente para análisis de datos empresariales utilizando Machine Learning. Procesamiento en tiempo real de big data, visualizaciones interactivas y predicciones automatizadas. Reduce el tiempo de análisis en un 80%.",
            'short_description': "Dashboard de analytics con IA y ML",
            'client': "DataInsights Inc",
            'completed_date': "2024-11-20",
            'category': web_category,
            'url': "https://ai-dashboard-demo.com",
            'featured': True
        }
    )
    
    if created:
        project3.technologies.set([python_tech, django_tech, react_tech, postgres_tech, aws_tech])
    
    # Crear servicios
    Service.objects.get_or_create(
        title="Desarrollo Full-Stack",
        icon="fas fa-code",
        description="Desarrollo completo de aplicaciones web con tecnologías modernas",
        order=1
    )
    
    Service.objects.get_or_create(
        title="Desarrollo Móvil",
        icon="fas fa-mobile-alt",
        description="Aplicaciones móviles nativas e híbridas para iOS y Android",
        order=2
    )
    
    Service.objects.get_or_create(
        title="Cloud & DevOps",
        icon="fas fa-cloud",
        description="Infraestructura en la nube y automatización de procesos",
        order=3
    )
    
    # Crear testimonios
    Testimonial.objects.get_or_create(
        name="María González",
        position="CTO",
        company="TechCorp Solutions",
        defaults={
            'quote': "Peter transformó completamente nuestra visión en una plataforma robusta y escalable. Su atención al detalle y experiencia técnica son excepcionales.",
            'rating': 5,
            'active': True,
            'order': 1
        }
    )
    
    Testimonial.objects.get_or_create(
        name="Carlos Rodríguez",
        position="Founder",
        company="StartupXYZ",
        defaults={
            'quote': "Trabajar con Peter fue una experiencia increíble. Entregó nuestra app móvil a tiempo y superó todas nuestras expectativas.",
            'rating': 5,
            'active': True,
            'order': 2
        }
    )
    
    print("✅ Datos de ejemplo creados exitosamente!")
    print(f"📊 Proyectos creados: {Project.objects.count()}")
    print(f"🔧 Servicios creados: {Service.objects.count()}")
    print(f"💬 Testimonios creados: {Testimonial.objects.count()}")

if __name__ == "__main__":
    create_sample_data()
