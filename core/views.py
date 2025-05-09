from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .forms import ContactForm
from .models import Service, Testimonial

class IndexView(TemplateView):
    template_name = 'core/index.html'  # o 'core/index.html' dependiendo de tu estructura
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['testimonials'] = Testimonial.objects.filter(active=True)
        # Eliminamos la referencia a featured_projects
        context['contact_form'] = ContactForm()
        return context


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<div class="p-4 rounded-lg bg-gradient-to-r from-accent-primary/20 to-accent-secondary/20 border border-accent-primary/30">'
                '<p class="text-white"><i class="fa-solid fa-check-circle mr-2 text-accent-primary"></i> '
                'Your message has been sent successfully. We will get back to you shortly.</p>'
                '</div>'
            )
        else:
            return HttpResponse(
                '<div class="p-4 rounded-lg bg-red-500/20 border border-red-500/30">'
                '<p class="text-white"><i class="fa-solid fa-exclamation-circle mr-2 text-red-400"></i> '
                'There was an error with your submission. Please check the form and try again.</p>'
                '</div>'
            )
    
    return HttpResponse('Method not allowed', status=405)