from django.core.management.base import BaseCommand
from core.models import Service, Testimonial
from portfolio.models import Project, Category, Technology
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Puebla la base de datos con datos iniciales para Aplyfly'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando población de datos para Aplyfly...')
        
        # Crear usuario admin si no existe
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@aplyfly.com',
                password='admin123'
            )
            self.stdout.write('👤 Usuario admin creado')
        
        # Crear categorías
        web_cat, _ = Category.objects.get_or_create(
            name='Aplicaciones Web',
            defaults={'slug': 'aplicaciones-web'}
        )
        
        mobile_cat, _ = Category.objects.get_or_create(
            name='Aplicaciones Móviles',
            defaults={'slug': 'aplicaciones-moviles'}
        )
        
        enterprise_cat, _ = Category.objects.get_or_create(
            name='Sistemas Empresariales',
            defaults={'slug': 'sistemas-empresariales'}
        )
        
        # Crear tecnologías
        technologies_data = [
            ('Python', 'fab fa-python'),
            ('Django', 'fab fa-python'),
            ('React', 'fab fa-react'),
            ('Node.js', 'fab fa-node-js'),
            ('PostgreSQL', 'fas fa-database'),
            ('Docker', 'fab fa-docker'),
            ('AWS', 'fab fa-aws'),
            ('JavaScript', 'fab fa-js'),
            ('TypeScript', 'fas fa-code'),
            ('Vue.js', 'fab fa-vuejs')
        ]
        
        technologies = []
        for tech_name, tech_icon in technologies_data:
            tech, _ = Technology.objects.get_or_create(
                name=tech_name,
                defaults={'icon': tech_icon}
            )
            technologies.append(tech)
        
        # Crear servicios si no existen
        services_data = [
            {
                'title': 'Desarrollo de Aplicaciones y Software SaaS',
                'description': 'Creamos aplicaciones web modernas y software como servicio (SaaS) escalables. Soluciones completas desde MVP hasta plataformas empresariales.',
                'icon': 'fas fa-code'
            },
            {
                'title': 'Aplicaciones Móviles',
                'description': 'Desarrollo de apps nativas y multiplataforma para iOS y Android. Experiencias móviles que conectan con tus usuarios.',
                'icon': 'fas fa-mobile-alt'
            },
            {
                'title': 'Sistemas Empresariales',
                'description': 'Soluciones corporativas robustas que automatizan procesos y mejoran la eficiencia operacional de tu empresa.',
                'icon': 'fas fa-building'
            },
            {
                'title': 'APIs y Backend',
                'description': 'Arquitecturas backend sólidas y APIs RESTful que soportan cualquier frontend y escalan con tu crecimiento.',
                'icon': 'fas fa-server'
            },
            {
                'title': 'Arquitectura de Software con IA',
                'description': 'Potenciamos tu negocio con arquitecturas inteligentes. Integración de IA, machine learning y automatización para transformar procesos empresariales.',
                'icon': 'fas fa-brain'
            },
            {
                'title': 'DevOps y Cloud',
                'description': 'Implementación de CI/CD, containerización y despliegues en la nube para máxima eficiencia y confiabilidad.',
                'icon': 'fas fa-cloud'
            }
        ]
        
        for service_data in services_data:
            Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
        
        # Crear proyectos de ejemplo si no existen
        from datetime import date
        from django.utils.text import slugify
        
        projects_data = [
            {
                'title': 'Sistema de Gestión Empresarial',
                'slug': 'sistema-gestion-empresarial',
                'description': 'Plataforma completa para gestión de inventarios, ventas y recursos humanos. Incluye dashboard analítico, reportes automatizados y integración con sistemas contables.',
                'short_description': 'Sistema completo de gestión empresarial con dashboard analítico',
                'category': enterprise_cat,
                'featured': True,
                'url': 'https://demo-empresa.aplyfly.com',
                'client': 'TechCorp Solutions',
                'completed_date': date(2024, 12, 15),
                'technologies': ['Python', 'Django', 'React', 'PostgreSQL']
            },
            {
                'title': 'E-commerce Multivendedor',
                'slug': 'ecommerce-multivendedor',
                'description': 'Marketplace completo con gestión de múltiples vendedores, procesamiento de pagos, sistema de reviews y panel administrativo avanzado.',
                'short_description': 'Marketplace completo con múltiples vendedores',
                'category': web_cat,
                'featured': True,
                'url': 'https://marketplace-demo.aplyfly.com',
                'client': 'MarketPlace Inc',
                'completed_date': date(2024, 11, 20),
                'technologies': ['Node.js', 'React', 'PostgreSQL', 'AWS']
            },
            {
                'title': 'App de Delivery',
                'slug': 'app-delivery',
                'description': 'Aplicación móvil para delivery con tracking en tiempo real, sistema de pagos integrado y panel para restaurantes.',
                'short_description': 'App móvil de delivery con tracking en tiempo real',
                'category': mobile_cat,
                'featured': True,
                'url': 'https://apps.apple.com/delivery-demo',
                'client': 'DeliveryFast',
                'completed_date': date(2024, 10, 30),
                'technologies': ['React', 'Node.js', 'PostgreSQL']
            }
        ]
        
        for project_data in projects_data:
            tech_names = project_data.pop('technologies', [])
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            
            if created:
                # Agregar tecnologías
                for tech_name in tech_names:
                    try:
                        tech = Technology.objects.get(name=tech_name)
                        project.technologies.add(tech)
                    except Technology.DoesNotExist:
                        pass
        
        # Crear testimonios si no existen
        testimonials_data = [
            {
                'name': 'Carlos Mendoza',
                'position': 'CEO',
                'company': 'TechCorp Solutions',
                'quote': 'Aplyfly transformó completamente nuestros procesos internos. Su sistema de gestión empresarial nos ayudó a aumentar la productividad en un 40%.',
                'rating': 5,
                'active': True,
                'order': 1
            },
            {
                'name': 'María González',
                'position': 'Directora de Tecnología',
                'company': 'InnovaCorp',
                'quote': 'El equipo de Aplyfly entregó una solución robusta y escalable. Su expertise en Python y Django es excepcional.',
                'rating': 5,
                'active': True,
                'order': 2
            },
            {
                'name': 'Roberto Silva',
                'position': 'Fundador',
                'company': 'StartupTech',
                'quote': 'Desde el primer día trabajaron como una extensión de nuestro equipo. Los resultados superaron todas nuestras expectativas.',
                'rating': 5,
                'active': True,
                'order': 3
            }
        ]
        
        for testimonial_data in testimonials_data:
            Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults=testimonial_data
            )
        
        # Crear categorías de proyectos para clientes
        from clients.models import ProjectCategory
        
        categories = [
            {'name': 'Desarrollo Web', 'description': 'Sitios web y aplicaciones web', 'icon': 'fas fa-globe', 'color': 'blue'},
            {'name': 'Aplicación Móvil', 'description': 'Apps iOS y Android', 'icon': 'fas fa-mobile-alt', 'color': 'purple'},
            {'name': 'E-commerce', 'description': 'Tiendas online', 'icon': 'fas fa-shopping-cart', 'color': 'emerald'},
            {'name': 'Inteligencia Artificial', 'description': 'Soluciones con IA', 'icon': 'fas fa-brain', 'color': 'cyan'},
            {'name': 'Automatización', 'description': 'Procesos y workflows', 'icon': 'fas fa-robot', 'color': 'yellow'},
            {'name': 'Dashboard/CRM', 'description': 'Sistemas de gestión', 'icon': 'fas fa-chart-line', 'color': 'orange'},
        ]
        
        for cat in categories:
            ProjectCategory.objects.get_or_create(
                name=cat['name'],
                defaults={
                    'description': cat['description'],
                    'icon': cat['icon'],
                    'color': cat['color']
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Datos poblados exitosamente para Aplyfly!')
        )
        self.stdout.write('📊 Servicios creados: {}'.format(Service.objects.count()))
        self.stdout.write('🚀 Proyectos creados: {}'.format(Project.objects.count()))
        self.stdout.write('💬 Testimonios creados: {}'.format(Testimonial.objects.count()))
        self.stdout.write('📁 Categorías de proyectos: {}'.format(ProjectCategory.objects.count()))
