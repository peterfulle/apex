#!/usr/bin/env python
"""
Test del Chat de IA de Aplyfly
Prueba las funcionalidades del agente virtual
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://127.0.0.1:8000"
CHAT_API = f"{BASE_URL}/api/chat/"

def test_chat_basic():
    """Prueba básica del chat"""
    print("🧪 Probando chat básico...")
    
    data = {
        "message": "Hola, ¿qué servicios ofrecen?",
        "history": [],
        "streaming": False
    }
    
    response = requests.post(CHAT_API, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Chat básico funcionando")
        print(f"🤖 Respuesta: {result['response'][:100]}...")
        return True
    else:
        print(f"❌ Error en chat básico: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return False

def test_chat_conversation():
    """Prueba una conversación completa"""
    print("\n💬 Probando conversación...")
    
    conversation = [
        "Hola, necesito desarrollar una aplicación web",
        "¿Qué tecnologías utilizan?",
        "¿Cuánto tiempo tardarían en desarrollarla?",
        "¿Podrían darme un presupuesto?"
    ]
    
    history = []
    
    for i, message in enumerate(conversation, 1):
        print(f"\n👤 Mensaje {i}: {message}")
        
        data = {
            "message": message,
            "history": history,
            "streaming": False
        }
        
        response = requests.post(CHAT_API, json=data)
        
        if response.status_code == 200:
            result = response.json()
            bot_response = result['response']
            print(f"🤖 Respuesta: {bot_response[:150]}...")
            
            # Agregar al historial
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": bot_response})
            
            time.sleep(1)  # Pausa entre mensajes
        else:
            print(f"❌ Error en mensaje {i}: {response.status_code}")
            break
    
    print("\n✅ Conversación completada")

def test_chat_streaming():
    """Prueba el modo streaming"""
    print("\n🌊 Probando modo streaming...")
    
    data = {
        "message": "Explícame todos los servicios de IA que manejan en Aplyfly",
        "history": [],
        "streaming": True
    }
    
    try:
        response = requests.post(CHAT_API, json=data, stream=True)
        
        if response.status_code == 200:
            print("✅ Streaming iniciado")
            print("🤖 Respuesta streaming:")
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            data_json = json.loads(line_str[6:])
                            if data_json.get('type') == 'content' and 'chunk' in data_json:
                                chunk = data_json['chunk']
                                full_response += chunk
                                print(chunk, end='', flush=True)
                            elif data_json.get('type') == 'end':
                                print("\n✅ Streaming completado")
                                break
                        except json.JSONDecodeError:
                            continue
            
            print(f"\n📝 Respuesta completa ({len(full_response)} caracteres)")
            return True
        else:
            print(f"❌ Error en streaming: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión en streaming: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del Chat IA de Aplyfly")
    print("="*50)
    
    # Verificar que el servidor esté funcionando
    try:
        response = requests.get(f"{BASE_URL}/api/chat/test/")
        if response.status_code == 200:
            print("✅ Servidor funcionando")
            print(f"🔧 Estado: {response.json()}")
        else:
            print("❌ Servidor no disponible")
            exit(1)
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        exit(1)
    
    print("\n" + "="*50)
    
    # Ejecutar pruebas
    success_count = 0
    total_tests = 3
    
    if test_chat_basic():
        success_count += 1
    
    if test_chat_conversation():
        success_count += 1
    
    if test_chat_streaming():
        success_count += 1
    
    print("\n" + "="*50)
    print(f"🎯 Pruebas completadas: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! El chat está funcionando perfectamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("\n💡 Puedes probar el chat en: http://127.0.0.1:8000")
    print("🤖 Busca el botón flotante de chat en la esquina inferior derecha")
