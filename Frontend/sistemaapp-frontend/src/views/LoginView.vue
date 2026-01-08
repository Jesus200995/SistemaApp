<template>
  <div class="login-container">
    <!-- Animación de carga con flor girando -->
    <transition name="fade-loading">
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-container">
          <svg class="rotating-flower" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Tallo -->
            <line x1="100" y1="100" x2="100" y2="30" stroke="#22C55E" stroke-width="3" stroke-linecap="round"/>
            
            <!-- Pétalos de flor -->
            <circle cx="100" cy="30" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="130" cy="50" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="145" cy="85" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="130" cy="120" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="100" cy="140" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="70" cy="120" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="55" cy="85" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            <circle cx="70" cy="50" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
            
            <!-- Centro de la flor -->
            <circle cx="100" cy="100" r="16" fill="#FCD34D"/>
          </svg>
          <p class="loading-text">Cargando...</p>
        </div>
      </div>
    </transition>

    <!-- Fondo animado -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Contenido principal -->
    <div class="login-content">
      <!-- Logo y título -->
      <div class="logo-section">
        <!-- Animación de maceta con flor -->
        <div class="flowerpot-animation">
          <svg viewBox="0 0 200 240" class="flowerpot-svg">
            <!-- Maceta verde oscuro -->
            <path d="M 60 120 L 50 180 Q 50 195 65 200 L 135 200 Q 150 195 150 180 L 140 120" 
                  fill="#15803D" stroke="#166534" stroke-width="2"/>
            <ellipse cx="100" cy="120" rx="50" ry="12" fill="#22C55E" stroke="#166534" stroke-width="2"/>
            
            <!-- Tierra en la maceta -->
            <ellipse cx="100" cy="125" rx="45" ry="10" fill="#1B4D2F" opacity="0.9"/>
            
            <!-- Tallo principal verde -->
            <path d="M 100 125 Q 98 90 98 50" stroke="#16A34A" stroke-width="4" fill="none" stroke-linecap="round"/>
            
            <!-- Hoja grande izquierda 1 -->
            <ellipse cx="70" cy="100" rx="22" ry="10" fill="#22C55E" transform="rotate(-45 70 100)" opacity="1"/>
            
            <!-- Hoja grande derecha 1 -->
            <ellipse cx="130" cy="95" rx="22" ry="10" fill="#22C55E" transform="rotate(45 130 95)" opacity="1"/>
            
            <!-- Hoja mediana izquierda 2 -->
            <ellipse cx="68" cy="70" rx="18" ry="8" fill="#10B981" transform="rotate(-40 68 70)" opacity="0.95"/>
            
            <!-- Hoja mediana derecha 2 -->
            <ellipse cx="132" cy="65" rx="18" ry="8" fill="#10B981" transform="rotate(40 132 65)" opacity="0.95"/>
            
            <!-- Hoja pequeña izquierda 3 -->
            <ellipse cx="72" cy="45" rx="14" ry="6" fill="#059669" transform="rotate(-35 72 45)" opacity="0.9"/>
            
            <!-- Hoja pequeña derecha 3 -->
            <ellipse cx="128" cy="40" rx="14" ry="6" fill="#059669" transform="rotate(35 128 40)" opacity="0.9"/>
            
            <!-- Flor principal - flores circulares verdes vibrantes -->
            <!-- Grupo 1: 3 flores arriba -->
            <g class="flower-group">
              <!-- Flor izquierda -->
              <circle cx="75" cy="28" r="6" fill="#10B981" class="flower-petal-1"/>
              <circle cx="70" cy="20" r="6" fill="#10B981" class="flower-petal-1"/>
              <circle cx="78" cy="20" r="6" fill="#10B981" class="flower-petal-1"/>
              <circle cx="72" cy="24" r="4" fill="#FBBF24"/>
              
              <!-- Flor centro -->
              <circle cx="100" cy="20" r="6" fill="#22C55E" class="flower-petal-2"/>
              <circle cx="94" cy="14" r="6" fill="#22C55E" class="flower-petal-2"/>
              <circle cx="106" cy="14" r="6" fill="#22C55E" class="flower-petal-2"/>
              <circle cx="100" cy="10" r="6" fill="#22C55E" class="flower-petal-2"/>
              <circle cx="100" cy="28" r="6" fill="#22C55E" class="flower-petal-2"/>
              <circle cx="100" cy="19" r="4" fill="#FCD34D"/>
              
              <!-- Flor derecha -->
              <circle cx="125" cy="28" r="6" fill="#059669" class="flower-petal-3"/>
              <circle cx="122" cy="20" r="6" fill="#059669" class="flower-petal-3"/>
              <circle cx="128" cy="20" r="6" fill="#059669" class="flower-petal-3"/>
              <circle cx="125" cy="24" r="4" fill="#FBBF24"/>
            </g>
          </svg>
        </div>
        <h1 class="app-title">Sistema de Administración</h1>
        <p class="app-subtitle">SEMBRANDO VIDA</p>
      </div>

      <!-- Tarjeta de login -->
      <div class="login-card">
        <h2 class="login-title">Inicia Sesión</h2>
        <p class="login-subtitle">Ingresa tus credenciales</p>

        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Campo Email -->
          <div class="form-group">
            <label for="email" class="form-label">Correo Electrónico</label>
            <div class="input-wrapper">
              <Mail class="input-icon" />
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="tu@correo.com"
                class="form-input"
                required
              />
            </div>
          </div>

          <!-- Campo Contraseña -->
          <div class="form-group">
            <label for="password" class="form-label">Contraseña</label>
            <div class="input-wrapper">
              <Lock class="input-icon" />
              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="••••••••"
                class="form-input"
                required
              />
            </div>
          </div>

          <!-- Recordarme -->
          <div class="remember-me">
            <input type="checkbox" id="remember" class="checkbox-input" />
            <label for="remember" class="checkbox-label">Recuérdame</label>
          </div>

          <!-- Mensaje de error -->
          <div v-if="auth.error" class="error-message">
            <AlertCircle class="error-icon" />
            <span>{{ auth.error }}</span>
          </div>

          <!-- Botón enviar -->
          <button type="submit" class="submit-button">
            <span>Iniciar Sesión</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="divider">
          <span>¿No tienes cuenta?</span>
        </div>

        <!-- Link a registro -->
        <router-link to="/register" class="register-button">
          Crear una cuenta nueva
        </router-link>

        <!-- Botón temporal para crear admin (solo desarrollo) -->
        <button
          @click="crearAdmin"
          type="button"
          class="admin-button"
        >
          <span>⚙️ Crear administrador (desarrollo)</span>
        </button>
      </div>

      <!-- Footer -->
      <div class="login-footer">
        <p>© 2025 <span class="footer-highlight">Sistema de Administración</span>. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { Mail, Lock, AlertCircle } from 'lucide-vue-next'
import axios from 'axios'
import { getSecureApiUrl } from '../utils/api'
import Swal from 'sweetalert2'

const email = ref('')
const password = ref('')
const isLoading = ref(false)
const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  isLoading.value = true
  try {
    const ok = await auth.login(email.value, password.value)
    if (ok) {
      // Esperar un poco para que la animación sea visible
      await new Promise(resolve => setTimeout(resolve, 1500))
      router.push('/dashboard')
    }
  } finally {
    isLoading.value = false
  }
}

const crearAdmin = async () => {
  try {
    const nombre = prompt('Nombre del nuevo administrador:')
    if (!nombre) return

    const emailAdmin = prompt('Correo del administrador:')
    if (!emailAdmin) return

    const passwordAdmin = prompt('Contraseña del administrador (mínimo 6 caracteres):')
    if (!passwordAdmin) return

    if (!nombre || !emailAdmin || !passwordAdmin) {
      await Swal.fire('⚠️ Campos incompletos', 'Debes llenar todos los campos', 'warning')
      return
    }

    if (passwordAdmin.length < 6) {
      await Swal.fire('⚠️ Contraseña muy corta', 'La contraseña debe tener al menos 6 caracteres', 'warning')
      return
    }

    // Usar el endpoint especial para crear admin inicial
    const apiUrl = getSecureApiUrl()
    await axios.post(`${apiUrl}/auth/setup-admin`, {
      nombre,
      email: emailAdmin.trim().toLowerCase(),
      password: passwordAdmin,
      rol: 'admin'
    })

    await Swal.fire('✅ Administrador creado', 'Ya puedes iniciar sesión con este usuario', 'success')
  } catch (err) {
    const errorMsg = err.response?.data?.detail || 'No se pudo crear el usuario'
    await Swal.fire('❌ Error', errorMsg, 'error')
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.login-container {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 2rem 0;
}

/* ========== BACKGROUND BLOBS ========== */
.background-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.blob {
  position: absolute;
  opacity: 0.3;
  filter: blur(100px);
  mix-blend-mode: multiply;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #bbf7d0, #86efac);
  border-radius: 50%;
  top: -200px;
  left: -200px;
  animation: blob-animate 8s ease-in-out infinite;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #a7f3d0, #6ee7b7);
  border-radius: 50%;
  top: 50%;
  right: -150px;
  animation: blob-animate 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #bbf7d0, #34d399);
  border-radius: 50%;
  bottom: -100px;
  left: 50%;
  animation: blob-animate 12s ease-in-out infinite;
}

@keyframes blob-animate {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -50px); }
}

/* ========== CONTENT ========== */
.login-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: clamp(280px, 85vw, 420px);
  padding: clamp(0.5rem, 2vw, 1rem) clamp(0.4rem, 2vw, 1rem);
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ========== LOGO SECTION ========== */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: clamp(0.6rem, 2vw, 1rem);
  text-align: center;
  width: 100%;
}

/* Animación de maceta con flor */
.flowerpot-animation {
  width: clamp(60px, 12vw, 90px);
  height: clamp(75px, 15vw, 110px);
  margin-bottom: clamp(0.4rem, 1.5vw, 0.8rem);
  display: flex;
  align-items: center;
  justify-content: center;
}

.flowerpot-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 12px rgba(34, 197, 94, 0.25));
}

.flower-group {
  animation: bloomFlowers 2.5s ease-in-out infinite;
}

.flower-petal-1 {
  animation: pulsePetal1 2s ease-in-out infinite;
}

.flower-petal-2 {
  animation: pulsePetal2 2s ease-in-out infinite;
}

.flower-petal-3 {
  animation: pulsePetal3 2s ease-in-out infinite;
}

@keyframes bloomFlowers {
  0%, 100% {
    opacity: 0.9;
  }
  50% {
    opacity: 1;
  }
}

@keyframes pulsePetal1 {
  0%, 100% {
    r: 5.5px;
    fill: #10B981;
  }
  50% {
    r: 6.5px;
    fill: #22C55E;
  }
}

@keyframes pulsePetal2 {
  0%, 100% {
    r: 5.5px;
    fill: #22C55E;
  }
  50% {
    r: 6.5px;
    fill: #34D399;
  }
}

@keyframes pulsePetal3 {
  0%, 100% {
    r: 5.5px;
    fill: #059669;
  }
  50% {
    r: 6.5px;
    fill: #10B981;
  }
}

.app-title {
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 600;
  background: linear-gradient(90deg, #15803d 0%, #166534 25%, #15803d 50%, #166534 75%, #15803d 100%);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.2rem;
  letter-spacing: -0.02em;
  line-height: 1.2;
  animation: gradient-flow 4s ease-in-out infinite;
}

@keyframes gradient-flow {
  0% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
  100% {
    background-position: 0% center;
  }
}

.app-subtitle {
  font-size: clamp(0.65rem, 1.5vw, 0.85rem);
  color: #84cc16;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding-bottom: clamp(0.35rem, 1vw, 0.5rem);
  border-bottom: 1.5px solid rgba(132, 204, 22, 0.3);
  display: inline-block;
}

/* ========== LOGIN CARD ========== */
.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: clamp(14px, 3vw, 20px);
  padding: clamp(0.7rem, 2.5vw, 1.25rem) clamp(0.6rem, 2vw, 1rem);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(22, 163, 74, 0.1), 0 0 1px rgba(16, 185, 129, 0.2);
  margin-bottom: clamp(0.4rem, 1.5vw, 0.6rem);
}

.login-title {
  font-size: clamp(0.95rem, 2.5vw, 1.2rem);
  font-weight: 700;
  color: #15803d;
  margin-bottom: clamp(0.2rem, 0.8vw, 0.35rem);
  text-align: center;
  letter-spacing: -0.01em;
}

.login-subtitle {
  font-size: clamp(0.75rem, 1.8vw, 0.9rem);
  color: #166534;
  text-align: center;
  margin-bottom: clamp(0.9rem, 2.5vw, 1.4rem);
  font-weight: 400;
}

/* ========== FORM ========== */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-label {
  font-size: clamp(0.6rem, 1.2vw, 0.75rem);
  font-weight: 600;
  color: #15803d;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: clamp(8px, 1.5vw, 14px);
  width: clamp(14px, 2vw, 20px);
  height: clamp(14px, 2vw, 20px);
  color: #10b981;
  pointer-events: none;
}

.form-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  border: 1.5px solid rgba(22, 163, 74, 0.3);
  border-radius: clamp(8px, 1.5vw, 12px);
  padding: clamp(0.5rem, 1vw, 0.7rem) clamp(0.7rem, 1.2vw, 1rem) clamp(0.5rem, 1vw, 0.7rem) clamp(1.8rem, 3vw, 2.5rem);
  color: #1e3a2f;
  font-size: clamp(0.75rem, 1.5vw, 0.95rem);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-input::placeholder {
  color: #6b7280;
}

.form-input:focus {
  outline: none;
  border-color: #16a34a;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.15);
}

/* ========== REMEMBER ME ========== */
.remember-me {
  display: flex;
  align-items: center;
  gap: clamp(0.35rem, 0.8vw, 0.6rem);
  font-size: clamp(0.7rem, 1.3vw, 0.85rem);
}

.checkbox-input {
  width: clamp(14px, 2vw, 18px);
  height: clamp(14px, 2vw, 18px);
  accent-color: #10b981;
  cursor: pointer;
  border-radius: 4px;
}

.checkbox-label {
  color: #166534;
  cursor: pointer;
  transition: color 0.3s ease;
  font-weight: 500;
  font-size: clamp(0.7rem, 1.3vw, 0.85rem);
}

.checkbox-label:hover {
  color: #15803d;
}

/* ========== ERROR MESSAGE ========== */
.error-message {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1vw, 0.85rem);
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.6rem, 1.2vw, 1rem) clamp(0.8rem, 1.5vw, 1.3rem);
  color: #fca5a5;
  font-size: clamp(0.7rem, 1.3vw, 0.9rem);
  animation: slideDown 0.3s ease;
  font-weight: 500;
}

.error-icon {
  width: clamp(14px, 2vw, 20px);
  height: clamp(14px, 2vw, 20px);
  flex-shrink: 0;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== SUBMIT BUTTON ========== */
.submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.4rem, 0.8vw, 0.7rem);
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.55rem, 1vw, 0.85rem) clamp(0.9rem, 1.5vw, 1.4rem);
  font-size: clamp(0.75rem, 1.4vw, 0.95rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
  margin-top: clamp(0.2rem, 0.5vw, 0.4rem);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  letter-spacing: 0.01em;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(16, 185, 129, 0.45);
}

.submit-button:active {
  transform: translateY(0);
}

.button-icon {
  width: clamp(15px, 2vw, 20px);
  height: clamp(15px, 2vw, 20px);
}

/* ========== DIVIDER ========== */
.divider {
  position: relative;
  height: 1px;
  background: rgba(22, 163, 74, 0.2);
  margin: clamp(0.8rem, 1.5vw, 1.4rem) 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.divider span {
  background: rgba(255, 255, 255, 0.9);
  padding: 0 clamp(0.5rem, 1vw, 0.85rem);
  color: #166534;
  font-size: clamp(0.65rem, 1.2vw, 0.85rem);
  font-weight: 500;
}

/* ========== REGISTER BUTTON ========== */
.register-button {
  width: 100%;
  background: rgba(22, 163, 74, 0.08);
  color: #15803d;
  border: 1.5px solid rgba(22, 163, 74, 0.4);
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.55rem, 1vw, 0.9rem) clamp(0.9rem, 1.5vw, 1.5rem);
  font-size: clamp(0.75rem, 1.4vw, 0.95rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  margin-top: clamp(0.3rem, 0.6vw, 0.6rem);
}

.register-button:hover {
  background: rgba(22, 163, 74, 0.15);
  border-color: rgba(22, 163, 74, 0.7);
  color: #166534;
  transform: translateY(-1px);
}

.register-button:active {
  transform: scale(0.98);
}

/* ========== ADMIN BUTTON ========== */
.admin-button {
  width: 100%;
  background: rgba(20, 184, 166, 0.1);
  color: #0d9488;
  border: 1.5px solid rgba(20, 184, 166, 0.3);
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.5rem, 0.9vw, 0.85rem) clamp(0.8rem, 1.4vw, 1.4rem);
  font-size: clamp(0.7rem, 1.3vw, 0.9rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  margin-top: clamp(0.35rem, 0.7vw, 0.6rem);
}

.admin-button:hover {
  background: rgba(20, 184, 166, 0.2);
  border-color: rgba(20, 184, 166, 0.6);
  color: #0f766e;
  transform: translateY(-1px);
}

.admin-button:active {
  transform: scale(0.98);
}

/* ========== FOOTER ========== */
.login-footer {
  text-align: center;
  font-size: clamp(0.55rem, 1vw, 0.7rem);
  color: #166534;
  margin-top: clamp(0.5rem, 1vw, 0.8rem);
  font-weight: 500;
  letter-spacing: 0.01em;
}

.footer-highlight {
  color: #15803d;
  font-weight: 700;
}

/* ========== LAYOUT UNIFICADO - ESCALADO FLUIDO CON CLAMP() ========== */
/* Sin media queries - misma vista en todos los dispositivos */

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

/* ========== LOADING ANIMATION ========== */
.loading-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(240, 253, 244, 0.95);
  backdrop-filter: blur(4px);
  z-index: 9999;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(1rem, 2vw, 1.5rem);
}

.rotating-flower {
  width: clamp(50px, 8vw, 80px);
  height: clamp(50px, 8vw, 80px);
  animation: rotate-flower 3s linear infinite;
}

@keyframes rotate-flower {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #22C55E;
  font-size: clamp(0.8rem, 1.5vw, 1.125rem);
  font-weight: 500;
  letter-spacing: 1px;
  animation: pulse-text 1.5s ease-in-out infinite;
}

@keyframes pulse-text {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Transición de fade para el overlay de carga */
.fade-loading-enter-active,
.fade-loading-leave-active {
  transition: opacity 0.3s ease;
}

.fade-loading-enter-from,
.fade-loading-leave-to {
  opacity: 0;
}
</style>
