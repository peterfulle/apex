"""
API de debugging simple y robusta
"""
import os
import sys
import json
import traceback
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


def simple_debug_status(request):
    """
    API de debugging ultra simple que siempre funciona
    """
    try:
        debug_info = {
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "basic_checks": {},
            "errors": []
        }
        
        # Verificaciones básicas que siempre funcionan
        debug_info["basic_checks"]["python_version"] = sys.version.split()[0]
        debug_info["basic_checks"]["environment"] = os.environ.get('ENV', 'unknown')
        
        # Verificar Django de forma segura
        try:
            import django
            debug_info["basic_checks"]["django_version"] = django.get_version()
            debug_info["basic_checks"]["django_imported"] = True
        except Exception as e:
            debug_info["basic_checks"]["django_imported"] = False
            debug_info["errors"].append(f"Django import error: {str(e)}")
        
        # Verificar settings de forma segura
        try:
            from django.conf import settings
            debug_info["basic_checks"]["settings_loaded"] = True
            debug_info["basic_checks"]["debug_mode"] = getattr(settings, 'DEBUG', 'unknown')
        except Exception as e:
            debug_info["basic_checks"]["settings_loaded"] = False
            debug_info["errors"].append(f"Settings error: {str(e)}")
        
        # Verificar OpenAI de forma ultra segura
        openai_status = {"status": "checking"}
        try:
            from core.ai_agent import AplyflyChatAgent
            openai_status["agent_import"] = True
            
            try:
                agent = AplyflyChatAgent()
                openai_status["agent_created"] = True
                
                if hasattr(agent, '_init_error') and agent._init_error:
                    openai_status["init_error"] = str(agent._init_error)
                    openai_status["status"] = "error"
                else:
                    openai_status["status"] = "ok"
                    
            except Exception as e:
                openai_status["agent_created"] = False
                openai_status["creation_error"] = str(e)
                openai_status["status"] = "creation_failed"
                
        except Exception as e:
            openai_status["agent_import"] = False
            openai_status["import_error"] = str(e)
            openai_status["status"] = "import_failed"
        
        debug_info["basic_checks"]["openai"] = openai_status
        
        # Verificar base de datos de forma ultra segura
        db_status = {"status": "checking"}
        try:
            from django.db import connection
            db_status["connection_import"] = True
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    db_status["connected"] = True
                    db_status["status"] = "connected"
            except Exception as e:
                db_status["connected"] = False
                db_status["connection_error"] = str(e)
                db_status["status"] = "connection_failed"
                
        except Exception as e:
            db_status["connection_import"] = False
            db_status["import_error"] = str(e)
            db_status["status"] = "import_failed"
        
        debug_info["basic_checks"]["database"] = db_status
        
        # Estado general
        if debug_info["errors"]:
            debug_info["status"] = "degraded"
            debug_info["summary"] = f"Sistema funcionando con {len(debug_info['errors'])} errores"
        else:
            debug_info["status"] = "healthy"
            debug_info["summary"] = "Verificaciones básicas pasaron correctamente"
        
        return JsonResponse(debug_info)
        
    except Exception as e:
        # Fallback extremo
        return JsonResponse({
            "status": "critical_error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "error_type": type(e).__name__,
            "message": "Error crítico en sistema de debug"
        }, status=500)


@csrf_exempt
def simple_test_chat(request):
    """
    Test simple del chat
    """
    try:
        if request.method == "GET":
            return JsonResponse({
                "status": "ready",
                "message": "Simple chat test endpoint ready",
                "timestamp": datetime.now().isoformat()
            })
        
        # POST
        try:
            data = json.loads(request.body)
            message = data.get('message', 'test')
        except:
            message = "test"
        
        # Intentar el chat de forma simple
        try:
            from core.ai_agent import AplyflyChatAgent
            agent = AplyflyChatAgent()
            
            if hasattr(agent, '_init_error') and agent._init_error:
                return JsonResponse({
                    "status": "fallback",
                    "message": message,
                    "response": f"Mensaje recibido: '{message}'. Sistema de IA temporalmente no disponible. Contacta info@aplyfly.com",
                    "ai_error": str(agent._init_error),
                    "timestamp": datetime.now().isoformat()
                })
            
            # Intentar respuesta real
            response = agent.get_response(message)
            return JsonResponse({
                "status": "success",
                "message": message,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "fallback",
                "message": message,
                "response": f"Mensaje recibido: '{message}'. Error técnico temporal. Contacta info@aplyfly.com",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, status=500)
