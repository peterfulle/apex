from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from .models import Service, Testimonial
from .forms import ContactForm
from portfolio.models import Project

class IndexView(TemplateView):
    template_name = 'core/index_aplyfly.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['testimonials'] = Testimonial.objects.filter(active=True)
        context['featured_projects'] = Project.objects.filter(featured=True)[:3]
        context['form'] = ContactForm()
        context['current_year'] = datetime.now().year
        return context

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'core/contact_success.html'
    
    def form_valid(self, form):
        # Guardar el mensaje
        form.save()
        
        if self.request.htmx:
            return HttpResponse(
                '<div class="p-4 mb-4 text-green-800 bg-green-100 rounded-lg">'
                'Gracias por tu mensaje. Te contactaremos pronto.'
                '</div>',
                headers={'HX-Trigger': 'contactFormSubmitted'}
            )
        
        # En lugar de redireccionar, renderizar la página de éxito
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        if self.request.htmx:
            return HttpResponse(
                '<div class="p-4 mb-4 text-red-800 bg-red-100 rounded-lg">'
                'Por favor corrige los errores en el formulario.'
                '</div>' + form.as_p(),
                status=400
            )
        
        return super().form_invalid(form)
        
        return super().form_invalid(form)

def services_view(request):
    """Vista para la página de servicios con branding Aplyfly"""
    services = Service.objects.all()
    return render(request, 'core/services_aplyfly.html', {'services': services})
