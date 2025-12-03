from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from clients.models import Project, ServiceRequest, CustomUser, ProjectAttachment
from decimal import Decimal

def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def admin_required(view_func):
    """Decorator that checks if user is admin and redirects to admin login"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/administrador/login/?next=' + request.path)
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'No tienes permisos de administrador.')
            return redirect('/administrador/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Intentar autenticar con username
        user = authenticate(request, username=username, password=password)
        
        # Si no funciona, intentar con email
        if user is None:
            try:
                user_obj = CustomUser.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                next_url = request.GET.get('next', 'admin_panel:dashboard')
                if next_url.startswith('/'):
                    return redirect(next_url)
                return redirect(next_url)
            else:
                messages.error(request, 'No tienes permisos de administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'admin/login.html')


@admin_required
def admin_dashboard(request):
    """Admin dashboard overview"""
    # Stats
    total_projects = Project.objects.count()
    pending_projects = Project.objects.filter(status='submitted').count()
    active_projects = Project.objects.filter(status__in=['in_review', 'approved', 'in_development', 'testing']).count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    total_clients = CustomUser.objects.filter(is_client=True).count()
    total_requests = ServiceRequest.objects.count()
    pending_requests = ServiceRequest.objects.filter(status='pending').count()
    
    # Recent projects
    recent_projects = Project.objects.select_related('client', 'category').order_by('-created_at')[:5]
    
    # Recent clients
    recent_clients = CustomUser.objects.filter(is_client=True).order_by('-date_joined')[:5]
    
    context = {
        'total_projects': total_projects,
        'pending_projects': pending_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_clients': total_clients,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'recent_projects': recent_projects,
        'recent_clients': recent_clients,
    }
    
    return render(request, 'admin/dashboard.html', context)


@admin_required
def admin_projects_list(request):
    """List all projects for admin"""
    projects = Project.objects.select_related('client', 'category').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        projects = projects.filter(priority=priority_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(client__email__icontains=search_query) |
            Q(client__first_name__icontains=search_query) |
            Q(client__last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Project.PROJECT_STATUS_CHOICES,
        'priority_choices': Project.PRIORITY_CHOICES,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/projects/list.html', context)


@admin_required
def admin_project_detail(request, pk):
    """Project detail view for admin"""
    project = get_object_or_404(Project.objects.select_related('client', 'category'), pk=pk)
    attachments = ProjectAttachment.objects.filter(project=project)
    
    context = {
        'project': project,
        'attachments': attachments,
    }
    
    return render(request, 'admin/projects/detail.html', context)


@admin_required
def admin_project_update_status(request, pk):
    """Update project status"""
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status in dict(Project.PROJECT_STATUS_CHOICES):
            project.status = new_status
            project.save()
            messages.success(request, f'Estado del proyecto actualizado a: {project.get_status_display()}')
        else:
            messages.error(request, 'Estado inválido')
    
    return redirect('admin:project_detail', pk=pk)


@admin_required
def admin_project_add_quote(request, pk):
    """Add quote to project"""
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        
        quote_amount = request.POST.get('quote_amount')
        quote_description = request.POST.get('quote_description')
        quote_file = request.FILES.get('quote_file')
        
        # Aquí puedes crear un modelo Quote o guardarlo en el proyecto
        # Por ahora lo guardamos en special_notes
        quote_text = f"\n\n--- COTIZACIÓN ---\nMonto: ${quote_amount}\nDescripción: {quote_description}\nFecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n"
        
        if project.special_notes:
            project.special_notes += quote_text
        else:
            project.special_notes = quote_text
        
        project.status = 'in_review'
        project.save()
        
        messages.success(request, 'Cotización agregada exitosamente')
    
    return redirect('admin:project_detail', pk=pk)


@admin_required
def admin_clients_list(request):
    """List all clients"""
    clients = CustomUser.objects.filter(is_client=True).annotate(
        projects_count=Count('projects')
    ).order_by('-date_joined')
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        clients = clients.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(clients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/clients/list.html', context)


@admin_required
def admin_client_detail(request, pk):
    """Client detail view"""
    client = get_object_or_404(CustomUser, pk=pk, is_client=True)
    projects = Project.objects.filter(client=client).order_by('-created_at')
    
    context = {
        'client': client,
        'projects': projects,
    }
    
    return render(request, 'admin/clients/detail.html', context)
