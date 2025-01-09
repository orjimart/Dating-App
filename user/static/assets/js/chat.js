// static/js/chat.js

class ChatManager {
    constructor(roomId, currentUserId) {
        this.roomId = roomId;
        this.currentUserId = currentUserId;
        this.socket = null;
        this.messageQueue = [];
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        this.initializeSocket();
        this.initializeEventListeners();
    }

    initializeSocket() {
        this.socket = new WebSocket(
            `ws://${window.location.host}/ws/chat/${this.roomId}/`
        );

        this.socket.onopen = () => {
            console.log('WebSocket connected');
            this.isConnecting = false;
            this.reconnectAttempts = 0;
            // Send any queued messages
            this.processMessageQueue();
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            this.attemptReconnect();
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleIncomingMessage(data);
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    attemptReconnect() {
        if (this.isConnecting || this.reconnectAttempts >= this.maxReconnectAttempts) {
            return;
        }

        this.isConnecting = true;
        this.reconnectAttempts++;

        setTimeout(() => {
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            this.initializeSocket();
        }, 3000 * this.reconnectAttempts);
    }

    initializeEventListeners() {
        // Message form submission
        document.getElementById('chat-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleTextMessage();
        });

        // File uploads
        document.getElementById('imageInput').addEventListener('change', (e) => {
            this.handleFileUpload(e, 'image');
        });

        document.getElementById('videoInput').addEventListener('change', (e) => {
            this.handleFileUpload(e, 'video');
        });

        // Emoji picker
        const emojiButton = document.getElementById('emoji-btn');
        const emojiPicker = new EmojiPicker({
            onEmojiSelect: (emoji) => {
                const input = document.querySelector('.chat-input');
                input.value += emoji.native;
                input.focus();
            }
        });

        emojiButton.addEventListener('click', () => {
            emojiPicker.togglePicker(emojiButton);
        });
    }

    async handleFileUpload(event, type) {
        const file = event.target.files[0];
        if (!file) return;

        // Validate file size
        const maxSize = type === 'image' ? 5 * 1024 * 1024 : 50 * 1024 * 1024; // 5MB for images, 50MB for videos
        if (file.size > maxSize) {
            alert(`File too large. Maximum size is ${maxSize / (1024 * 1024)}MB`);
            return;
        }

        // Show upload progress
        this.showUploadProgress();

        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);
        formData.append('room_id', this.roomId);

        try {
            const response = await fetch('/chat/upload/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                },
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            this.sendMessage({
                type: type,
                file_url: data.file_url,
                message: '',
            });
        } catch (error) {
            console.error('Upload error:', error);
            alert('Failed to upload file. Please try again.');
        } finally {
            this.hideUploadProgress();
        }
    }

    handleTextMessage() {
        const input = document.querySelector('.chat-input');
        const message = input.value.trim();
        
        if (message) {
            this.sendMessage({
                type: 'text',
                message: message,
            });
            input.value = '';
        }
    }

    sendMessage(messageData) {
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(messageData));
        } else {
            // Queue message if socket is not open
            this.messageQueue.push(messageData);
            if (!this.isConnecting) {
                this.attemptReconnect();
            }
        }
    }

    processMessageQueue() {
        while (this.messageQueue.length > 0) {
            const messageData = this.messageQueue.shift();
            this.sendMessage(messageData);
        }
    }

    handleIncomingMessage(data) {
        const chatContainer = document.querySelector('.chat-conversation-list');
        const messageElement = this.createMessageElement(data);
        chatContainer.appendChild(messageElement);
        this.scrollToBottom();
        
        // Mark message as read if it's not from current user
        if (data.sender_id !== this.currentUserId) {
            this.markMessageAsRead(data.message_id);
        }
    }

    createMessageElement(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${data.sender_id === this.currentUserId ? 'right' : 'left'}`;
        
        let contentHtml = '';
        switch (data.type) {
            case 'image':
                contentHtml = `<img src="${data.file_url}" class="chat-image" alt="Shared image">`;
                break;
            case 'video':
                contentHtml = `
                    <video controls class="chat-video">
                        <source src="${data.file_url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>`;
                break;
            default:
                contentHtml = `<p>${this.escapeHtml(data.message)}</p>`;
        }

        messageDiv.innerHTML = `
            <div class="conversation-list">
                <div class="ctext-wrap">
                    ${contentHtml}
                    <p class="chat-time mb-0">
                        <i class="mdi mdi-clock-outline me-1"></i>
                        ${this.formatTimestamp(data.timestamp)}
                    </p>
                </div>
            </div>`;

        return messageDiv;
    }

    async markMessageAsRead(messageId) {
        try {
            await fetch(`/chat/mark-read/${messageId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                    'Content-Type': 'application/json',
                }
            });
        } catch (error) {
            console.error('Error marking message as read:', error);
        }
    }

    // Utility methods
    scrollToBottom() {
        const chatContainer = document.querySelector('.chat-conversation-list');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    showUploadProgress() {
        // Implement upload progress UI
    }

    hideUploadProgress() {
        // Hide upload progress UI
    }
}

// Initialize chat when document is ready
document.addEventListener('DOMContentLoaded', () => {
    const roomId = document.querySelector('.chat-room').dataset.roomId;
    const currentUserId = document.querySelector('body').dataset.userId;
    window.chatManager = new ChatManager(roomId, currentUserId);
});