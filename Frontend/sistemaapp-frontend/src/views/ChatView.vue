<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Header -->
    <div class="bg-white shadow-lg p-4 flex justify-between items-center border-b-4 border-green-500">
      <h2 class="text-2xl font-bold text-green-600 flex items-center gap-2">
        💬 Chat en tiempo real
      </h2>
      <div class="flex items-center gap-3">
        <span
          class="inline-flex items-center gap-1 px-3 py-1 rounded-full"
          :class="isConnected ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
        >
          <span :class="isConnected ? 'text-green-500' : 'text-red-500'" class="w-2 h-2 rounded-full inline-block"></span>
          {{ isConnected ? 'Conectado' : 'Desconectado' }}
        </span>
        <button
          @click="disconnect"
          class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition"
        >
          Desconectar
        </button>
      </div>
    </div>

    <!-- Contenedor de mensajes -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
      <!-- Estado de conexión -->
      <div v-if="!isConnected" class="text-center py-8">
        <p class="text-gray-500 text-lg">🔌 Conectando al chat...</p>
      </div>

      <!-- Mensajes -->
      <div
        v-for="(msg, i) in messages"
        :key="i"
        class="flex transition-all"
        :class="msg.isMine ? 'justify-end' : 'justify-start'"
      >
        <div
          class="max-w-xs px-4 py-3 rounded-lg shadow-md"
          :class="msg.isMine 
            ? 'bg-green-500 text-white rounded-br-none' 
            : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'"
        >
          <p v-if="!msg.isMine" class="text-xs font-semibold text-gray-600 mb-1">
            {{ msg.sender }}
          </p>
          <p class="text-sm leading-relaxed break-words">{{ msg.text }}</p>
          <p class="text-xs mt-1 opacity-70">{{ msg.time }}</p>
        </div>
      </div>

      <!-- Indicador de escritura -->
      <div v-if="otherTyping" class="flex items-center gap-2 text-gray-500 text-sm">
        <span class="animate-pulse">✏️</span>
        <span>{{ otherTyping }} está escribiendo...</span>
      </div>
    </div>

    <!-- Input de mensaje -->
    <div class="p-4 bg-white border-t-2 border-gray-200 flex gap-3">
      <input
        v-model="input"
        type="text"
        placeholder="Escribe un mensaje..."
        class="flex-1 border-2 border-gray-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-green-400 focus:border-transparent outline-none transition"
        @keyup.enter="sendMessage"
        @keydown="notifyTyping"
      />
      <button
        @click="sendMessage"
        :disabled="!input.trim() || !isConnected"
        class="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition flex items-center gap-2"
      >
        📤 Enviar
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const user = auth.user?.nombre || 'Usuario'

const ws = ref(null)
const messages = ref([])
const input = ref('')
const chatContainer = ref(null)
const isConnected = ref(false)
const otherTyping = ref('')
const lastTypingTime = ref(0)

const getTime = () => {
  const now = new Date()
  return now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const connect = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = import.meta.env.VITE_API_URL.replace('https://', '').replace('http://', '')
  
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
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
