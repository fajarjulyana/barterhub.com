// Real-time Chat System using Socket.IO
class RealtimeChatSystem {
    constructor() {
        this.socket = null;
        this.conversationId = null;
        this.currentUserId = null;
        this.isConnected = false;
        this.typingTimeout = null;
        this.init();
    }

    init() {
        // Initialize Socket.IO connection
        this.socket = io({
            transports: ['websocket', 'polling'],
            upgrade: true,
            rememberUpgrade: true
        });

        this.setupSocketEvents();
        this.setupUIEvents();
        
        // Get current user ID from global variable
        if (typeof currentUserId !== 'undefined') {
            this.currentUserId = currentUserId;
        }
        
        // Get conversation ID from global variable
        if (typeof conversationId !== 'undefined') {
            this.conversationId = conversationId;
            this.joinConversation();
        }
    }

    setupSocketEvents() {
        // Connection events
        this.socket.on('connect', () => {
            console.log('Connected to chat server');
            this.isConnected = true;
            this.updateConnectionStatus(true);
            
            if (this.conversationId) {
                this.joinConversation();
            }
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from chat server');
            this.isConnected = false;
            this.updateConnectionStatus(false);
        });

        this.socket.on('connection_status', (data) => {
            console.log('Connection status:', data);
        });

        // Chat events
        this.socket.on('joined_conversation', (data) => {
            console.log('Joined conversation:', data.conversation_id);
            this.loadMessages();
        });

        this.socket.on('new_message', (data) => {
            this.displayMessage(data);
            this.scrollToBottom();
            this.playNotificationSound();
        });

        this.socket.on('message_sent', (data) => {
            console.log('Message sent successfully:', data.message_id);
        });

        this.socket.on('offer_response', (data) => {
            console.log('Offer response:', data);
            this.loadMessages(); // Refresh messages to show updated status
        });

        // User presence events
        this.socket.on('user_online', (data) => {
            this.updateUserStatus(data.user_id, true);
            this.showUserNotification(`${data.full_name} is online`, 'success');
        });

        this.socket.on('user_offline', (data) => {
            this.updateUserStatus(data.user_id, false);
        });

        this.socket.on('user_typing', (data) => {
            this.showTypingIndicator(data.username, data.is_typing);
        });

        // Error handling
        this.socket.on('error', (data) => {
            console.error('Socket error:', data);
            this.showAlert(data.message || 'An error occurred', 'error');
        });
    }

    setupUIEvents() {
        // Message form submission
        const messageForm = document.getElementById('messageForm');
        if (messageForm) {
            messageForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }

        // Message input events
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            // Auto-resize textarea
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });

            // Handle Enter key
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // Typing indicator
            messageInput.addEventListener('input', () => {
                this.handleTyping();
            });

            messageInput.addEventListener('blur', () => {
                this.stopTyping();
            });
        }

        // Offer/Deal response buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('accept-offer-btn')) {
                this.respondToOffer(e.target.dataset.messageId, 'accept');
            }
            if (e.target.classList.contains('reject-offer-btn')) {
                this.respondToOffer(e.target.dataset.messageId, 'reject');
            }
            if (e.target.classList.contains('counter-offer-btn')) {
                this.showCounterOfferModal(e.target.dataset.messageId);
            }
        });

        // Page visibility handling
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.conversationId) {
                this.loadMessages();
            }
        });
    }

    joinConversation() {
        if (this.conversationId && this.isConnected) {
            this.socket.emit('join_conversation', {
                conversation_id: this.conversationId
            });
        }
    }

    leaveConversation() {
        if (this.conversationId && this.isConnected) {
            this.socket.emit('leave_conversation', {
                conversation_id: this.conversationId
            });
        }
    }

    sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();

        if (!message) {
            this.showAlert('Pesan tidak boleh kosong', 'warning');
            return;
        }

        if (!this.isConnected) {
            this.showAlert('Tidak terhubung ke server chat', 'error');
            return;
        }

        const receiverId = document.getElementById('receiverId').value;
        const productId = document.getElementById('productId').value;
        const messageType = document.getElementById('messageType').value || 'text';

        // Prepare message data
        const messageData = {
            receiver_id: parseInt(receiverId),
            product_id: productId ? parseInt(productId) : null,
            message: message,
            message_type: messageType
        };

        // Add offer data if it's an offer message
        if (messageType === 'offer') {
            const offerPrice = document.getElementById('offerPrice');
            const offerQuantity = document.getElementById('offerQuantity');
            
            if (offerPrice && offerPrice.value) {
                messageData.offer_price = parseFloat(offerPrice.value);
            }
            if (offerQuantity && offerQuantity.value) {
                messageData.offer_quantity = parseInt(offerQuantity.value);
            }
        }

        // Send via Socket.IO
        this.socket.emit('send_message', messageData);

        // Clear input
        messageInput.value = '';
        messageInput.style.height = 'auto';
        document.getElementById('messageType').value = 'text';

        // Stop typing indicator
        this.stopTyping();
    }

    respondToOffer(messageId, action, counterPrice = null) {
        if (!this.isConnected) {
            this.showAlert('Tidak terhubung ke server chat', 'error');
            return;
        }

        const responseData = {
            message_id: parseInt(messageId),
            action: action
        };

        if (action === 'counter' && counterPrice) {
            responseData.counter_price = parseFloat(counterPrice);
        }

        this.socket.emit('respond_to_offer', responseData);
    }

    handleTyping() {
        if (!this.isConnected || !this.conversationId) return;

        // Send typing indicator
        this.socket.emit('typing', {
            conversation_id: this.conversationId,
            is_typing: true
        });

        // Clear existing timeout
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }

        // Set timeout to stop typing indicator
        this.typingTimeout = setTimeout(() => {
            this.stopTyping();
        }, 2000);
    }

    stopTyping() {
        if (!this.isConnected || !this.conversationId) return;

        this.socket.emit('typing', {
            conversation_id: this.conversationId,
            is_typing: false
        });

        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
            this.typingTimeout = null;
        }
    }

    loadMessages() {
        if (!this.conversationId) return;

        fetch(`/get_chat_messages/${this.conversationId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.displayMessages(data.messages);
                    this.updateConversationInfo(data.conversation);
                }
            })
            .catch(error => {
                console.error('Error loading messages:', error);
            });
    }

    displayMessages(messages) {
        const messagesList = document.getElementById('messagesList');
        if (!messagesList) return;

        messagesList.innerHTML = '';

        if (messages.length === 0) {
            messagesList.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fas fa-comments fa-3x mb-3"></i>
                    <h5>Belum ada pesan</h5>
                    <p>Mulai percakapan dengan mengirim pesan pertama!</p>
                </div>
            `;
            return;
        }

        messages.forEach(message => {
            this.displayMessage(message);
        });

        this.scrollToBottom();
    }

    displayMessage(message) {
        const messagesList = document.getElementById('messagesList');
        if (!messagesList) return;

        const messageElement = this.createMessageElement(message);
        messagesList.appendChild(messageElement);
    }

    createMessageElement(message) {
        const div = document.createElement('div');
        const isOwn = message.sender_id === this.currentUserId;
        
        div.className = `message mb-3 ${isOwn ? 'text-end' : 'text-start'}`;

        let messageContent = '';

        if (message.message_type === 'offer') {
            messageContent = this.createOfferMessage(message, isOwn);
        } else if (message.message_type === 'deal') {
            messageContent = this.createDealMessage(message, isOwn);
        } else {
            messageContent = this.createTextMessage(message, isOwn);
        }

        div.innerHTML = messageContent;
        return div;
    }

    createTextMessage(message, isOwn) {
        return `
            <div class="d-flex ${isOwn ? 'justify-content-end' : 'justify-content-start'}">
                <div class="message-bubble ${isOwn ? 'bg-primary text-white' : 'bg-light'} rounded p-3" style="max-width: 70%;">
                    <p class="mb-1">${this.escapeHtml(message.message)}</p>
                    <small class="opacity-75">
                        <i class="fas fa-clock me-1"></i>${message.created_at}
                    </small>
                </div>
            </div>
        `;
    }

    createOfferMessage(message, isOwn) {
        const isExpired = message.is_expired;
        const statusBadge = isExpired ? 
            '<span class="badge bg-danger">Expired</span>' : 
            '<span class="badge bg-success">Aktif</span>';

        let actionButtons = '';
        if (!isOwn && !isExpired && message.deal_accepted === null) {
            actionButtons = `
                <div class="mt-3">
                    <button class="btn btn-success btn-sm accept-offer-btn me-2" data-message-id="${message.id}">
                        <i class="fas fa-check"></i> Terima
                    </button>
                    <button class="btn btn-warning btn-sm counter-offer-btn me-2" data-message-id="${message.id}">
                        <i class="fas fa-exchange-alt"></i> Counter
                    </button>
                    <button class="btn btn-danger btn-sm reject-offer-btn" data-message-id="${message.id}">
                        <i class="fas fa-times"></i> Tolak
                    </button>
                </div>
            `;
        }

        let dealStatus = '';
        if (message.deal_accepted === true) {
            dealStatus = '<div class="mt-2 text-success"><i class="fas fa-check-circle"></i> Deal Diterima!</div>';
        } else if (message.deal_accepted === false) {
            dealStatus = '<div class="mt-2 text-danger"><i class="fas fa-times-circle"></i> Deal Ditolak</div>';
        }

        return `
            <div class="d-flex ${isOwn ? 'justify-content-end' : 'justify-content-start'}">
                <div class="card ${isOwn ? 'bg-primary text-white' : 'bg-light'}" style="max-width: 400px;">
                    <div class="card-body p-3">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <strong><i class="fas fa-hand-holding-usd"></i> Penawaran</strong>
                            ${statusBadge}
                        </div>
                        <div class="mb-2">
                            <h5 class="mb-1">Rp ${parseInt(message.offer_price || 0).toLocaleString()}</h5>
                            ${message.offer_quantity > 1 ? `<small>Jumlah: ${message.offer_quantity}</small>` : ''}
                        </div>
                        ${message.message ? `<p class="mb-2">${this.escapeHtml(message.message)}</p>` : ''}
                        <small class="opacity-75">
                            <i class="fas fa-clock me-1"></i>${message.created_at}
                        </small>
                        ${dealStatus}
                        ${actionButtons}
                    </div>
                </div>
            </div>
        `;
    }

    createDealMessage(message, isOwn) {
        return `
            <div class="d-flex ${isOwn ? 'justify-content-end' : 'justify-content-start'}">
                <div class="card bg-success text-white" style="max-width: 400px;">
                    <div class="card-body p-3">
                        <div class="mb-2">
                            <strong><i class="fas fa-handshake"></i> Deal Final</strong>
                        </div>
                        <p class="mb-2">${this.escapeHtml(message.message)}</p>
                        <small class="opacity-75">
                            <i class="fas fa-clock me-1"></i>${message.created_at}
                        </small>
                    </div>
                </div>
            </div>
        `;
    }

    showTypingIndicator(username, isTyping) {
        const typingIndicator = document.getElementById('typingIndicator');
        if (!typingIndicator) return;

        if (isTyping) {
            typingIndicator.innerHTML = `
                <div class="text-muted small">
                    <i class="fas fa-circle-notch fa-spin me-1"></i>
                    ${username} sedang mengetik...
                </div>
            `;
            typingIndicator.style.display = 'block';
        } else {
            typingIndicator.style.display = 'none';
        }
    }

    updateUserStatus(userId, isOnline) {
        const statusIndicators = document.querySelectorAll(`[data-user-id="${userId}"]`);
        statusIndicators.forEach(indicator => {
            if (isOnline) {
                indicator.classList.add('online');
                indicator.classList.remove('offline');
            } else {
                indicator.classList.add('offline');
                indicator.classList.remove('online');
            }
        });
    }

    updateConnectionStatus(isConnected) {
        const statusIndicator = document.getElementById('connectionStatus');
        if (statusIndicator) {
            if (isConnected) {
                statusIndicator.innerHTML = '<span class="badge bg-success">Terhubung</span>';
            } else {
                statusIndicator.innerHTML = '<span class="badge bg-danger">Terputus</span>';
            }
        }
    }

    updateConversationInfo(conversation) {
        // Update conversation status if needed
        const statusElement = document.getElementById('conversationStatus');
        if (statusElement && conversation) {
            let statusText = '';
            switch (conversation.status) {
                case 'active':
                    statusText = '<span class="badge bg-primary">💬 Aktif</span>';
                    break;
                case 'negotiating':
                    statusText = '<span class="badge bg-warning">🤝 Negosiasi</span>';
                    break;
                case 'completed':
                    statusText = '<span class="badge bg-success">✅ Selesai</span>';
                    break;
                default:
                    statusText = '<span class="badge bg-secondary">📝 ' + conversation.status + '</span>';
            }
            statusElement.innerHTML = statusText;
        }
    }

    scrollToBottom() {
        const messagesArea = document.getElementById('messagesArea');
        if (messagesArea) {
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }
    }

    showAlert(message, type) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'times-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    showUserNotification(message, type) {
        // Only show if user is not actively viewing the chat
        if (document.hidden) {
            this.showAlert(message, type);
        }
    }

    playNotificationSound() {
        // Only play sound if document is hidden (user not actively viewing)
        if (document.hidden) {
            // Create audio element for notification sound
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAABAA4mAAARTYoAAAAAABAACAAIABBHAAB1VwAAZeEAAAAAAAAAIAIAIAEAAQABAAEAAQABAAABAAABAAABAAAIAAgACAAIAAgACAAIAAgACAAICAgACAAIAAgACAAIAAgACAAIAAgACAAICAgACAAIAAgACAAIAAgACAAIAAgACAAICAAAUElTVAAAAABQQU5VCAAAAAQAADg=');
            audio.volume = 0.3;
            audio.play().catch(() => {
                // Ignore errors (browser might block autoplay)
            });
        }
    }

    showCounterOfferModal(messageId) {
        // Create modal for counter offer
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">💰 Counter Offer</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Harga Counter (Rp)</label>
                            <input type="number" id="counterPrice" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Pesan Tambahan</label>
                            <textarea id="counterMessage" class="form-control" rows="3" placeholder="Jelaskan alasan counter offer Anda..."></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                        <button type="button" class="btn btn-primary" onclick="chatSystem.submitCounterOffer('${messageId}')">Kirim Counter</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        // Remove modal from DOM when hidden
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    submitCounterOffer(messageId) {
        const counterPrice = document.getElementById('counterPrice').value;
        const counterMessage = document.getElementById('counterMessage').value;
        
        if (!counterPrice) {
            this.showAlert('Masukkan harga counter offer', 'warning');
            return;
        }
        
        this.respondToOffer(messageId, 'counter', counterPrice);
        
        // Hide modal
        const modal = document.querySelector('.modal.show');
        if (modal) {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            bootstrapModal.hide();
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Cleanup when page is unloaded
    destroy() {
        if (this.socket) {
            this.leaveConversation();
            this.socket.disconnect();
        }
        
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }
    }
}

// Initialize chat system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on a chat page
    if (document.getElementById('messageForm') || document.getElementById('messagesArea')) {
        window.chatSystem = new RealtimeChatSystem();
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (window.chatSystem) {
                window.chatSystem.destroy();
            }
        });
    }
});

// Quick message functions for buttons
function sendQuickMessage(message) {
    if (window.chatSystem) {
        document.getElementById('messageInput').value = message;
        window.chatSystem.sendMessage();
    }
}

function sendQuickOffer() {
    const modal = document.getElementById('offerModal');
    if (modal) {
        new bootstrap.Modal(modal).show();
    }
}

function submitOffer() {
    const price = document.getElementById('offerPrice').value;
    const quantity = document.getElementById('offerQuantity').value || 1;
    const message = document.getElementById('offerMessage').value;
    
    if (!price) {
        window.chatSystem.showAlert('Masukkan harga penawaran', 'warning');
        return;
    }
    
    // Set offer data in form
    document.getElementById('messageInput').value = message || `Penawaran: Rp ${parseInt(price).toLocaleString()}`;
    document.getElementById('messageType').value = 'offer';
    document.getElementById('offerPrice').dataset.value = price;
    document.getElementById('offerQuantity').dataset.value = quantity;
    
    // Send via chat system
    window.chatSystem.sendMessage();
    
    // Hide modal and reset form
    const modal = bootstrap.Modal.getInstance(document.getElementById('offerModal'));
    modal.hide();
    document.getElementById('offerForm').reset();
}