<template>
  <div class="chat-container">
    <!-- Header -->
    <header class="chat-header">
      <div class="header-top">
        <button @click="goBack" class="back-button">
          <ArrowLeft class="back-icon" />
        </button>
        <div class="header-title">
          <MessageCircle class="title-icon" />
          <h1 class="title-text">Chat en Tiempo Real</h1>
        </div>
        <div class="status-indicator" :class="{ connected: isConnected, disconnected: !isConnected }">
          <span class="status-dot"></span>
          <span class="status-text">{{ isConnected ? 'Conectado' : 'Desconectado' }}</span>
        </div>
      </div>
    </header>

    <!-- Chat Area -->
    <div class="chat-area">
      <!-- Empty State -->
      <div v-if="messages.length === 0" class="empty-state">
        <div class="empty-icon">
          <MessageCircle class="empty-lucide" />
        </div>
        <p class="empty-title">Inicia una conversación</p>
        <p class="empty-desc">Los mensajes aparecerán aquí</p>
      </div>

      <!-- Messages -->
      <div v-else ref="chatContainer" class="messages-container">
        <!-- Connection Status -->
        <div v-if="!isConnected" class="status-message">
          <div class="status-icon">
            <WifiOff class="wifi-icon" />
          </div>
          <p>Conectando al chat...</p>
        </div>

        <!-- Messages List -->
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="message-wrapper"
          :class="{ 'message-mine': msg.isMine }"
        >
          <div class="message-bubble" :class="{ 'bubble-mine': msg.isMine }">
            <p v-if="!msg.isMine" class="message-sender">{{ msg.sender }}</p>
            <p class="message-text">{{ msg.text }}</p>
            <p class="message-time">{{ msg.time }}</p>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="otherTyping" class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <span class="typing-text">{{ otherTyping }} está escribiendo...</span>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-area">
      <input
        v-model="input"
        type="text"
        placeholder="Escribe un mensaje..."
        class="message-input"
        @keyup.enter="sendMessage"
        @keydown="notifyTyping"
      />
      <button
        @click="sendMessage"
        :disabled="!input.trim() || !isConnected"
        class="send-button"
      >
        <Send class="send-icon" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { MessageCircle, WifiOff, ArrowLeft, Send } from 'lucide-vue-next'

const auth = useAuthStore()
const router = useRouter()
const user = auth.user?.nombre || 'Usuario'

const ws = ref(null)
const messages = ref([])
const input = ref('')
const chatContainer = ref(null)
const isConnected = ref(false)
const otherTyping = ref('')
const lastTypingTime = ref(0)

const goBack = () => {
  router.back()
}

const getTime = () => {
  const now = new Date()
  return now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const connect = () => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  // Determinar protocolo basado en la URL del API, no en window.location
  const isSecure = apiUrl.startsWith('https')
  const protocol = isSecure ? 'wss:' : 'ws:'
  const host = apiUrl.replace('https://', '').replace('http://', '').replace(/\/$/, '')
  
  ws.value = new WebSocket(`${protocol}//${host}/chat/ws`)

  ws.value.onopen = () => {
    isConnected.value = true
    console.log('✅ Conectado al chat en tiempo real')
  }

  ws.value.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      
      if (msg.type === 'typing') {
        otherTyping.value = msg.sender !== user ? msg.sender : ''
        return
      }

      messages.value.push({
        sender: msg.sender,
        text: msg.text,
        time: msg.time || getTime(),
        isMine: msg.sender === user
      })
      
      scrollToBottom()
    } catch (e) {
      console.error('Error procesando mensaje:', e)
    }
  }

  ws.value.onclose = () => {
    isConnected.value = false
    console.log('🔴 Desconectado del chat')
  }

  ws.value.onerror = (error) => {
    console.error('❌ Error WebSocket:', error)
    isConnected.value = false
  }
}

const sendMessage = () => {
  if (!input.value.trim() || !isConnected.value) return
  
  const message = {
    type: 'message',
    sender: user,
    text: input.value.trim(),
    time: getTime()
  }
  
  ws.value.send(JSON.stringify(message))
  input.value = ''
}

const notifyTyping = () => {
  const now = Date.now()
  if (now - lastTypingTime.value > 1000) {
    lastTypingTime.value = now
    const typingMsg = {
      type: 'typing',
      sender: user
    }
    ws.value.send(JSON.stringify(typingMsg))
  }
}

const disconnect = () => {
  if (ws.value) {
    ws.value.close()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  connect()
})

onBeforeUnmount(() => {
  disconnect()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #e2e8f0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  overflow: hidden;
}

/* ========== HEADER ========== */
.chat-header {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
}

.header-top {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.back-button {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.back-button:hover {
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.back-icon {
  width: 20px;
  height: 20px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: #10b981;
}

.title-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  flex-shrink: 0;
}

.status-indicator.connected {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-indicator.disconnected {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.status-indicator.connected .status-dot {
  background: #10b981;
}

.status-indicator.disconnected .status-dot {
  background: #ef4444;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ========== CHAT AREA ========== */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #64748b;
  padding: 2rem;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.empty-lucide {
  width: 40px;
  height: 40px;
  color: #10b981;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 0.5rem;
}

.empty-desc {
  font-size: 0.9rem;
  color: #94a3b8;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  justify-content: center;
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  color: #ef4444;
  font-size: 0.9rem;
}

.status-icon {
  display: flex;
  align-items: center;
}

.wifi-icon {
  width: 16px;
  height: 16px;
}

/* ========== MESSAGES ========== */
.message-wrapper {
  display: flex;
  justify-content: flex-start;
  animation: slideIn 0.3s ease-out;
}

.message-wrapper.message-mine {
  justify-content: flex-end;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-bubble {
  max-width: 60%;
  padding: 0.75rem 1rem;
  border-radius: 16px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  word-wrap: break-word;
}

.message-bubble.bubble-mine {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
}

.message-sender {
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.message-bubble.bubble-mine .message-sender {
  color: rgba(255, 255, 255, 0.8);
}

.message-text {
  font-size: 0.95rem;
  line-height: 1.4;
  margin: 0;
  color: #e2e8f0;
}

.message-bubble.bubble-mine .message-text {
  color: white;
}

.message-time {
  font-size: 0.7rem;
  margin-top: 0.25rem;
  color: #64748b;
  margin: 0;
}

.message-bubble.bubble-mine .message-time {
  color: rgba(255, 255, 255, 0.7);
}

/* ========== TYPING INDICATOR ========== */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% { opacity: 0.5; transform: translateY(0); }
  30% { opacity: 1; transform: translateY(-10px); }
}

.typing-text {
  font-size: 0.85rem;
  color: #94a3b8;
  margin-left: 0.5rem;
}

/* ========== INPUT AREA ========== */
.input-area {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.8);
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.message-input {
  flex: 1;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.message-input::placeholder {
  color: #64748b;
}

.message-input:focus {
  outline: none;
  border-color: rgba(16, 185, 129, 0.5);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.send-button {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  flex-shrink: 0;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
}

.send-button:disabled {
  background: rgba(148, 163, 184, 0.3);
  cursor: not-allowed;
  box-shadow: none;
}

.send-icon {
  width: 20px;
  height: 20px;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .title-text {
    font-size: 1.25rem;
  }

  .status-text {
    display: none;
  }

  .back-button {
    width: 40px;
    height: 40px;
  }

  .back-icon {
    width: 18px;
    height: 18px;
  }

  .message-bubble {
    max-width: 80%;
  }
}

@media (max-width: 480px) {
  .back-button {
    width: 36px;
    height: 36px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .title-text {
    font-size: 1rem;
  }

  .title-icon {
    width: 20px;
    height: 20px;
  }

  .message-bubble {
    max-width: 90%;
  }

  .input-area {
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .send-button {
    width: 40px;
    height: 40px;
  }

  .send-icon {
    width: 18px;
    height: 18px;
  }
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}
</style>
