from django.core.management.base import BaseCommand
from core.models import Service

class Command(BaseCommand):
    help = 'Poblado inicial de servicios de Aplyfly'

    def handle(self, *args, **options):
        # Limpiar servicios existentes
        Service.objects.all().delete()
        
        # Crear servicios de Aplyfly
        services_data = [
            {
                'title': 'Desarrollo de Aplicaciones y Software SaaS',
                'icon': 'fas fa-code',
                'description': 'Creamos aplicaciones web modernas y software como servicio (SaaS) escalables. Soluciones completas desde MVP hasta plataformas empresariales con tecnologías cutting-edge.',
                'order': 1
            },
            {
                'title': 'Aplicaciones Móviles',
                'icon': 'fas fa-mobile-alt',
                'description': 'Desarrollamos apps nativas para iOS y Android, así como aplicaciones multiplataforma con React Native y Flutter. Tu negocio al alcance de todos.',
                'order': 2
            },
            {
                'title': 'Sistemas Empresariales',
                'icon': 'fas fa-building',
                'description': 'Soluciones ERP y CRM personalizadas para optimizar los procesos de tu empresa. Integración con sistemas existentes y automatización inteligente.',
                'order': 3
            },
            {
                'title': 'APIs y Microservicios',
                'icon': 'fas fa-plug',
                'description': 'Arquitecturas robustas y escalables. Diseñamos APIs RESTful y GraphQL, microservicios con Docker y orquestación con Kubernetes.',
                'order': 4
            },
            {
                'title': 'Cloud Computing',
                'icon': 'fas fa-cloud',
                'description': 'Migración y optimización en la nube con AWS, Azure y Google Cloud. Infraestructura como código, CI/CD y monitoreo avanzado.',
                'order': 5
            },
            {
                'title': 'Arquitectura de Software con IA',
                'icon': 'fas fa-brain',
                'description': 'Potenciamos tu negocio con arquitecturas inteligentes. Integración de IA, machine learning, automatización y chatbots para transformar procesos empresariales.',
                'order': 6
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Servicio creado: {service.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Servicio ya existe: {service.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('¡Servicios de Aplyfly poblados exitosamente!')
        )
