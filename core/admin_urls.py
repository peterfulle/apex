from django.urls import path
from . import admin_views

app_name = 'admin_panel'

urlpatterns = [
    # Login
    path('login/', admin_views.admin_login, name='login'),
    
    # Dashboard
    path('', admin_views.admin_dashboard, name='dashboard'),
    
    # Projects
    path('projects/', admin_views.admin_projects_list, name='projects'),
    path('projects/<uuid:pk>/', admin_views.admin_project_detail, name='project_detail'),
    path('projects/<uuid:pk>/update-status/', admin_views.admin_project_update_status, name='project_update_status'),
    path('projects/<uuid:pk>/add-quote/', admin_views.admin_project_add_quote, name='project_add_quote'),
    
    # Clients
    path('clients/', admin_views.admin_clients_list, name='clients'),
    path('clients/<int:pk>/', admin_views.admin_client_detail, name='client_detail'),
]
