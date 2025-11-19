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
      <div
        v-motion
        :initial="{ opacity: 0, y: -50 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="logo-section"
      >
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
        <p class="app-subtitle">Acceso seguro</p>
      </div>

      <!-- Tarjeta de login -->
      <div
        v-motion
        :initial="{ opacity: 0, scale: 0.9, y: 50 }"
        :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
        class="login-card"
      >
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
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1, transition: { delay: 600, duration: 600 } }"
        class="login-footer"
      >
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

    const passwordAdmin = prompt('Contraseña del administrador:')
    if (!passwordAdmin) return

    if (!nombre || !emailAdmin || !passwordAdmin) {
      await Swal.fire('⚠️ Campos incompletos', 'Debes llenar todos los campos', 'warning')
      return
    }

    await axios.post(`${import.meta.env.VITE_API_URL}/auth/register`, {
      nombre,
      email: emailAdmin,
      password: passwordAdmin,
      rol: 'admin'
    })

    await Swal.fire('✅ Administrador creado', 'Ya puedes iniciar sesión con este usuario', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', err.response?.data?.detail || 'No se pudo crear el usuario', 'error')
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
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
}

/* ========== BACKGROUND BLOBS ========== */
.background-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.blob {
  position: absolute;
  opacity: 0.1;
  filter: blur(100px);
  mix-blend-mode: screen;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  border-radius: 50%;
  top: -200px;
  left: -200px;
  animation: blob-animate 8s ease-in-out infinite;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  top: 50%;
  right: -150px;
  animation: blob-animate 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #ec4899, #f59e0b);
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
  max-width: 390px;
  padding: 1.5rem 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ========== LOGO SECTION ========== */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
  text-align: center;
  width: 100%;
}

/* Animación de maceta con flor */
.flowerpot-animation {
  width: 85px;
  height: 105px;
  margin-bottom: 0.8rem;
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
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.app-subtitle {
  font-size: 0.9rem;
  color: #cbd5e1;
  font-weight: 400;
  letter-spacing: 0.01em;
}

/* ========== LOGIN CARD ========== */
.login-card {
  width: 100%;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.85) 100%);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 24px;
  padding: 1.8rem 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 1px rgba(16, 185, 129, 0.1);
  margin-bottom: 1rem;
}

.login-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 0.4rem;
  text-align: center;
  letter-spacing: -0.01em;
}

.login-subtitle {
  font-size: 0.9rem;
  color: #cbd5e1;
  text-align: center;
  margin-bottom: 1.5rem;
  font-weight: 400;
}

/* ========== FORM ========== */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #cbd5e1;
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
  left: 14px;
  width: 20px;
  height: 20px;
  color: #10b981;
  pointer-events: none;
}

.form-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1.5px solid rgba(148, 163, 184, 0.25);
  border-radius: 12px;
  padding: 0.75rem 1.1rem 0.75rem 2.7rem;
  color: #e2e8f0;
  font-size: 0.9rem;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15);
}

/* ========== REMEMBER ME ========== */
.remember-me {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.9rem;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  accent-color: #10b981;
  cursor: pointer;
  border-radius: 4px;
}

.checkbox-label {
  color: #cbd5e1;
  cursor: pointer;
  transition: color 0.3s ease;
  font-weight: 500;
}

.checkbox-label:hover {
  color: #e2e8f0;
}

/* ========== ERROR MESSAGE ========== */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  padding: 0.85rem 1.2rem;
  color: #fca5a5;
  font-size: 0.875rem;
  animation: slideDown 0.3s ease;
  font-weight: 500;
}

.error-icon {
  width: 18px;
  height: 18px;
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
  gap: 0.65rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.9rem 1.4rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
  margin-top: 0.5rem;
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
  width: 18px;
  height: 18px;
}

/* ========== DIVIDER ========== */
.divider {
  position: relative;
  height: 1px;
  background: rgba(148, 163, 184, 0.2);
  margin: 1.2rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.divider span {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  padding: 0 0.75rem;
  color: #64748b;
  font-size: 0.8rem;
  font-weight: 500;
}

/* ========== REGISTER BUTTON ========== */
.register-button {
  width: 100%;
  background: rgba(148, 163, 184, 0.08);
  color: #6ee7b7;
  border: 1.5px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  padding: 0.8rem 1.4rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  margin-top: 0.5rem;
}

.register-button:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.6);
  color: #10b981;
  transform: translateY(-1px);
}

.register-button:active {
  transform: scale(0.98);
}

/* ========== ADMIN BUTTON ========== */
.admin-button {
  width: 100%;
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
  border: 1.5px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  padding: 0.75rem 1.3rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  margin-top: 0.5rem;
}

.admin-button:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.6);
  color: #3b82f6;
  transform: translateY(-1px);
}

.admin-button:active {
  transform: scale(0.98);
}

/* ========== FOOTER ========== */
.login-footer {
  text-align: center;
  font-size: 0.75rem;
  color: #475569;
  margin-top: 1rem;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.footer-highlight {
  color: #10b981;
  font-weight: 700;
}

/* ========== RESPONSIVE - TABLET (768px - 1024px) ========== */
@media (max-width: 1024px) {
  .login-content {
    max-width: 420px;
  }

  .app-title {
    font-size: 1.6rem;
  }

  .flowerpot-animation {
    width: 80px;
    height: 100px;
    margin-bottom: 0.75rem;
  }
}

/* ========== RESPONSIVE - TABLET (641px - 768px) ========== */
@media (max-width: 768px) {
  .login-container {
    padding: 1rem 0;
  }

  .login-content {
    padding: 1.25rem 1rem;
    max-width: 100%;
  }

  .logo-section {
    margin-bottom: 1.75rem;
  }

  .app-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .app-subtitle {
    font-size: 0.9rem;
  }

  .flowerpot-animation {
    width: 90px;
    height: 110px;
    margin-bottom: 1rem;
  }

  .login-card {
    padding: 1.75rem 1.5rem;
    margin-bottom: 1.25rem;
    border-radius: 20px;
  }

  .login-title {
    font-size: 1.35rem;
  }

  .login-subtitle {
    font-size: 0.9rem;
    margin-bottom: 1.75rem;
  }

  .login-form {
    gap: 1.2rem;
  }

  .form-label {
    font-size: 0.8rem;
  }

  .form-input {
    padding: 0.75rem 1rem 0.75rem 2.4rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  .input-icon {
    left: 12px;
    width: 18px;
    height: 18px;
  }

  .submit-button {
    padding: 0.8rem 1.25rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  .register-button {
    padding: 0.8rem 1.25rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  .admin-button {
    padding: 0.7rem 1.2rem;
    font-size: 0.8rem;
    border-radius: 10px;
    margin-top: 0.6rem;
  }

  .login-footer {
    font-size: 0.75rem;
  }
}

/* ========== RESPONSIVE - MOBILE (577px - 640px) ========== */
@media (max-width: 640px) {
  .login-container {
    padding: 0.75rem 0;
  }

  .login-content {
    padding: 1rem 0.75rem;
    max-width: 100%;
  }

  .logo-section {
    margin-bottom: 1.5rem;
  }

  .app-title {
    font-size: 1.35rem;
    margin-bottom: 0.4rem;
  }

  .app-subtitle {
    font-size: 0.85rem;
  }

  .flowerpot-animation {
    width: 80px;
    height: 100px;
    margin-bottom: 0.9rem;
  }

  .login-card {
    padding: 1.5rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 18px;
  }

  .login-title {
    font-size: 1.2rem;
    margin-bottom: 0.4rem;
  }

  .login-subtitle {
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .login-form {
    gap: 1rem;
  }

  .form-group {
    gap: 0.4rem;
  }

  .form-label {
    font-size: 0.75rem;
    letter-spacing: 0.06em;
  }

  .form-input {
    padding: 0.65rem 0.9rem 0.65rem 2.2rem;
    font-size: 16px;
    border-radius: 9px;
  }

  .input-icon {
    left: 11px;
    width: 17px;
    height: 17px;
  }

  .remember-me {
    font-size: 0.8rem;
    gap: 0.4rem;
  }

  .checkbox-input {
    width: 16px;
    height: 16px;
  }

  .checkbox-label {
    font-size: 0.8rem;
  }

  .submit-button {
    padding: 0.7rem 1.1rem;
    font-size: 0.85rem;
    border-radius: 9px;
    margin-top: 0.4rem;
  }

  .error-message {
    font-size: 0.75rem;
    padding: 0.6rem 0.9rem;
    border-radius: 10px;
  }

  .divider {
    margin: 1.2rem 0;
  }

  .divider span {
    font-size: 0.75rem;
  }

  .register-button {
    padding: 0.7rem 1.1rem;
    font-size: 0.85rem;
    border-radius: 9px;
  }

  .admin-button {
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    border-radius: 9px;
    margin-top: 0.5rem;
  }

  .login-footer {
    font-size: 0.7rem;
    margin-top: 1rem;
  }
}

/* ========== RESPONSIVE - MOBILE PEQUEÑO (481px - 576px) ========== */
@media (max-width: 576px) {
  .login-container {
    padding: 0.5rem 0;
  }

  .login-content {
    padding: 0.9rem 0.7rem;
    max-width: 100%;
  }

  .logo-section {
    margin-bottom: 1.3rem;
  }

  .app-title {
    font-size: 1.25rem;
    margin-bottom: 0.3rem;
    line-height: 1.2;
  }

  .app-subtitle {
    font-size: 0.8rem;
  }

  .flowerpot-animation {
    width: 75px;
    height: 95px;
    margin-bottom: 0.75rem;
  }

  .login-card {
    padding: 1.4rem 1.1rem;
    margin-bottom: 0.8rem;
    border-radius: 16px;
  }

  .login-title {
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
  }

  .login-subtitle {
    font-size: 0.8rem;
    margin-bottom: 1.3rem;
  }

  .login-form {
    gap: 0.9rem;
  }

  .form-group {
    gap: 0.35rem;
  }

  .form-label {
    font-size: 0.7rem;
    letter-spacing: 0.05em;
  }

  .form-input {
    padding: 0.6rem 0.85rem 0.6rem 2.1rem;
    font-size: 15px;
    border-radius: 8px;
  }

  .input-icon {
    left: 10px;
    width: 16px;
    height: 16px;
  }

  .remember-me {
    font-size: 0.75rem;
    gap: 0.35rem;
  }

  .checkbox-input {
    width: 15px;
    height: 15px;
  }

  .checkbox-label {
    font-size: 0.75rem;
  }

  .submit-button {
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    border-radius: 8px;
    gap: 0.35rem;
    margin-top: 0.3rem;
  }

  .button-icon {
    width: 16px;
    height: 16px;
  }

  .error-message {
    font-size: 0.7rem;
    padding: 0.55rem 0.8rem;
    border-radius: 8px;
  }

  .error-icon {
    width: 16px;
    height: 16px;
  }

  .divider {
    margin: 1rem 0;
    height: 0.5px;
  }

  .divider span {
    font-size: 0.7rem;
    padding: 0 0.6rem;
  }

  .register-button {
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    border-radius: 8px;
  }

  .admin-button {
    padding: 0.6rem 0.9rem;
    font-size: 0.75rem;
    border-radius: 8px;
    margin-top: 0.5rem;
  }

  .login-footer {
    font-size: 0.65rem;
    margin-top: 0.8rem;
  }
}

/* ========== RESPONSIVE - MOBILE ULTRA PEQUEÑO (320px - 480px) ========== */
@media (max-width: 480px) {
  .login-container {
    padding: 0.5rem 0;
  }

  .login-content {
    padding: 0.75rem 0.6rem;
    max-width: 100%;
  }

  .logo-section {
    margin-bottom: 1.15rem;
  }

  .app-title {
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
    line-height: 1.1;
  }

  .app-subtitle {
    font-size: 0.75rem;
  }

  .flowerpot-animation {
    width: 70px;
    height: 90px;
    margin-bottom: 0.65rem;
  }

  .login-card {
    padding: 1.2rem 0.95rem;
    margin-bottom: 0.7rem;
    border-radius: 14px;
  }

  .login-title {
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }

  .login-subtitle {
    font-size: 0.75rem;
    margin-bottom: 1.1rem;
  }

  .login-form {
    gap: 0.8rem;
  }

  .form-group {
    gap: 0.3rem;
  }

  .form-label {
    font-size: 0.65rem;
    letter-spacing: 0.04em;
  }

  .form-input {
    padding: 0.55rem 0.8rem 0.55rem 2rem;
    font-size: 14px;
    border-radius: 7px;
  }

  .input-icon {
    left: 9px;
    width: 15px;
    height: 15px;
  }

  .remember-me {
    font-size: 0.7rem;
    gap: 0.3rem;
  }

  .checkbox-input {
    width: 14px;
    height: 14px;
  }

  .checkbox-label {
    font-size: 0.7rem;
  }

  .submit-button {
    padding: 0.6rem 0.9rem;
    font-size: 0.75rem;
    border-radius: 7px;
    gap: 0.3rem;
    margin-top: 0.25rem;
  }

  .button-icon {
    width: 15px;
    height: 15px;
  }

  .error-message {
    font-size: 0.65rem;
    padding: 0.5rem 0.75rem;
    border-radius: 7px;
  }

  .error-icon {
    width: 15px;
    height: 15px;
  }

  .divider {
    margin: 0.9rem 0;
    height: 0.5px;
  }

  .divider span {
    font-size: 0.65rem;
    padding: 0 0.5rem;
  }

  .register-button {
    padding: 0.6rem 0.9rem;
    font-size: 0.75rem;
    border-radius: 7px;
  }

  .admin-button {
    padding: 0.55rem 0.85rem;
    font-size: 0.7rem;
    border-radius: 7px;
    margin-top: 0.4rem;
  }

  .login-footer {
    font-size: 0.6rem;
    margin-top: 0.7rem;
  }
}

/* ========== RESPONSIVE - MOBILE TINY (280px - 320px) ========== */
@media (max-width: 320px) {
  .login-container {
    padding: 0.25rem 0;
  }

  .login-content {
    padding: 0.65rem 0.5rem;
    max-width: 100%;
  }

  .logo-section {
    margin-bottom: 1rem;
  }

  .app-title {
    font-size: 1rem;
    margin-bottom: 0.2rem;
    line-height: 1.1;
  }

  .app-subtitle {
    font-size: 0.7rem;
  }

  .flowerpot-animation {
    width: 60px;
    height: 80px;
    margin-bottom: 0.6rem;
  }

  .login-card {
    padding: 1rem 0.8rem;
    margin-bottom: 0.6rem;
    border-radius: 12px;
  }

  .login-title {
    font-size: 0.95rem;
    margin-bottom: 0.2rem;
  }

  .login-subtitle {
    font-size: 0.7rem;
    margin-bottom: 1rem;
  }

  .login-form {
    gap: 0.7rem;
  }

  .form-group {
    gap: 0.25rem;
  }

  .form-label {
    font-size: 0.6rem;
    letter-spacing: 0.03em;
  }

  .form-input {
    padding: 0.5rem 0.7rem 0.5rem 1.9rem;
    font-size: 13px;
    border-radius: 6px;
  }

  .input-icon {
    left: 8px;
    width: 14px;
    height: 14px;
  }

  .remember-me {
    font-size: 0.65rem;
    gap: 0.25rem;
  }

  .checkbox-input {
    width: 13px;
    height: 13px;
  }

  .checkbox-label {
    font-size: 0.65rem;
  }

  .submit-button {
    padding: 0.55rem 0.8rem;
    font-size: 0.7rem;
    border-radius: 6px;
    gap: 0.25rem;
    margin-top: 0.2rem;
  }

  .error-message {
    font-size: 0.6rem;
    padding: 0.45rem 0.7rem;
    border-radius: 6px;
  }

  .divider {
    margin: 0.8rem 0;
  }

  .divider span {
    font-size: 0.6rem;
    padding: 0 0.4rem;
  }

  .register-button {
    padding: 0.55rem 0.8rem;
    font-size: 0.7rem;
    border-radius: 6px;
  }

  .admin-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.65rem;
    border-radius: 6px;
    margin-top: 0.35rem;
  }

  .login-footer {
    font-size: 0.55rem;
    margin-top: 0.6rem;
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

/* ========== LOADING ANIMATION ========== */
.loading-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(4px);
  z-index: 9999;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.rotating-flower {
  width: 80px;
  height: 80px;
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
  font-size: 1.125rem;
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

/* ========== RESPONSIVE - LOADING ========== */
@media (max-width: 1024px) {
  .rotating-flower {
    width: 70px;
    height: 70px;
  }
  
  .loading-text {
    font-size: 1rem;
  }
}

@media (max-width: 768px) {
  .rotating-flower {
    width: 65px;
    height: 65px;
  }
  
  .loading-text {
    font-size: 0.95rem;
  }
}

@media (max-width: 640px) {
  .rotating-flower {
    width: 60px;
    height: 60px;
  }
  
  .loading-text {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .rotating-flower {
    width: 55px;
    height: 55px;
  }
  
  .loading-text {
    font-size: 0.85rem;
  }
}

@media (max-width: 320px) {
  .rotating-flower {
    width: 50px;
    height: 50px;
  }
  
  .loading-text {
    font-size: 0.8rem;
  }
}
</style>
