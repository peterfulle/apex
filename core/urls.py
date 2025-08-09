from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('servicios/', views.services_view, name='services'),
    path('servicios-ia/', views.servicios_ia_view, name='servicios_ia'),
    path('contacto/', views.ContactFormView.as_view(), name='contact'),
    
    # URLs del Chat IA
    path('api/chat/', views.chat_api_view, name='chat_api'),
    path('api/chat/test/', views.chat_test_view, name='chat_test'),
]
