
// Real-time Chat System
class ChatSystem {
    constructor() {
        this.refreshInterval = 3000; // 3 seconds
        this.lastMessageId = 0;
        this.conversationId = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startPeriodicRefresh();
        this.updateOnlineStatus('online');
        
        // Handle page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.updateOnlineStatus('away');
            } else {
                this.updateOnlineStatus('online');
                this.refreshMessages();
            }
        });

        // Handle beforeunload
        window.addEventListener('beforeunload', () => {
            this.updateOnlineStatus('offline');
        });
    }

    setupEventListeners() {
        // Chat form submission
        const chatForm = document.getElementById('chatForm');
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }

        // Auto-resize textarea
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        }

        // Offer/Deal buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('accept-offer-btn')) {
                this.respondToOffer(e.target.dataset.messageId, 'accept');
            }
            if (e.target.classList.contains('reject-offer-btn')) {
                this.respondToOffer(e.target.dataset.messageId, 'reject');
            }
        });
    }

    updateOnlineStatus(status) {
        fetch('/update_online_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: status })
        }).catch(err => console.log('Status update failed:', err));
    }

    startPeriodicRefresh() {
        setInterval(() => {
            if (!document.hidden) {
                this.refreshMessages();
                this.updateUnreadCount();
            }
        }, this.refreshInterval);
    }

    sendMessage() {
        const form = document.getElementById('chatForm');
        const formData = new FormData(form);
        const messageInput = document.getElementById('messageInput');
        
        if (!messageInput.value.trim()) {
            this.showAlert('Pesan tidak boleh kosong', 'warning');
            return;
        }

        // Disable send button temporarily
        const sendBtn = form.querySelector('button[type="submit"]');
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Mengirim...';

        fetch('/send_chat_message', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageInput.value = '';
                messageInput.style.height = 'auto';
                this.conversationId = data.conversation_id;
                this.refreshMessages();
                this.showAlert(data.message, 'success');
            } else {
                this.showAlert(data.error, 'error');
            }
        })
        .catch(error => {
            this.showAlert('Gagal mengirim pesan', 'error');
        })
        .finally(() => {
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Kirim';
        });
    }

    refreshMessages() {
        if (!this.conversationId) return;

        fetch(`/get_chat_messages/${this.conversationId}`)
        .then(response => response.json())
        .then(data => {
            if (data.messages) {
                this.displayMessages(data.messages);
                this.scrollToBottom();
            }
        })
        .catch(error => console.log('Failed to refresh messages:', error));
    }

    displayMessages(messages) {
        const container = document.getElementById('messagesContainer');
        if (!container) return;

        container.innerHTML = '';
        
        messages.forEach(message => {
            const messageEl = this.createMessageElement(message);
            container.appendChild(messageEl);
        });
    }

    createMessageElement(message) {
        const div = document.createElement('div');
        const isOwn = message.sender_id == currentUserId; // Assume currentUserId is available globally
        
        div.className = `message ${isOwn ? 'message-own' : 'message-other'} mb-3`;
        
        let messageContent = `
            <div class="message-bubble ${isOwn ? 'bg-primary text-white' : 'bg-light'}">
                <div class="message-header">
                    <small class="text-muted">${message.sender_name}</small>
                    <small class="text-muted ms-2">${message.created_at}</small>
                </div>
                <div class="message-content">${this.formatMessage(message)}</div>
            </div>
        `;

        // Add offer/deal controls if applicable
        if (message.message_type === 'offer' && !isOwn && !message.deal_accepted && !message.is_expired) {
            messageContent += this.createOfferControls(message);
        }

        div.innerHTML = messageContent;
        return div;
    }

    formatMessage(message) {
        let content = message.message.replace(/\n/g, '<br>');
        
        if (message.message_type === 'offer') {
            content += `<div class="offer-details mt-2 p-2 bg-warning bg-opacity-25 rounded">
                <strong>💰 Penawaran: Rp ${message.offer_price?.toLocaleString()}</strong>
                ${message.expires_at ? `<br><small>⏰ Berlaku hingga: ${message.expires_at}</small>` : ''}
            </div>`;
        }

        if (message.message_type === 'deal') {
            const status = message.deal_accepted === true ? '✅ Diterima' : 
                         message.deal_accepted === false ? '❌ Ditolak' : '⏳ Menunggu';
            content += `<div class="deal-status mt-2 p-2 bg-info bg-opacity-25 rounded">
                <strong>🤝 Deal Status: ${status}</strong>
            </div>`;
        }

        return content;
    }

    createOfferControls(message) {
        return `
            <div class="offer-controls mt-2">
                <button class="btn btn-success btn-sm accept-offer-btn me-2" data-message-id="${message.id}">
                    <i class="fas fa-check"></i> Terima
                </button>
                <button class="btn btn-danger btn-sm reject-offer-btn" data-message-id="${message.id}">
                    <i class="fas fa-times"></i> Tolak
                </button>
            </div>
        `;
    }

    respondToOffer(messageId, action) {
        const formData = new FormData();
        formData.append('message_id', messageId);
        formData.append('action', action);
        
        fetch('/respond_to_offer', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showAlert(data.message, 'success');
                this.refreshMessages();
            } else {
                this.showAlert(data.error, 'error');
            }
        })
        .catch(error => {
            this.showAlert('Gagal merespons penawaran', 'error');
        });
    }

    updateUnreadCount() {
        fetch('/get_unread_chat_count')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('unreadChatBadge');
            if (badge) {
                if (data.unread_count > 0) {
                    badge.textContent = data.unread_count;
                    badge.style.display = 'inline';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => console.log('Failed to update unread count:', error));
    }

    scrollToBottom() {
        const container = document.getElementById('messagesContainer');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    showAlert(message, type) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
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
}

// Initialize chat system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('chatForm') || document.getElementById('messagesContainer')) {
        window.chatSystem = new ChatSystem();
    }
});

// Online status indicator
function updateUserOnlineStatus() {
    const statusIndicators = document.querySelectorAll('.user-online-status');
    statusIndicators.forEach(indicator => {
        const userId = indicator.dataset.userId;
        // You can fetch user online status here if needed
        // For now, just add visual indicators
    });
}

// Call periodically
setInterval(updateUserOnlineStatus, 30000); // Every 30 seconds
