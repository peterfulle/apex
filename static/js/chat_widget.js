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
        
        // Nuevos botones de control
        this.clearChatBtn = document.getElementById('clear-chat');
        this.infoChatBtn = document.getElementById('info-chat');
        this.exportChatBtn = document.getElementById('export-chat');
        
        // Modal de información
        this.infoModal = document.getElementById('info-modal');
        this.closeModalBtn = document.getElementById('close-info-modal');
        
        // Indicadores de estado
        this.connectionStatus = document.getElementById('connection-status');
        this.statusText = document.getElementById('status-text');
        this.statusNotification = document.getElementById('status-notification');
        
        // Iconos
        this.chatIcon = document.getElementById('chat-icon');
        this.closeIcon = document.getElementById('close-icon');
        
        console.log('🔍 Elementos inicializados:', {
            widget: !!this.widget,
            toggleBtn: !!this.toggleBtn,
            chatWindow: !!this.chatWindow,
            minimizeBtn: !!this.minimizeBtn,
            clearChatBtn: !!this.clearChatBtn,
            infoChatBtn: !!this.infoChatBtn,
            exportChatBtn: !!this.exportChatBtn,
            infoModal: !!this.infoModal
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
                    const message = e.target.getAttribute('data-message');
                    if (message) {
                        this.chatInput.value = message;
                        this.sendMessage();
                    } else {
                        this.handleSuggestionClick(e.target.textContent.trim());
                    }
                }
            });
        }
        
        // Nuevos botones de control
        if (this.clearChatBtn) {
            this.clearChatBtn.addEventListener('click', () => this.clearChat());
        }
        
        if (this.infoChatBtn) {
            this.infoChatBtn.addEventListener('click', () => this.openInfoModal());
        }
        
        if (this.exportChatBtn) {
            this.exportChatBtn.addEventListener('click', () => this.exportChat());
        }
        
        // Modal de información
        if (this.closeModalBtn) {
            this.closeModalBtn.addEventListener('click', () => this.closeInfoModal());
        }
        
        if (this.infoModal) {
            this.infoModal.addEventListener('click', (e) => {
                if (e.target === this.infoModal) {
                    this.closeInfoModal();
                }
            });
        }
        
        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (this.infoModal && !this.infoModal.classList.contains('hidden')) {
                    this.closeInfoModal();
                } else if (this.isOpen) {
                    this.closeChat();
                }
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
        
        // Cambiar clases para abrir el chat
        this.chatWindow.classList.remove('scale-0', 'opacity-0');
        this.chatWindow.classList.add('scale-100', 'opacity-100');
        
        // Cambiar iconos
        if (this.chatIcon) this.chatIcon.classList.add('hidden');
        if (this.closeIcon) this.closeIcon.classList.remove('hidden');
        
        // Focus en el input
        setTimeout(() => {
            if (this.chatInput) this.chatInput.focus();
        }, 300);
        
        // Actualizar estado de conexión
        this.updateConnectionStatus(true);
        
        // Analytics (opcional)
        this.trackEvent('chat_opened');
    }
    
    closeChat() {
        console.log('📕 Closing chat');
        this.isOpen = false;
        
        // Cambiar clases para cerrar el chat
        this.chatWindow.classList.remove('scale-100', 'opacity-100');
        this.chatWindow.classList.add('scale-0', 'opacity-0');
        
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
            this.updateConnectionStatus(true);
        } catch (error) {
            this.hideTypingIndicator();
            this.addBotMessage('Disculpa, hubo un error de conexión. Por favor intenta nuevamente o contacta directamente a info@aplyfly.com 🔧');
            this.updateConnectionStatus(false);
            this.showStatusNotification('Error de conexión', 'error');
            console.error('Error en chat:', error);
        }
    }
    
    async sendToAPI(message) {
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
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
    
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        // También intentar obtenerlo de meta tag si existe
        if (!cookieValue) {
            const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
            if (csrfMetaTag) {
                cookieValue = csrfMetaTag.getAttribute('content');
            }
        }
        return cookieValue;
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
            <div class="flex flex-col items-end space-y-1">
                <div class="text-xs text-gray-400">${this.getCurrentTime()}</div>
                <div class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg rounded-tr-sm p-3 shadow-sm max-w-xs">
                    <p class="text-xs leading-relaxed">${this.escapeHtml(message)}</p>
                </div>
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
            this.charCounter.textContent = `${count}/500`;
            
            if (count > 450) {
                this.charCounter.classList.add('text-red-500');
                this.charCounter.classList.remove('text-yellow-500');
            } else if (count > 400) {
                this.charCounter.classList.add('text-yellow-500');
                this.charCounter.classList.remove('text-red-500');
            } else {
                this.charCounter.classList.remove('text-red-500', 'text-yellow-500');
            }
        }
    }
    
    clearChat() {
        if (confirm('¿Estás seguro de que quieres limpiar toda la conversación?')) {
            // Limpiar mensajes excepto el de bienvenida
            const messages = this.messagesContainer.querySelectorAll('.animate-slideInLeft, .animate-slideInRight, .animate-fadeIn');
            const welcomeMessage = this.messagesContainer.querySelector('.animate-fadeIn');
            
            // Remover todos los mensajes excepto el de bienvenida
            messages.forEach(msg => {
                if (msg !== welcomeMessage) {
                    msg.remove();
                }
            });
            
            // Mostrar sugerencias nuevamente
            if (this.quickSuggestions) {
                this.quickSuggestions.style.display = 'flex';
            }
            
            // Limpiar historial de conversación
            this.conversationHistory = [];
            
            this.showStatusNotification('Chat limpiado exitosamente', 'success');
        }
    }
    
    openInfoModal() {
        if (this.infoModal) {
            this.infoModal.classList.remove('hidden');
            setTimeout(() => {
                const modalContent = document.getElementById('info-modal-content');
                if (modalContent) {
                    modalContent.classList.remove('scale-95', 'opacity-0');
                    modalContent.classList.add('scale-100', 'opacity-100');
                }
            }, 10);
        }
    }
    
    closeInfoModal() {
        const modalContent = document.getElementById('info-modal-content');
        if (modalContent) {
            modalContent.classList.remove('scale-100', 'opacity-100');
            modalContent.classList.add('scale-95', 'opacity-0');
        }
        
        setTimeout(() => {
            if (this.infoModal) {
                this.infoModal.classList.add('hidden');
            }
        }, 300);
    }
    
    exportChat() {
        if (this.conversationHistory.length === 0) {
            this.showStatusNotification('No hay mensajes para exportar', 'error');
            return;
        }

        const chatData = {
            exported_at: new Date().toISOString(),
            total_messages: this.conversationHistory.length,
            conversation: this.conversationHistory
        };

        const dataStr = JSON.stringify(chatData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `aplybot-chat-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        this.showStatusNotification('Chat exportado exitosamente', 'success');
    }
    
    showStatusNotification(message, type = 'success') {
        if (!this.statusNotification) return;
        
        const notification = this.statusNotification;
        const messageSpan = document.getElementById('notification-text');
        
        if (messageSpan) {
            messageSpan.textContent = message;
        }
        
        if (type === 'error') {
            notification.firstElementChild.className = 'bg-gradient-to-r from-red-100 to-pink-100 text-red-800 px-3 py-2 rounded-lg border border-red-200';
        } else {
            notification.firstElementChild.className = 'bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 px-3 py-2 rounded-lg border border-emerald-200';
        }
        
        notification.classList.remove('opacity-0', 'translate-y-2');
        notification.classList.add('opacity-100', 'translate-y-0');
        
        setTimeout(() => {
            notification.classList.remove('opacity-100', 'translate-y-0');
            notification.classList.add('opacity-0', 'translate-y-2');
        }, 3000);
    }
    
    updateConnectionStatus(isConnected) {
        if (!this.connectionStatus || !this.statusText) return;
        
        if (isConnected) {
            this.connectionStatus.className = 'w-2 h-2 bg-emerald-400 rounded-full mr-2 animate-pulse shadow-sm';
            this.statusText.textContent = 'Conectado • Aplyfly';
        } else {
            this.connectionStatus.className = 'w-2 h-2 bg-red-400 rounded-full mr-2 animate-pulse shadow-sm';
            this.statusText.textContent = 'Desconectado • Reintentando...';
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
    
    // Agregar estilos CSS adicionales para animaciones
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .animate-fadeIn {
            animation: fadeIn 0.3s ease-out;
        }
        
        .animate-slideInLeft {
            animation: slideInLeft 0.3s ease-out;
        }
        
        .animate-slideInRight {
            animation: slideInRight 0.3s ease-out;
        }
        
        /* Mejorar scrollbar en el chat */
        #chat-messages::-webkit-scrollbar {
            width: 4px;
        }
        
        #chat-messages::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        #chat-messages::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 2px;
        }
        
        #chat-messages::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        
        /* Transiciones del chat window */
        #chat-window {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: bottom right;
        }
        
        /* Efecto typewriter para mensajes streaming */
        .typewriter-text::after {
            content: '|';
            opacity: 1;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});