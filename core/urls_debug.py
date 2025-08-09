"""
URLs de debugging para diagnosticar problemas del chat
"""
from django.urls import path
from . import views_debug

urlpatterns = [
    path('', views_debug.debug_chat_page, name='debug_chat_page'),  # Página principal de debug
    path('chat/', views_debug.chat_debug_status, name='chat_debug_status'),
    path('test-chat/', views_debug.test_chat_api, name='test_chat_api'),
    path('frontend/', views_debug.frontend_debug, name='frontend_debug'),
]
