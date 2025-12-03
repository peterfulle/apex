"""
API de debugging para diagnosticar problemas del chatbot y la aplicación
"""
import os
import sys
import django
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json
import traceback
from datetime import datetime


def debug_chat_page(request):
    """
    Página web de debugging para el chat
    """
    return render(request, 'debug_chat.html')


def chat_debug_status(request):
    """
    API para diagnosticar el estado del chatbot y la aplicación
    """
    try:
        debug_info = {
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "environment": {
                "python_version": sys.version,
                "django_version": django.get_version(),
                "debug_mode": settings.DEBUG,
                "environment": os.environ.get('ENV', 'unknown'),
            },
            "openai_status": {},
            "database_status": {},
            "static_files": {},
            "chat_endpoints": {},
            "errors": []
        }
        
        # Verificar OpenAI
        try:
            from core.ai_agent import AplyflyChatAgent
            agent = AplyflyChatAgent()
            debug_info["openai_status"] = {
                "client_initialized": hasattr(agent, 'client') and agent.client is not None,
                "azure_endpoint": os.environ.get('AZURE_OPENAI_ENDPOINT', 'NOT_SET'),
                "deployment_name": os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME', 'NOT_SET'),
                "api_version": os.environ.get('AZURE_OPENAI_API_VERSION', 'NOT_SET'),
                "has_api_key": bool(os.environ.get('AZURE_OPENAI_API_KEY')),
                "init_error": getattr(agent, '_init_error', None),
                "client_status": "connected" if (hasattr(agent, 'client') and agent.client is not None) else "disconnected"
            }
        except ImportError as ie:
            debug_info["openai_status"] = {
                "error": f"Import error: {str(ie)}",
                "client_status": "module_not_found"
            }
            debug_info["errors"].append(f"OpenAI Import Error: {str(ie)}")
        except Exception as e:
            debug_info["openai_status"] = {
                "error": str(e),
                "traceback": traceback.format_exc(),
                "client_status": "error"
            }
            debug_info["errors"].append(f"OpenAI Error: {str(e)}")
        
        # Verificar base de datos
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                debug_info["database_status"] = {
                    "connected": True,
                    "engine": settings.DATABASES['default']['ENGINE'],
                    "name": settings.DATABASES['default']['NAME']
                }
                
                # Verificar tablas importantes
                try:
                    cursor.execute("SELECT COUNT(*) FROM clients_customuser")
                    user_count = cursor.fetchone()[0]
                    debug_info["database_status"]["user_count"] = user_count
                except Exception as e:
                    debug_info["database_status"]["user_table_error"] = str(e)
                    debug_info["errors"].append(f"User table error: {str(e)}")
                
                try:
                    cursor.execute("SELECT COUNT(*) FROM core_contactmessage")
                    message_count = cursor.fetchone()[0]
                    debug_info["database_status"]["message_count"] = message_count
                except Exception as e:
                    debug_info["database_status"]["message_table_error"] = str(e)
                    debug_info["errors"].append(f"Message table error: {str(e)}")
                    
        except Exception as e:
            debug_info["database_status"] = {
                "connected": False,
                "error": str(e)
            }
            debug_info["errors"].append(f"Database Error: {str(e)}")
        
        # Verificar archivos estáticos
        try:
            import os
            static_root = getattr(settings, 'STATIC_ROOT', None)
            static_files_info = {
                "static_root": static_root,
                "static_url": getattr(settings, 'STATIC_URL', '/static/'),
                "exists": False,
                "files": {}
            }
            
            if static_root:
                static_files_info["exists"] = os.path.exists(static_root)
                if static_files_info["exists"]:
                    # Verificar archivos críticos
                    critical_files = {
                        "chat_js": os.path.join(static_root, 'js', 'chat_widget.js'),
                        "ai_png": os.path.join(static_root, 'images', 'ai.png'),
                        "css_main": os.path.join(static_root, 'css', 'style.css'),
                    }
                    
                    for file_key, file_path in critical_files.items():
                        try:
                            static_files_info["files"][file_key] = {
                                "exists": os.path.exists(file_path),
                                "path": file_path
                            }
                        except Exception as file_e:
                            static_files_info["files"][file_key] = {
                                "exists": False,
                                "error": str(file_e)
                            }
                else:
                    debug_info["errors"].append(f"STATIC_ROOT directory does not exist: {static_root}")
            else:
                debug_info["errors"].append("STATIC_ROOT not configured")
            
            debug_info["static_files"] = static_files_info
            
        except Exception as e:
            debug_info["static_files"] = {
                "error": str(e),
                "static_root": "unknown",
                "exists": False
            }
            debug_info["errors"].append(f"Static files check error: {str(e)}")
        
        # Verificar endpoints del chat
        try:
            from django.urls import reverse
            debug_info["chat_endpoints"] = {
                "chat_api_url": "/api/chat/",
                "debug_url": "/api/debug/chat/",
            }
        except Exception as e:
            debug_info["chat_endpoints"] = {"error": str(e)}
        
        # Estado general
        if debug_info["errors"]:
            debug_info["status"] = "degraded"
            debug_info["summary"] = f"Sistema funcionando con {len(debug_info['errors'])} errores"
        else:
            debug_info["summary"] = "Sistema funcionando correctamente"
        
        return JsonResponse(debug_info, indent=2)
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status=500, indent=2)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def test_chat_api(request):
    """
    Endpoint para probar la funcionalidad del chat directamente
    """
    try:
        if request.method == "GET":
            return JsonResponse({
                "status": "ready",
                "message": "Chat API test endpoint. Send POST with 'message' to test.",
                "example": {
                    "method": "POST",
                    "body": {"message": "Hola, ¿cómo están?"}
                }
            })
        
        # POST request
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON",
                "received": request.body.decode('utf-8')[:100]
            }, status=400)
        
        message = data.get('message', '')
        if not message:
            return JsonResponse({
                "error": "No message provided",
                "required": "message"
            }, status=400)
        
        # Intentar procesar con el agente de IA
        try:
            from core.ai_agent import AplyflyChatAgent
            agent = AplyflyChatAgent()
            
            # Verificar si el agente está funcionando
            if hasattr(agent, '_init_error'):
                return JsonResponse({
                    "status": "degraded",
                    "message": "OpenAI no disponible",
                    "response": f"Gracias por tu mensaje: '{message}'. Actualmente tenemos problemas técnicos con nuestro asistente de IA, pero puedes contactarnos directamente a info@aplyfly.com para asistencia inmediata.",
                    "openai_error": agent._init_error,
                    "fallback_mode": True
                })
            
            # Intentar generar respuesta
            response = agent.get_response(message)
            return JsonResponse({
                "status": "success",
                "message": message,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "openai_working": True
            })
            
        except Exception as ai_error:
            return JsonResponse({
                "status": "fallback",
                "message": message,
                "response": f"Recibimos tu mensaje: '{message}'. Nuestro sistema de IA está temporalmente no disponible, pero nuestro equipo estará encantado de ayudarte. Contáctanos directamente a info@aplyfly.com",
                "ai_error": str(ai_error),
                "timestamp": datetime.now().isoformat(),
                "openai_working": False
            })
            
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }, status=500)


def frontend_debug(request):
    """
    Información de debugging para el frontend
    """
    try:
        return JsonResponse({
            "status": "ready",
            "timestamp": datetime.now().isoformat(),
            "chat_widget": {
                "template_path": "templates/chat_widget.html",
                "javascript_path": "static/js/chat_widget.js",
                "css_framework": "TailwindCSS",
                "icons": "FontAwesome",
            },
            "api_endpoints": {
                "chat": "/api/chat/",
                "debug_status": "/api/debug/chat/",
                "test_chat": "/api/debug/test-chat/",
                "frontend_debug": "/api/debug/frontend/"
            },
            "javascript_config": {
                "chat_widget_id": "aplyfly-chat-widget",
                "toggle_button_id": "chat-toggle-btn",
                "chat_window_id": "chat-window",
                "message_container_id": "chat-messages",
                "input_id": "chat-input",
                "send_button_id": "send-btn"
            },
            "troubleshooting": {
                "common_issues": [
                    "Verificar que el JavaScript se está cargando",
                    "Comprobar errores en la consola del navegador",
                    "Verificar que los IDs de elementos coinciden",
                    "Comprobar que TailwindCSS está disponible",
                    "Verificar conectividad con el endpoint /api/chat/"
                ]
            }
        }, indent=2)
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status=500)
