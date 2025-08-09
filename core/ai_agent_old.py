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
    Agente de IA especializado para Aplyfly - Asistente de atención al cliente
    100% enfocado en desarrollo de software y servicios de Aplyfly
    """
    
    def __init__(self):
        # Configuración temporal sin Azure - usaremos respuestas predefinidas
        self.deployment = "gpt-4"
        
        # Personalidad y conocimiento de Aplyfly
        self.system_prompt = """
        Eres AplyBot, asistente virtual de Aplyfly - empresa líder en desarrollo de software.
        
        IDENTIDAD:
        - Personalidad: Profesional, técnico pero amigable
        - Objetivo: Convertir consultas en leads calificados
        
        SERVICIOS DE APLYFLY:
        
        🚀 PRINCIPALES:
        1. **Apps Web**: React, Vue.js, Django, PWAs escalables
        2. **Sistemas Empresariales**: CRM, ERP, automatización, APIs
        3. **Inteligencia Artificial**: GPT, Claude, chatbots, ML
        4. **Apps Móviles**: React Native, Flutter, nativas iOS/Android
        5. **APIs & Microservicios**: REST, GraphQL, Docker, Kubernetes
        6. **Consultoría**: Auditorías, arquitectura, migración cloud
        
        🏢 EMPRESA:
        - +100 proyectos exitosos
        - 99% satisfacción
        - Equipo senior
        - Metodología ágil
        - Soporte 24/7
        
        💼 PROCESO:
        1. Consulta gratuita 30min
        2. Propuesta técnica personalizada
        3. Desarrollo ágil iterativo
        4. Testing y deploy
        5. Soporte continuo
        
        📞 CONTACTO:
        - Email: info@aplyfly.com
        - WhatsApp: +123 456 7890
        - Consulta gratuita disponible
        
        INSTRUCCIONES:
        
        1. **Respuestas CONCISAS** - máximo 3-4 líneas
        2. **Identifica necesidades** con preguntas específicas
        3. **Relaciona con servicios** de Aplyfly
        4. **Dirige a consulta gratuita** como siguiente paso
        5. **Usa emojis moderadamente**
        6. **Mantén tono profesional pero cercano**
        
        RESPUESTAS TIPO:
        - IA: "¡Perfecto! Especialistas en IA. Hemos implementado chatbots y ML con OpenAI/Claude. ¿Qué tipo de automatización necesitas?"
        - Apps móviles: "Desarrollamos apps nativas y multiplataforma con React Native/Flutter. ¿Para qué plataformas y qué funcionalidad principal?"
        - Precios: "Depende del alcance. Ofrezco consulta gratuita de 30min para analizar tu proyecto. ¿Cuándo te viene bien?"
        
        ¡IMPORTANTE: Respuestas cortas, directas y siempre con pregunta para continuar conversación!
        
        NUNCA menciones competencia. Posiciona Aplyfly como mejor opción.
        """
        
        # Respuestas predefinidas inteligentes
        self.predefined_responses = {
            'saludo': [
                "¡Hola! 👋 Soy AplyBot de Aplyfly. Especialistas en desarrollo web, IA y apps móviles. ¿En qué proyecto puedo ayudarte? 🚀",
                "¡Bienvenido/a! Soy tu asistente virtual de Aplyfly. ¿Tienes algún proyecto de desarrollo en mente? 💻",
            ],
            'servicios': [
                "Ofrecemos: Apps Web (React/Django), IA & Chatbots, Apps Móviles, APIs, y Consultoría. ¿Qué tipo de proyecto tienes en mente? 🛠️",
                "Nuestros servicios principales: Desarrollo Web, Inteligencia Artificial, Apps Móviles, Sistemas Empresariales. ¿Cuál te interesa más? 💡",
            ],
            'web': [
                "¡Perfecto! Desarrollamos apps web modernas con React, Vue.js y Django. PWAs, sistemas escalables. ¿Qué funcionalidad necesitas? 🌐",
                "Especialistas en desarrollo web: React, Vue, Django, APIs. ¿Tu proyecto es e-commerce, dashboard, o qué tipo de aplicación? 💻",
            ],
            'ia': [
                "¡Excelente! Implementamos IA: chatbots inteligentes, análisis de datos, automatización con OpenAI/Claude. ¿Qué quieres automatizar? 🤖",
                "Servicios de IA: Chatbots, ML, análisis de datos, integración GPT. ¿Para qué industria o caso específico? 🧠",
            ],
            'movil': [
                "Desarrollamos apps nativas y multiplataforma con React Native/Flutter. iOS, Android. ¿Qué tipo de app necesitas? 📱",
                "Apps móviles nativas y cross-platform. React Native, Flutter. ¿Es para iOS, Android o ambas? ¿Qué funcionalidad? 🚀",
            ],
            'precio': [
                "Los precios dependen del alcance y complejidad. Ofrezco consulta gratuita de 30min para analizar tu proyecto. ¿Te parece bien? 💰",
                "Cada proyecto es único. ¿Te gustaría una consulta gratuita para evaluar tu idea y darte un presupuesto personalizado? 📊",
            ],
            'contacto': [
                "¡Perfecto! Puedes contactarnos: info@aplyfly.com o WhatsApp +123 456 7890. ¿Prefieres una llamada o empezamos por email? 📞",
                "Contacto directo: info@aplyfly.com. También ofrezco consulta gratuita de 30min. ¿Cuándo te viene bien? ⏰",
            ],
            'default': [
                "Interesante proyecto. En Aplyfly manejamos desarrollo web, IA, apps móviles y más. ¿Podrías contarme más detalles? 🤔",
                "¡Genial! Somos especialistas en soluciones tech personalizadas. ¿Qué tecnología o funcionalidad específica necesitas? 💡",
            ]
        }
    
    async def get_chat_response(self, message: str, conversation_history: list = None) -> AsyncGenerator[str, None]:
        """
        Genera respuesta streaming del agente de IA usando respuestas inteligentes
        """
        try:
            # Analizar el mensaje para dar respuesta contextual
            response = self._get_smart_response(message.lower())
            
            # Simular streaming palabra por palabra
            words = response.split(' ')
            for i, word in enumerate(words):
                if i == 0:
                    yield word
                else:
                    yield f" {word}"
                await asyncio.sleep(0.05)  # Simular delay natural
                    
        except Exception as e:
            logger.error(f"Error en chat agent: {str(e)}")
            yield f"Disculpa, hubo un error técnico. Por favor contacta directamente a info@aplyfly.com o intenta nuevamente. 🔧"
    
    def get_response_sync(self, message: str, conversation_history: list = None) -> str:
        """
        Versión síncrona para casos donde no se necesita streaming
        """
        try:
            # Analizar contexto del historial
            context = self._analyze_conversation_context(conversation_history or [])
            return self._get_smart_response(message.lower(), context)
            
        except Exception as e:
            logger.error(f"Error en chat agent sync: {str(e)}")
            return "Disculpa, hubo un error técnico. Por favor contacta directamente a info@aplyfly.com 🔧"
    
    def _analyze_conversation_context(self, history: list) -> dict:
        """
        Analiza el historial de conversación para extraer contexto
        """
        context = {
            'user_name': None,
            'topics_discussed': [],
            'services_mentioned': []
        }
        
        # Buscar nombre del usuario en mensajes anteriores
        for msg in history:
            if isinstance(msg, dict) and msg.get('role') == 'user':
                content = msg.get('content', '').lower()
                print(f"🔍 Analizando mensaje del usuario: {content}")
                
                # Detectar presentación del usuario - patrones más amplios
                if any(phrase in content for phrase in ['me llamo', 'soy', 'mi nombre es', 'soy pedro', 'soy juan']):
                    words = content.split()
                    for i, word in enumerate(words):
                        if word in ['llamo', 'soy', 'nombre'] and i + 1 < len(words):
                            # Tomar la siguiente palabra como nombre
                            potential_name = words[i + 1].capitalize()
                            # Si hay dos palabras después (nombre y apellido)
                            if i + 2 < len(words) and words[i + 2].replace(',', '').isalpha():
                                context['user_name'] = f"{potential_name} {words[i + 2].capitalize()}"
                            else:
                                context['user_name'] = potential_name
                            print(f"👤 Nombre detectado: {context['user_name']}")
                            break
                
                # También detectar si dice directamente su nombre
                # Buscar nombres comunes en el texto
                common_names = ['pedro', 'juan', 'maria', 'ana', 'carlos', 'luis', 'jose', 'antonio', 'francisco', 'manuel', 'david', 'daniel', 'rafael', 'miguel', 'alejandro', 'gonzalez', 'rodriguez', 'garcia', 'martinez', 'lopez', 'hernandez', 'perez', 'sanchez', 'ramirez', 'cruz']
                for name in common_names:
                    if name in content and not context['user_name']:
                        # Buscar el contexto alrededor del nombre
                        words = content.split()
                        for i, word in enumerate(words):
                            if name in word.lower():
                                if i + 1 < len(words) and words[i + 1].replace(',', '').isalpha():
                                    context['user_name'] = f"{word.capitalize()} {words[i + 1].capitalize()}"
                                else:
                                    context['user_name'] = word.capitalize()
                                print(f"👤 Nombre detectado por patrón: {context['user_name']}")
                                break
                
                # Detectar temas mencionados
                if any(word in content for word in ['web', 'página', 'sitio']):
                    context['topics_discussed'].append('web')
                if any(word in content for word in ['ia', 'inteligencia', 'ai']):
                    context['topics_discussed'].append('ia')
                if any(word in content for word in ['móvil', 'app', 'aplicación']):
                    context['topics_discussed'].append('mobile')
        
        print(f"📊 Contexto final: {context}")
        return context
    
    def _get_smart_response(self, message: str, context: dict = None) -> str:
        """
        Analiza el mensaje y devuelve una respuesta contextual inteligente
        """
        import random
        
        if context is None:
            context = {}
        
        message = message.lower().strip()
        user_name = context.get('user_name', '')
        
        # Respuestas personalizadas si conocemos el nombre
        name_prefix = f"¡Hola {user_name}! " if user_name else ""
        
        # Detectar preguntas específicas sobre contexto
        if any(phrase in message for phrase in ['mi nombre', 'cómo me llamo', 'cual es mi nombre', 'como me llamo']):
            if user_name:
                return f"Te llamas {user_name}, ¿verdad? 😊 ¿En qué proyecto puedo ayudarte?"
            else:
                return "No me has dicho tu nombre aún. ¿Cómo te llamas? 😊"
        
        # Detectar cuando el usuario se presenta (nombres específicos)
        if any(name in message for name in ['pedro', 'juan', 'maria', 'ana', 'carlos', 'luis']):
            if 'pedro' in message and 'gonzalez' in message:
                return "¡Mucho gusto Pedro González! 😊 ¿En qué proyecto puedo ayudarte hoy?"
            elif any(phrase in message for phrase in ['me llamo', 'soy']):
                # Extraer el nombre del mensaje actual
                words = message.split()
                for i, word in enumerate(words):
                    if word in ['llamo', 'soy'] and i + 1 < len(words):
                        name_parts = []
                        # Recoger palabras que parecen nombres
                        for j in range(i + 1, min(i + 3, len(words))):
                            if words[j].replace(',', '').replace('.', '').isalpha():
                                name_parts.append(words[j].capitalize())
                        if name_parts:
                            full_name = ' '.join(name_parts)
                            return f"¡Mucho gusto {full_name}! 😊 ¿En qué proyecto puedo ayudarte hoy?"
        
        # Detectar intención basada en palabras clave
        if any(word in message for word in ['hola', 'hello', 'hi', 'buenas', 'buenos']):
            response = random.choice(self.predefined_responses['saludo'])
            return name_prefix + response if user_name else response
        
        elif any(word in message for word in ['servicio', 'qué hacen', 'qué ofrecen', 'servicios', 'capaz', 'haces']):
            responses = [
                "🚀 **Servicios Aplyfly:**\n• Apps Web (React/Django)\n• IA & Chatbots\n• Apps Móviles\n• APIs & Sistemas\n\n¿Qué tipo de proyecto tienes en mente?",
                "Somos especialistas en:\n✅ Desarrollo Web moderno\n✅ Inteligencia Artificial\n✅ Apps Móviles nativas\n✅ Sistemas empresariales\n\n¿Cuál te interesa más? 💡"
            ]
            return random.choice(responses)
        
        elif any(word in message for word in ['web', 'página', 'sitio', 'react', 'django', 'frontend']):
            return random.choice(self.predefined_responses['web'])
        
        elif any(word in message for word in ['ia', 'inteligencia artificial', 'chatbot', 'bot', 'ai', 'machine learning', 'ml', 'proyecto ia', 'quiero un proyecto ia']):
            responses = [
                "¡Perfecto para IA! 🤖 Implementamos:\n• Chatbots inteligentes\n• Análisis de datos con ML\n• Automatización con GPT/Claude\n• Asistentes virtuales\n\n¿Para qué industria o proceso específico?",
                "¡Excelente elección! IA es nuestro fuerte:\n✅ Chatbots conversacionales\n✅ Análisis predictivo\n✅ Automatización inteligente\n✅ Integración OpenAI/Claude\n\n¿Qué quieres automatizar? 🧠"
            ]
            return random.choice(responses)
        
        elif any(word in message for word in ['móvil', 'movil', 'app', 'aplicación', 'ios', 'android', 'flutter', 'react native']):
            return random.choice(self.predefined_responses['movil'])
        
        elif any(word in message for word in ['precio', 'costo', 'cuánto', 'presupuesto', 'cotización', 'vale', 'costar']):
            return random.choice(self.predefined_responses['precio'])
        
        elif any(word in message for word in ['contacto', 'contactar', 'llamar', 'email', 'whatsapp']):
            return random.choice(self.predefined_responses['contacto'])
        
        elif any(phrase in message for phrase in ['recomienda', 'recomendación', 'consejo', 'sugieres', 'lo que me recomiendes']):
            if context.get('topics_discussed'):
                topics = context['topics_discussed']
                if 'ia' in topics:
                    return f"Para IA {name_prefix}te recomiendo empezar con un chatbot inteligente para tu web. ¿Qué industria es tu negocio? 🤖"
                elif 'web' in topics:
                    return f"Para web {name_prefix}recomiendo React + Django para máximo rendimiento. ¿Qué funcionalidades necesitas? 💻"
            
            # Recomendación general personalizada
            if user_name:
                return f"¡Perfecto {user_name}! Te recomiendo empezar con una consulta gratuita de 30min para entender mejor tu proyecto. Según lo que me cuentes, podemos sugerir la mejor tecnología. ¿Te parece bien? 💡"
            else:
                return "Te recomiendo empezar con una consulta gratuita para evaluar tu proyecto específico. ¿Cuál es tu industria o tipo de negocio? 💡"
        
        else:
            # Respuesta por defecto más inteligente
            if user_name:
                return f"Entiendo {user_name}. En Aplyfly manejamos desarrollo web, IA, apps móviles y sistemas empresariales. ¿Podrías contarme más detalles sobre lo que necesitas? 🤔"
            else:
                return random.choice(self.predefined_responses['default'])

# Instancia global del agente
aplyfly_agent = AplyflyChatAgent()
