from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # Authentication URLs
    path('login/', views.client_login, name='login'),
    path('register/', views.client_register, name='register'),
    path('logout/', views.client_logout, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='index'),  # Redirect root to dashboard
    
    # Project URLs
    path('projects/', views.projects_list, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<uuid:pk>/', views.project_detail, name='project_detail'),
    path('projects/<uuid:pk>/message/', views.send_message, name='send_message'),
    
    # Service Request URLs
    path('requests/', views.service_requests_list, name='service_requests'),
    path('requests/create/', views.service_request_create, name='service_request_create'),
    path('requests/<uuid:pk>/', views.service_request_detail, name='service_request_detail'),
    
    # Notification URLs
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='notification_read'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/remove-avatar/', views.remove_avatar, name='remove_avatar'),
    
    # API URLs for AJAX
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
]
