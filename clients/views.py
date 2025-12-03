from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from datetime import timedelta
import json

from .models import (
    CustomUser, Project, ProjectCategory, ServiceRequest, 
    ClientNotification, ProjectUpdate, ProjectMessage
)
from .forms import (
    ClientRegistrationForm, ProjectCreateForm, ServiceRequestForm,
    ProjectMessageForm, UserProfileForm
)

def client_login(request):
    """Client login view"""
    if request.user.is_authenticated:
        return redirect('clients:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_client:
                login(request, user)
                messages.success(request, f'¡Bienvenido de vuelta, {user.get_full_name()}!')
                return redirect('clients:dashboard')
            else:
                messages.error(request, 'Credenciales inválidas o acceso no autorizado.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'clients/auth/login.html', {'form': form})

def client_register(request):
    """Client registration view"""
    if request.user.is_authenticated:
        return redirect('clients:dashboard')
    
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('clients:login')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'clients/auth/register.html', {'form': form})

@login_required
def client_logout(request):
    """Client logout view"""
    logout(request)
    messages.success(request, '¡Hasta luego! Has cerrado sesión exitosamente.')
    return redirect('index')

@login_required
def dashboard(request):
    """Main dashboard view"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    # Get dashboard statistics
    total_projects = Project.objects.filter(client=request.user).count()
    active_projects = Project.objects.filter(
        client=request.user, 
        status__in=['approved', 'in_development', 'testing']
    ).count()
    completed_projects = Project.objects.filter(
        client=request.user, 
        status='completed'
    ).count()
    pending_requests = ServiceRequest.objects.filter(
        client=request.user, 
        status__in=['pending', 'in_review']
    ).count()
    
    # Recent projects
    recent_projects = Project.objects.filter(client=request.user)[:5]
    
    # Recent service requests
    recent_requests = ServiceRequest.objects.filter(client=request.user)[:5]
    
    # Recent notifications
    notifications = ClientNotification.objects.filter(
        client=request.user, 
        is_read=False
    )[:5]
    
    # Project status distribution
    project_status_data = list(
        Project.objects.filter(client=request.user)
        .values('status')
        .annotate(count=Count('status'))
    )
    
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'pending_requests': pending_requests,
        'recent_projects': recent_projects,
        'recent_requests': recent_requests,
        'notifications': notifications,
        'project_status_data': json.dumps(project_status_data),
    }
    
    return render(request, 'clients/dashboard/dashboard.html', context)

@login_required
def projects_list(request):
    """List all client projects"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    projects = Project.objects.filter(client=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Project.PROJECT_STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'clients/projects/list.html', context)

@login_required
def project_detail(request, pk):
    """Project detail view"""
    project = get_object_or_404(Project, pk=pk, client=request.user)
    
    # Get project updates
    updates = ProjectUpdate.objects.filter(project=project)[:10]
    
    # Get project messages
    messages_list = ProjectMessage.objects.filter(project=project)[:20]
    
    # Mark project messages as read
    ProjectMessage.objects.filter(
        project=project, 
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Message form
    message_form = ProjectMessageForm()
    
    context = {
        'project': project,
        'updates': updates,
        'messages': messages_list,
        'message_form': message_form,
    }
    
    return render(request, 'clients/projects/detail.html', context)

@login_required
def project_create(request):
    """Create new project"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            
            # Build budget_range from min/max
            budget_min = request.POST.get('budget_min')
            budget_max = request.POST.get('budget_max')
            if budget_min and budget_max:
                project.budget_min = budget_min
                project.budget_max = budget_max
                project.budget_range = f"${budget_min} - ${budget_max}"
            
            # Save additional fields
            project.requirements = request.POST.get('requirements', '')
            project.reference_urls = request.POST.get('reference_urls', '')
            project.special_notes = request.POST.get('special_notes', '')
            project.status = 'submitted'  # Mark as submitted instead of draft
            
            project.save()
            form.save_m2m()
            
            # Handle multiple attachments
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                from .models import ProjectAttachment
                ProjectAttachment.objects.create(
                    project=project,
                    file=attachment,
                    file_name=attachment.name,
                    file_type=attachment.content_type,
                    file_size=attachment.size,
                    uploaded_by=request.user
                )
            
            messages.success(request, '¡Proyecto enviado exitosamente! Te contactaremos pronto.')
            return redirect('clients:project_detail', pk=project.pk)
    else:
        form = ProjectCreateForm()
    
    # Get categories for the template
    from .models import ProjectCategory
    categories = ProjectCategory.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'clients/projects/create.html', context)

@login_required
def service_requests_list(request):
    """List all service requests"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    requests = ServiceRequest.objects.filter(client=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    # Filter by service type
    service_filter = request.GET.get('service_type')
    if service_filter:
        requests = requests.filter(service_type=service_filter)
    
    # Pagination
    paginator = Paginator(requests, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': ServiceRequest.STATUS_CHOICES,
        'service_choices': ServiceRequest.SERVICE_TYPES,
        'current_status': status_filter,
        'current_service': service_filter,
    }
    
    return render(request, 'clients/requests/list.html', context)

@login_required
def service_request_create(request):
    """Create new service request"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.client = request.user
            service_request.save()
            
            messages.success(request, 'Solicitud de servicio enviada exitosamente!')
            return redirect('clients:service_requests')
    else:
        form = ServiceRequestForm()
    
    context = {'form': form}
    return render(request, 'clients/requests/create.html', context)

@login_required
def service_request_detail(request, pk):
    """Service request detail view"""
    service_request = get_object_or_404(ServiceRequest, pk=pk, client=request.user)
    
    context = {'service_request': service_request}
    return render(request, 'clients/requests/detail.html', context)

@login_required
def notifications_list(request):
    """List all notifications"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    notifications = ClientNotification.objects.filter(client=request.user)
    
    # Mark as read
    if request.GET.get('mark_read') == 'all':
        notifications.update(is_read=True)
        messages.success(request, 'Todas las notificaciones marcadas como leídas.')
        return redirect('clients:notifications')
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'clients/notifications/list.html', context)

@login_required
def profile_view(request):
    """User profile view and edit"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    if request.method == 'POST':
        # Handle avatar upload separately
        if 'avatar' in request.FILES:
            user = request.user
            # Delete old avatar if exists
            if user.avatar:
                user.avatar.delete()
            user.avatar = request.FILES['avatar']
            user.save()
            messages.success(request, '¡Foto de perfil actualizada exitosamente!')
            return redirect('clients:profile')
        
        # Handle profile form
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente!')
            return redirect('clients:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Get user statistics
    total_projects = Project.objects.filter(client=request.user).count()
    total_requests = ServiceRequest.objects.filter(client=request.user).count()
    completed_projects = Project.objects.filter(
        client=request.user, 
        status='completed'
    ).count()
    
    context = {
        'form': form,
        'total_projects': total_projects,
        'total_requests': total_requests,
        'completed_projects': completed_projects,
    }
    return render(request, 'clients/profile/profile.html', context)

@login_required
@require_http_methods(["POST"])
def send_message(request, project_pk):
    """Send message to project"""
    project = get_object_or_404(Project, pk=project_pk, client=request.user)
    
    form = ProjectMessageForm(request.POST, request.FILES)
    if form.is_valid():
        message = form.save(commit=False)
        message.project = project
        message.sender = request.user
        message.save()
        
        messages.success(request, 'Mensaje enviado exitosamente!')
    else:
        messages.error(request, 'Error al enviar el mensaje.')
    
    return redirect('clients:project_detail', pk=project_pk)

@login_required
def mark_notification_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(ClientNotification, pk=pk, client=request.user)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'status': 'success'})

@login_required
def change_password(request):
    """Change user password"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    if request.method == 'POST':
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            messages.success(request, '¡Contraseña cambiada exitosamente!')
            return redirect('clients:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('clients:profile')

@login_required
def remove_avatar(request):
    """Remove user avatar"""
    if not request.user.is_client:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index')
    
    if request.method == 'POST':
        user = request.user
        if user.avatar:
            user.avatar.delete()
            user.save()
            messages.success(request, '¡Foto de perfil eliminada exitosamente!')
        else:
            messages.info(request, 'No tienes foto de perfil.')
    
    return redirect('clients:profile')

# API Views for AJAX requests
@login_required
def api_dashboard_stats(request):
    """API endpoint for dashboard statistics"""
    if not request.user.is_client:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    stats = {
        'total_projects': Project.objects.filter(client=request.user).count(),
        'active_projects': Project.objects.filter(
            client=request.user, 
            status__in=['approved', 'in_development', 'testing']
        ).count(),
        'completed_projects': Project.objects.filter(
            client=request.user, 
            status='completed'
        ).count(),
        'unread_notifications': ClientNotification.objects.filter(
            client=request.user, 
            is_read=False
        ).count(),
    }
    
    return JsonResponse(stats)
