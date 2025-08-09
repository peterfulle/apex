#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
django.setup()

from core.models import Service

# Crear servicios modernos
services_data = [
    {
        'title': 'Desarrollo de Aplicaciones y Software SaaS',
        'icon': 'fas fa-code',
        'description': 'Aplicaciones web modernas y software como servicio (SaaS) escalables. Soluciones completas desde MVP hasta plataformas empresariales con tecnologías cutting-edge.',
        'order': 1
    },
    {
        'title': 'Sistemas Empresariales',
        'icon': 'fas fa-building',
        'description': 'Soluciones empresariales completas: CRM, ERP, sistemas de gestión y automatización de procesos. Integraciones seamless con APIs y servicios existentes.',
        'order': 2
    },
    {
        'title': 'Inteligencia Artificial',
        'icon': 'fas fa-robot',
        'description': 'Integración de IA generativa, chatbots inteligentes, análisis de datos con ML y automatización inteligente usando OpenAI, Claude y modelos personalizados.',
        'order': 3
    },
    {
        'title': 'Aplicaciones Móviles',
        'icon': 'fas fa-mobile-alt',
        'description': 'Apps nativas y multiplataforma con React Native y Flutter. Experiencias móviles fluidas, sincronización en tiempo real y diseño centrado en el usuario.',
        'order': 4
    },
    {
        'title': 'APIs & Microservicios',
        'icon': 'fas fa-network-wired',
        'description': 'Arquitecturas de microservicios robustas, APIs RESTful y GraphQL escalables. Sistemas distribuidos con Docker, Kubernetes y cloud-native technologies.',
        'order': 5
    },
    {
        'title': 'Arquitectura de Software con IA',
        'icon': 'fas fa-brain',
        'description': 'Potenciamos tu negocio con arquitecturas inteligentes. Integración de IA, machine learning, automatización y chatbots para transformar procesos empresariales.',
        'order': 6
    }
]

# Limpiar servicios existentes
Service.objects.all().delete()
print("🗑️  Servicios anteriores eliminados")

# Crear nuevos servicios
created_services = []
for service_data in services_data:
    service = Service.objects.create(**service_data)
    created_services.append(service)
    print(f"✅ Creado: {service.title}")

print(f"\n🎉 Se crearon {len(created_services)} servicios modernos!")
print("🚀 Los servicios ya deberían aparecer en tu aplicación")