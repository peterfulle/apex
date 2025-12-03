from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json
import asyncio
from .models import Service
from .forms import ContactForm
from portfolio.models import Project
from .ai_agent import aplyfly_agent

class IndexView(TemplateView):
    template_name = 'core/index_modern.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
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

def servicios_ia_view(request):
    """Vista para la página de servicios de IA"""
    return render(request, 'core/servicios_ia.html')

# ============ VISTAS DEL CHAT IA ============

@csrf_exempt
@require_http_methods(["POST"])
def chat_api_view(request):
    """
    API endpoint para el chat con IA
    Maneja tanto respuestas normales como streaming
    """
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        history = data.get('history', [])
        streaming = data.get('streaming', False)
        
        if not message:
            return JsonResponse({'error': 'Mensaje requerido'}, status=400)
        
        if streaming:
            # Respuesta streaming
            def stream_response():
                try:
                    # Crear event loop para async
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    async def get_streaming_response():
                        async for chunk in aplyfly_agent.get_chat_response(message, history):
                            yield f"data: {json.dumps({'type': 'content', 'chunk': chunk})}\n\n"
                        yield f"data: {json.dumps({'type': 'end'})}\n\n"
                    
                    # Ejecutar la función async
                    async_gen = get_streaming_response()
                    
                    try:
                        while True:
                            chunk = loop.run_until_complete(async_gen.__anext__())
                            yield chunk
                    except StopAsyncIteration:
                        pass
                    finally:
                        loop.close()
                        
                except Exception as e:
                    yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
            
            response = StreamingHttpResponse(
                stream_response(),
                content_type='text/event-stream'
            )
            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'
            return response
        
        else:
            # Respuesta normal
            response = aplyfly_agent.get_response_sync(message, history)
            return JsonResponse({
                'response': response,
                'status': 'success'
            })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@require_http_methods(["GET"])
def chat_test_view(request):
    """
    Endpoint de test para verificar que el chat funciona
    """
    return JsonResponse({
        'status': 'active',
        'agent': 'AplyBot',
        'version': '1.0',
        'services': ['web', 'ia', 'mobile', 'api', 'consulting'],
        'message': '🤖 Chat IA funcionando correctamente'
    })
