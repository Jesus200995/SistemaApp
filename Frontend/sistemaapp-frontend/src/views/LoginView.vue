<template>
  <div class="login-container">
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
        <div class="logo-icon">
          <LogIn class="logo-svg" />
        </div>
        <h1 class="app-title">SistemaApp</h1>
        <p class="app-subtitle">Acceso al Panel de Control</p>
      </div>

      <!-- Tarjeta de login -->
      <div
        v-motion
        :initial="{ opacity: 0, scale: 0.9, y: 50 }"
        :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
        class="login-card"
      >
        <h2 class="login-title">Bienvenido de Nuevo</h2>
        <p class="login-subtitle">Inicia sesión para continuar</p>

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
            <LogIn class="button-icon" />
          </button>
        </form>

        <!-- Divider -->
        <div class="divider">
          <span>¿No tienes cuenta?</span>
        </div>

        <!-- Botón registrarse -->
        <button @click="mostrarRegistro = true" class="register-button">
          Crear una cuenta nueva
        </button>
      </div>

      <!-- Footer -->
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1, transition: { delay: 600, duration: 600 } }"
        class="login-footer"
      >
        <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Todos los derechos reservados.</p>
      </div>
    </div>

    <!-- Modal de registro -->
    <RegisterForm :mostrar="mostrarRegistro" @close="mostrarRegistro = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { LogIn, Mail, Lock, AlertCircle } from 'lucide-vue-next'
import RegisterForm from '../components/RegisterForm.vue'

const email = ref('')
const password = ref('')
const mostrarRegistro = ref(false)
const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  const ok = await auth.login(email.value, password.value)
  if (ok) {
    router.push('/dashboard')
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
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
  max-width: 420px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ========== LOGO SECTION ========== */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  text-align: center;
}

.logo-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.logo-svg {
  width: 36px;
  height: 36px;
  color: white;
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.app-subtitle {
  font-size: 0.95rem;
  color: #94a3b8;
  font-weight: 500;
}

/* ========== LOGIN CARD ========== */
.login-card {
  width: 100%;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  margin-bottom: 1.5rem;
}

.login-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  text-align: center;
}

.login-subtitle {
  font-size: 0.9rem;
  color: #94a3b8;
  text-align: center;
  margin-bottom: 2rem;
}

/* ========== FORM ========== */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: #10b981;
  pointer-events: none;
}

.form-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

/* ========== REMEMBER ME ========== */
.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  accent-color: #10b981;
  cursor: pointer;
  border-radius: 4px;
}

.checkbox-label {
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.3s ease;
}

.checkbox-label:hover {
  color: #cbd5e1;
}

/* ========== ERROR MESSAGE ========== */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #fca5a5;
  font-size: 0.875rem;
  animation: slideDown 0.3s ease;
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
  gap: 0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  margin-top: 0.5rem;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
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
  margin: 1.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.divider span {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  padding: 0 0.75rem;
  color: #64748b;
  font-size: 0.8rem;
}

/* ========== REGISTER BUTTON ========== */
.register-button {
  width: 100%;
  background: rgba(148, 163, 184, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 10px;
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.register-button:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.5);
  color: #6ee7b7;
}

.register-button:active {
  transform: scale(0.98);
}

/* ========== FOOTER ========== */
.login-footer {
  text-align: center;
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 1rem;
}

.footer-highlight {
  color: #10b981;
  font-weight: 600;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 640px) {
  .login-content {
    padding: 1rem;
    max-width: 100%;
  }

  .logo-section {
    margin-bottom: 1.5rem;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .app-subtitle {
    font-size: 0.85rem;
  }

  .logo-icon {
    width: 50px;
    height: 50px;
  }

  .logo-svg {
    width: 28px;
    height: 28px;
  }

  .login-card {
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  .login-title {
    font-size: 1.25rem;
  }

  .login-subtitle {
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .login-form {
    gap: 1rem;
  }

  .form-input {
    padding: 0.7rem 1rem 0.7rem 2.3rem;
    font-size: 0.9rem;
  }

  .submit-button {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }

  .divider {
    margin: 1.25rem 0;
  }

  .divider span {
    font-size: 0.75rem;
  }

  .error-message {
    font-size: 0.8rem;
    padding: 0.6rem 0.8rem;
  }
}

@media (max-width: 480px) {
  .login-content {
    padding: 0.75rem;
  }

  .logo-icon {
    width: 45px;
    height: 45px;
  }

  .logo-svg {
    width: 24px;
    height: 24px;
  }

  .app-title {
    font-size: 1.25rem;
  }

  .login-card {
    padding: 1.25rem;
  }

  .login-title {
    font-size: 1.1rem;
  }

  .form-input {
    font-size: 16px; /* Previene zoom automático en iOS */
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
