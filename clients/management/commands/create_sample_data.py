from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clients.models import (
    ProjectCategory, ProjectTechnology, Project, 
    ServiceRequest, ClientNotification
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para la plataforma de clientes'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de ejemplo...')
        
        # Crear categorías de proyectos
        categories = [
            {'name': 'Desarrollo Web', 'description': 'Sitios web y aplicaciones web', 'icon': 'fas fa-globe', 'color': 'blue'},
            {'name': 'Aplicaciones Móviles', 'description': 'Apps para iOS y Android', 'icon': 'fas fa-mobile-alt', 'color': 'green'},
            {'name': 'Inteligencia Artificial', 'description': 'Soluciones con IA y ML', 'icon': 'fas fa-brain', 'color': 'purple'},
            {'name': 'E-commerce', 'description': 'Tiendas online y marketplaces', 'icon': 'fas fa-shopping-cart', 'color': 'orange'},
            {'name': 'Sistemas Empresariales', 'description': 'ERP, CRM y sistemas internos', 'icon': 'fas fa-building', 'color': 'gray'},
        ]
        
        for cat_data in categories:
            category, created = ProjectCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Categoría creada: {category.name}')
        
        # Crear tecnologías
        technologies = [
            {'name': 'Django', 'category': 'backend', 'icon': 'fab fa-python', 'color': 'green'},
            {'name': 'React', 'category': 'frontend', 'icon': 'fab fa-react', 'color': 'blue'},
            {'name': 'Vue.js', 'category': 'frontend', 'icon': 'fab fa-vuejs', 'color': 'green'},
            {'name': 'Node.js', 'category': 'backend', 'icon': 'fab fa-node-js', 'color': 'green'},
            {'name': 'Python', 'category': 'backend', 'icon': 'fab fa-python', 'color': 'blue'},
            {'name': 'PostgreSQL', 'category': 'database', 'icon': 'fas fa-database', 'color': 'blue'},
            {'name': 'MongoDB', 'category': 'database', 'icon': 'fas fa-leaf', 'color': 'green'},
            {'name': 'Redis', 'category': 'cache', 'icon': 'fas fa-memory', 'color': 'red'},
            {'name': 'Docker', 'category': 'devops', 'icon': 'fab fa-docker', 'color': 'blue'},
            {'name': 'AWS', 'category': 'cloud', 'icon': 'fab fa-aws', 'color': 'orange'},
            {'name': 'TensorFlow', 'category': 'ai', 'icon': 'fas fa-brain', 'color': 'orange'},
            {'name': 'OpenAI', 'category': 'ai', 'icon': 'fas fa-robot', 'color': 'green'},
        ]
        
        for tech_data in technologies:
            technology, created = ProjectTechnology.objects.get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                self.stdout.write(f'✓ Tecnología creada: {technology.name}')
        
        # Crear usuario cliente de ejemplo
        client_user, created = User.objects.get_or_create(
            email='cliente@ejemplo.com',
            defaults={
                'username': 'cliente_demo',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'company': 'TechStart Solutions',
                'position': 'CTO',
                'phone': '+1234567890',
                'is_client': True,
            }
        )
        if created:
            client_user.set_password('demo123456')
            client_user.save()
            self.stdout.write(f'✓ Usuario cliente creado: {client_user.email}')
        
        # Crear proyectos de ejemplo
        if created:  # Solo crear proyectos si el usuario fue creado
            web_category = ProjectCategory.objects.get(name='Desarrollo Web')
            ai_category = ProjectCategory.objects.get(name='Inteligencia Artificial')
            
            projects_data = [
                {
                    'title': 'Plataforma E-learning Corporativa',
                    'description': 'Desarrollo de una plataforma de aprendizaje online para la empresa con sistema de evaluaciones, certificaciones y seguimiento de progreso.',
                    'category': web_category,
                    'status': 'in_development',
                    'priority': 'high',
                    'budget_range': '$15,000 - $25,000',
                    'estimated_duration': '3-4 meses',
                    'progress_percentage': 65,
                },
                {
                    'title': 'Chatbot con IA para Atención al Cliente',
                    'description': 'Implementación de un chatbot inteligente usando GPT-4 para automatizar el 80% de las consultas de soporte técnico.',
                    'category': ai_category,
                    'status': 'testing',
                    'priority': 'medium',
                    'budget_range': '$8,000 - $12,000',
                    'estimated_duration': '2-3 meses',
                    'progress_percentage': 85,
                },
                {
                    'title': 'App Mobile para Gestión de Inventarios',
                    'description': 'Aplicación móvil nativa para iOS y Android que permita gestionar inventarios en tiempo real con códigos QR.',
                    'category': ProjectCategory.objects.get(name='Aplicaciones Móviles'),
                    'status': 'approved',
                    'priority': 'high',
                    'budget_range': '$20,000 - $30,000',
                    'estimated_duration': '4-5 meses',
                    'progress_percentage': 15,
                },
                {
                    'title': 'Sistema CRM Personalizado',
                    'description': 'CRM a medida para gestión de clientes, ventas y pipeline con integraciones a herramientas existentes.',
                    'category': ProjectCategory.objects.get(name='Sistemas Empresariales'),
                    'status': 'completed',
                    'priority': 'medium',
                    'budget_range': '$12,000 - $18,000',
                    'estimated_duration': '3 meses',
                    'progress_percentage': 100,
                },
            ]
            
            for project_data in projects_data:
                project, created = Project.objects.get_or_create(
                    title=project_data['title'],
                    client=client_user,
                    defaults=project_data
                )
                if created:
                    self.stdout.write(f'✓ Proyecto creado: {project.title}')
            
            # Crear solicitudes de servicio
            service_requests_data = [
                {
                    'title': 'Optimización SEO para Sitio Web',
                    'description': 'Necesitamos mejorar el posicionamiento de nuestro sitio web actual en Google y otros buscadores.',
                    'service_type': 'web_development',
                    'status': 'quoted',
                    'urgency': 'medium',
                    'budget_range': '$3,000 - $5,000',
                    'timeline': '1-2 meses',
                    'quote_amount': 4200.00,
                },
                {
                    'title': 'Integración con API de Pagos',
                    'description': 'Integrar Stripe y PayPal en nuestra plataforma existente para procesar pagos de manera segura.',
                    'service_type': 'web_development',
                    'status': 'pending',
                    'urgency': 'high',
                    'budget_range': '$2,000 - $4,000',
                    'timeline': '2-3 semanas',
                },
                {
                    'title': 'Análisis Predictivo de Ventas',
                    'description': 'Implementar un sistema de machine learning para predecir tendencias de ventas basado en datos históricos.',
                    'service_type': 'ai_service',
                    'status': 'in_review',
                    'urgency': 'medium',
                    'budget_range': '$8,000 - $12,000',
                    'timeline': '2-3 meses',
                },
            ]
            
            for request_data in service_requests_data:
                service_request, created = ServiceRequest.objects.get_or_create(
                    title=request_data['title'],
                    client=client_user,
                    defaults=request_data
                )
                if created:
                    self.stdout.write(f'✓ Solicitud de servicio creada: {service_request.title}')
            
            # Crear notificaciones
            notifications_data = [
                {
                    'title': 'Proyecto actualizado',
                    'message': 'El proyecto "Plataforma E-learning Corporativa" ha sido actualizado. Se completó la fase de diseño UI/UX.',
                    'notification_type': 'project_update',
                    'related_project': Project.objects.get(title='Plataforma E-learning Corporativa'),
                },
                {
                    'title': 'Cotización lista',
                    'message': 'Tu solicitud de "Optimización SEO para Sitio Web" ha sido cotizada. Revisa los detalles en tu dashboard.',
                    'notification_type': 'quote_ready',
                },
                {
                    'title': 'Nuevo mensaje',
                    'message': 'Has recibido un mensaje del equipo de desarrollo sobre el proyecto "Chatbot con IA para Atención al Cliente".',
                    'notification_type': 'message',
                },
            ]
            
            for notif_data in notifications_data:
                notification, created = ClientNotification.objects.get_or_create(
                    title=notif_data['title'],
                    client=client_user,
                    defaults=notif_data
                )
                if created:
                    self.stdout.write(f'✓ Notificación creada: {notification.title}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Datos de ejemplo creados exitosamente!')
        )
        self.stdout.write('')
        self.stdout.write('📧 Usuario de prueba:')
        self.stdout.write(f'   Email: cliente@ejemplo.com')
        self.stdout.write(f'   Password: demo123456')
        self.stdout.write('')
        self.stdout.write('🔗 URLs importantes:')
        self.stdout.write(f'   Dashboard: http://127.0.0.1:8000/clients/')
        self.stdout.write(f'   Login: http://127.0.0.1:8000/clients/login/')
        self.stdout.write(f'   Admin: http://127.0.0.1:8000/admin/')
