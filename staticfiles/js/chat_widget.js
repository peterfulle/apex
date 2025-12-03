/**
 * Aplyfly Chat Widget - Asistente Virtual Inteligente
 * Maneja toda la funcionalidad del chat con IA
 */

class AplyflyChatWidget {
    constructor() {
        this.isOpen = false;
        this.conversationHistory = [];
        this.isTyping = false;
        this.currentStreamingMessage = '';
        
        this.initializeElements();
        this.bindEvents();
        this.loadWelcomeMessage();
    }
    
    initializeElements() {
        // Elementos principales
        this.widget = document.getElementById('aplyfly-chat-widget');
        this.toggleBtn = document.getElementById('chat-toggle-btn');
        this.chatWindow = document.getElementById('chat-window');
        this.minimizeBtn = document.getElementById('minimize-chat');
        
        // Elementos del chat
        this.messagesContainer = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.sendingIndicator = document.getElementById('sending-indicator');
        this.charCounter = document.getElementById('char-counter');
        this.quickSuggestions = document.getElementById('quick-suggestions');
        
        // Iconos
        this.chatIcon = document.getElementById('chat-icon');
        this.closeIcon = document.getElementById('close-icon');
        
        console.log('🔍 Elementos inicializados:', {
            widget: !!this.widget,
            toggleBtn: !!this.toggleBtn,
            chatWindow: !!this.chatWindow,
            minimizeBtn: !!this.minimizeBtn
        });
    }
    
    bindEvents() {
        // Toggle del chat
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', (e) => {
                console.log('🔘 Toggle button clicked');
                e.preventDefault();
                e.stopPropagation();
                this.toggleChat();
            });
        } else {
            console.error('❌ Toggle button not found');
        }
        
        // Minimizar con debugging
        if (this.minimizeBtn) {
            this.minimizeBtn.addEventListener('click', (e) => {
                console.log('Botón minimizar clickeado');
                e.preventDefault();
                e.stopPropagation();
                this.closeChat();
            });
        } else {
            console.error('Botón minimizar no encontrado');
        }
        
        // Envío de mensajes
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (this.chatInput) {
            this.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            // Auto-resize del textarea
            this.chatInput.addEventListener('input', () => {
                this.autoResizeTextarea();
                this.updateCharCounter();
            });
        }
        
        // Sugerencias rápidas
        if (this.quickSuggestions) {
            this.quickSuggestions.addEventListener('click', (e) => {
                if (e.target.classList.contains('suggestion-btn')) {
                    this.handleSuggestionClick(e.target.textContent.trim());
                }
            });
        }
        
        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeChat();
            }
        });
        
        // Click fuera del widget para cerrar
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.widget.contains(e.target)) {
                this.closeChat();
            }
        });
    }
    
    toggleChat() {
        console.log('🔄 Toggle chat - current state:', this.isOpen);
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        console.log('📖 Opening chat');
        this.isOpen = true;
        this.chatWindow.classList.add('open');
        
        // Cambiar iconos
        if (this.chatIcon) this.chatIcon.classList.add('hidden');
        if (this.closeIcon) this.closeIcon.classList.remove('hidden');
        
        // Focus en el input
        setTimeout(() => {
            if (this.chatInput) this.chatInput.focus();
        }, 300);
        
        // Analytics (opcional)
        this.trackEvent('chat_opened');
    }
    
    closeChat() {
        console.log('📕 Closing chat');
        this.isOpen = false;
        this.chatWindow.classList.remove('open');
        
        // Cambiar iconos
        if (this.closeIcon) this.closeIcon.classList.add('hidden');
        if (this.chatIcon) this.chatIcon.classList.remove('hidden');
        
        // Analytics (opcional)
        this.trackEvent('chat_closed');
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Agregar mensaje del usuario
        this.addUserMessage(message);
        
        // Limpiar input
        this.chatInput.value = '';
        this.updateCharCounter();
        this.autoResizeTextarea();
        
        // Ocultar sugerencias después del primer mensaje
        this.quickSuggestions.style.display = 'none';
        
        // Mostrar indicador de typing
        this.showTypingIndicator();
        
        try {
            // Enviar a la API
            await this.sendToAPI(message);
        } catch (error) {
            this.hideTypingIndicator();
            this.addBotMessage('Disculpa, hubo un error de conexión. Por favor intenta nuevamente o contacta directamente a info@aplyfly.com 🔧');
            console.error('Error en chat:', error);
        }
    }
    
    async sendToAPI(message) {
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    history: this.conversationHistory,
                    streaming: true
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Manejar streaming response
            await this.handleStreamingResponse(response);
            
        } catch (error) {
            console.error('Error en API:', error);
            throw error;
        }
    }
    
    async handleStreamingResponse(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        this.hideTypingIndicator();
        
        // Crear contenedor para el mensaje streaming
        const messageContainer = this.createBotMessageContainer();
        const textElement = messageContainer.querySelector('.bot-message-text');
        
        this.currentStreamingMessage = '';
        textElement.classList.add('typewriter-text');
        
        try {
            while (true) {
                const { done, value } = await reader.read();
                
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'content' && data.chunk) {
                                this.currentStreamingMessage += data.chunk;
                                textElement.innerHTML = this.formatMessage(this.currentStreamingMessage);
                                this.scrollToBottom();
                            } else if (data.type === 'end') {
                                // Finalizar streaming
                                textElement.classList.remove('typewriter-text');
                                this.addToHistory('assistant', this.currentStreamingMessage);
                                return;
                            } else if (data.type === 'error') {
                                throw new Error(data.error);
                            }
                        } catch (parseError) {
                            console.warn('Error parsing SSE data:', parseError);
                        }
                    }
                }
            }
        } catch (error) {
            textElement.classList.remove('typewriter-text');
            textElement.innerHTML = 'Error de conexión. Por favor intenta nuevamente.';
            console.error('Streaming error:', error);
        }
    }
    
    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start space-x-3 justify-end animate-slideInRight';
        
        messageDiv.innerHTML = `
            <div class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-2xl rounded-tr-md p-4 shadow-sm max-w-xs">
                <p class="text-sm leading-relaxed">${this.escapeHtml(message)}</p>
                <div class="text-xs text-cyan-100 mt-2 text-right">${this.getCurrentTime()}</div>
            </div>
            <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center flex-shrink-0">
                <i class="fas fa-user text-gray-600 text-xs"></i>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Agregar al historial
        this.addToHistory('user', message);
    }
    
    addBotMessage(message) {
        const messageContainer = this.createBotMessageContainer();
        const textElement = messageContainer.querySelector('.bot-message-text');
        textElement.innerHTML = this.formatMessage(message);
        
        this.addToHistory('assistant', message);
    }
    
    createBotMessageContainer() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start space-x-3 animate-slideInLeft';
        
        messageDiv.innerHTML = `
            <div class="w-8 h-8 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <i class="fas fa-robot text-white text-xs"></i>
            </div>
            <div class="bg-white rounded-2xl rounded-tl-md p-4 shadow-sm border border-gray-100 max-w-xs">
                <div class="bot-message-text text-gray-800 text-sm leading-relaxed"></div>
                <div class="text-xs text-gray-400 mt-2">${this.getCurrentTime()}</div>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        if (this.typingIndicator) this.typingIndicator.style.opacity = '1';
        if (this.sendBtn) this.sendBtn.disabled = true;
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        if (this.typingIndicator) this.typingIndicator.style.opacity = '0';
        if (this.sendBtn) this.sendBtn.disabled = false;
    }
    
    handleSuggestionClick(text) {
        // Extraer solo el texto sin emoji
        const cleanText = text.replace(/[^\w\s]/gi, '').trim();
        
        const suggestions = {
            'Desarrollo web': '¿Qué servicios de desarrollo web ofrecen? Me interesa una aplicación moderna.',
            'Inteligencia Artificial': 'Quiero implementar IA en mi negocio. ¿Qué soluciones manejan?',
            'Apps móviles': '¿Desarrollan aplicaciones móviles? Necesito una app para iOS y Android.',
            'Presupuesto': '¿Podrían darme una estimación de costos para mi proyecto?'
        };
        
        const suggestion = suggestions[cleanText];
        if (suggestion) {
            this.chatInput.value = suggestion;
            this.chatInput.focus();
        }
    }
    
    addToHistory(role, content) {
        this.conversationHistory.push({ role, content });
        
        // Limitar historial para evitar exceso de tokens
        if (this.conversationHistory.length > 20) {
            this.conversationHistory = this.conversationHistory.slice(-20);
        }
    }
    
    formatMessage(message) {
        // Convertir markdown básico y emojis
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/```(.*?)```/gs, '<code class="bg-gray-100 px-2 py-1 rounded text-xs">$1</code>');
    }
    
    scrollToBottom() {
        setTimeout(() => {
            if (this.messagesContainer) {
                this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            }
        }, 100);
    }
    
    autoResizeTextarea() {
        if (this.chatInput) {
            this.chatInput.style.height = 'auto';
            this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 120) + 'px';
        }
    }
    
    updateCharCounter() {
        if (this.chatInput && this.charCounter) {
            const count = this.chatInput.value.length;
            this.charCounter.textContent = `${count}/300`;
            
            if (count > 250) {
                this.charCounter.classList.add('text-red-500');
            } else {
                this.charCounter.classList.remove('text-red-500');
            }
        }
    }
    
    getCurrentTime() {
        return new Date().toLocaleTimeString('es-ES', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    loadWelcomeMessage() {
        // El mensaje de bienvenida ya está en el HTML
    }
    
    trackEvent(eventName) {
        // Integración con analytics (Google Analytics, etc.)
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                'event_category': 'chat_widget',
                'event_label': 'aplyfly_chat'
            });
        }
    }
}

// Inicializar el widget cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM ready, looking for chat widget...');
    
    // Verificar que estamos en una página que debe tener el chat
    const chatElement = document.getElementById('aplyfly-chat-widget');
    
    if (chatElement) {
        console.log('✅ Chat widget element found, initializing...');
        window.aplyflyChatWidget = new AplyflyChatWidget();
        
        // Agregar indicador de carga global
        window.addEventListener('beforeunload', function() {
            if (window.aplyflyChatWidget && window.aplyflyChatWidget.isOpen) {
                window.aplyflyChatWidget.trackEvent('chat_closed_page_unload');
            }
        });
        
        console.log('🤖 Aplyfly Chat Widget inicializado correctamente');
    } else {
        console.error('❌ Chat widget element not found in DOM');
    }
});