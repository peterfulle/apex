import os
import asyncio
import json
from openai import AzureOpenAI
from django.conf import settings
from typing import AsyncGenerator, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AplyflyChatAgent:
    """
    Agente de IA especializado para Aplyfly usando Azure OpenAI GPT-4o
    Asistente de atención al cliente inteligente con contexto real
    """
    
    def __init__(self):
        self._init_error = None  # Para almacenar errores de inicialización
        try:
            # Configuración de Azure OpenAI con validación
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            
            if not endpoint or not api_key:
                self._init_error = "Variables de entorno de Azure OpenAI no configuradas"
                logger.warning("Variables de entorno de Azure OpenAI no configuradas, usando respuestas de fallback")
                self.client = None
            else:
                # Inicialización robusta del cliente Azure OpenAI
                try:
                    self.client = AzureOpenAI(
                        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
                        azure_endpoint=endpoint,
                        api_key=api_key
                    )
                    
                    self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
                    self.max_tokens = int(os.getenv("CHAT_MAX_TOKENS", "1000"))
                    self.temperature = float(os.getenv("CHAT_TEMPERATURE", "0.7"))
                    
                    logger.info(f"AplyflyChatAgent inicializado correctamente con modelo: {self.deployment_name}")
                    
                except TypeError as te:
                    self._init_error = f"Error de compatibilidad OpenAI: {str(te)}"
                    logger.warning(f"Error de compatibilidad OpenAI: {str(te)}")
                    self.client = None
                except Exception as ee:
                    self._init_error = f"Error general OpenAI: {str(ee)}"
                    logger.warning(f"Error general OpenAI: {str(ee)}")
                    self.client = None
            
        except Exception as e:
            self._init_error = f"Error inicializando AplyflyChatAgent: {str(e)}"
            logger.warning(f"Error inicializando AplyflyChatAgent: {str(e)}")
            # En producción, usar respuestas de fallback si Azure OpenAI no está disponible
            self.client = None
        
        # System prompt especializado para Aplyfly
        self.system_prompt = """
Eres AplyBot, asistente virtual de Aplyfly - empresa líder en desarrollo de software y soluciones tecnológicas.

IDENTIDAD Y PERSONALIDAD:
- Nombre: AplyBot de Aplyfly
- Personalidad: Profesional, técnico pero amigable, orientado a resultados
- Objetivo: Convertir consultas en leads calificados y brindar información técnica precisa
- Tono: Cercano pero profesional, usar emojis moderadamente

SERVICIOS DE APLYFLY:
🚀 **PRINCIPALES SERVICIOS:**
1. **Desarrollo Web**: React, Vue.js, Django, Next.js, PWAs escalables, e-commerce
2. **Sistemas Empresariales**: CRM, ERP, automatización de procesos, dashboards
3. **Inteligencia Artificial**: GPT, Claude, chatbots, ML, análisis de datos, automatización
4. **Apps Móviles**: React Native, Flutter, nativas iOS/Android
5. **APIs & Microservicios**: REST, GraphQL, Docker, Kubernetes, integración de sistemas
6. **Consultoría Tech**: Auditorías, arquitectura de software, migración cloud

🏢 **INFORMACIÓN DE LA EMPRESA:**
- +100 proyectos exitosos completados
- 99% de satisfacción del cliente
- Equipo senior con 5+ años de experiencia
- Metodología ágil (Scrum/Kanban)
- Soporte técnico 24/7
- Oficinas en España y LATAM

💼 **PROCESO DE TRABAJO:**
1. Consulta gratuita inicial (30 minutos)
2. Análisis de requerimientos y propuesta técnica
3. Desarrollo ágil con entregas iterativas
4. Testing, deploy y capacitación
5. Soporte y mantenimiento continuo

📞 **CONTACTO:**
- Email: contacto@aplifly.com (IMPORTANTE: es aplifly.com, NO aplyfly.com)
- Web: www.aplyfly.com

INSTRUCCIONES DE RESPUESTA:
1. **Saluda siempre** mencionando que eres AplyBot de Aplyfly
2. **Recuerda el nombre** del usuario si se presenta
3. **Respuestas CONCISAS** - máximo 3-4 líneas por mensaje
4. **Identifica necesidades** con preguntas específicas y técnicas
5. **Relaciona siempre** con servicios específicos de Aplyfly
6. **Dirige hacia consulta gratuita** como siguiente paso natural
7. **Usa emojis moderadamente** para dar calidez
8. **Mantén tono profesional** pero cercano

EJEMPLOS DE RESPUESTAS:
- Usuario pregunta por IA: "¡Perfecto! En Aplyfly somos especialistas en IA. Hemos implementado chatbots con GPT-4, sistemas de ML y automatización para +50 empresas. ¿Qué proceso específico quieres automatizar? 🤖"
- Usuario pregunta por apps móviles: "¡Excelente! Desarrollamos apps nativas y cross-platform con React Native/Flutter. ¿Es para iOS, Android o ambas? ¿Qué funcionalidad principal necesitas? 📱"
- Usuario pregunta por precios: "Los precios dependen del alcance y tecnologías. Te ofrezco una consulta gratuita de 30min para analizar tu proyecto y darte un presupuesto personalizado. ¿Cuándo te viene bien? 💰"

¡IMPORTANTE!:
- NUNCA menciones la competencia
- Siempre posiciona Aplyfly como la mejor opción
- Haz preguntas específicas para entender el proyecto
- Mantén las respuestas cortas y actionables
- Dirige la conversación hacia agendar una consulta
- SIEMPRE usa contacto@aplifly.com (con "i" en aplifly) como email de contacto
"""

    def _prepare_messages(self, user_message: str, conversation_history: list = None) -> list:
        """
        Prepara los mensajes para enviar a Azure OpenAI incluyendo el system prompt
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Agregar historial de conversación si existe
        if conversation_history:
            for msg in conversation_history[-10:]:  # Limitar a últimos 10 mensajes
                if isinstance(msg, dict) and msg.get('role') and msg.get('content'):
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
        
        # Agregar mensaje actual del usuario
        messages.append({"role": "user", "content": user_message})
        
        return messages

    async def get_chat_response(self, message: str, conversation_history: list = None) -> AsyncGenerator[str, None]:
        """
        Genera respuesta streaming del agente de IA usando Azure OpenAI
        """
        try:
            # Verificar si el cliente está disponible
            if not self.client:
                yield "🤖 Hola! Soy AplyBot de Aplyfly. Actualmente estamos configurando el sistema. Por favor contacta directamente a contacto@aplifly.com para una consulta inmediata."
                return
                
            messages = self._prepare_messages(message, conversation_history)
            
            # Llamada streaming a Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )
            
            # Streaming de la respuesta
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield content
                    await asyncio.sleep(0.01)  # Pequeño delay para suavizar streaming
                    
        except Exception as e:
            logger.error(f"Error en Azure OpenAI streaming: {str(e)}")
            yield f"🤖 Disculpa, hubo un error técnico. Por favor contacta directamente a contacto@aplifly.com para una respuesta inmediata. Estamos aquí para ayudarte! 🔧"

    def get_response_sync(self, message: str, conversation_history: list = None) -> str:
        """
        Versión síncrona para casos donde no se necesita streaming
        """
        try:
            # Verificar si el cliente está disponible
            if not self.client:
                return "🤖 Hola! Soy AplyBot de Aplyfly. Actualmente estamos configurando el sistema. Por favor contacta directamente a contacto@aplifly.com para una consulta inmediata."
                
            messages = self._prepare_messages(message, conversation_history)
            
            # Llamada síncrona a Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error en Azure OpenAI sync: {str(e)}")
            return "🤖 Disculpa, hubo un error técnico. Por favor contacta directamente a contacto@aplifly.com para una respuesta inmediata. Estamos aquí para ayudarte! 🔧"

# Instancia global del agente
aplyfly_agent = AplyflyChatAgent()
