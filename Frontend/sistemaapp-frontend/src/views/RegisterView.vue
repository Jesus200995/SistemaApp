<template>
  <div class="register-container">
    <!-- Fondo animado -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Contenido principal -->
    <div class="register-content">
      <!-- Logo y título -->
      <div
        v-motion
        :initial="{ opacity: 0, y: -50 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="logo-section"
      >
        <div class="logo-icon">
          <UserPlus class="logo-svg" />
        </div>
        <h1 class="app-title">SistemaApp</h1>
        <p class="app-subtitle">Crear Nueva Cuenta</p>
      </div>

      <!-- Tarjeta de registro -->
      <div
        v-motion
        :initial="{ opacity: 0, scale: 0.9, y: 50 }"
        :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
        class="register-card"
      >
        <h2 class="register-title">Únete a SistemaApp</h2>
        <p class="register-subtitle">Completa el formulario para crear tu cuenta</p>

        <form @submit.prevent="handleRegister" class="register-form">
          <!-- Campo Nombre -->
          <div class="form-group">
            <label for="nombre" class="form-label">Nombre Completo</label>
            <div class="input-wrapper">
              <User class="input-icon" />
              <input
                id="nombre"
                v-model="formData.nombre"
                type="text"
                placeholder="Juan Pérez"
                class="form-input"
                required
                minlength="2"
              />
            </div>
          </div>

          <!-- Campo Email -->
          <div class="form-group">
            <label for="email" class="form-label">Correo Electrónico</label>
            <div class="input-wrapper">
              <Mail class="input-icon" />
              <input
                id="email"
                v-model="formData.email"
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
                v-model="formData.password"
                type="password"
                placeholder="••••••••"
                class="form-input"
                required
                minlength="6"
              />
            </div>
          </div>

          <!-- Campo Confirmar Contraseña -->
          <div class="form-group">
            <label for="confirm" class="form-label">Confirmar Contraseña</label>
            <div class="input-wrapper">
              <Lock class="input-icon" />
              <input
                id="confirm"
                v-model="formData.confirmPassword"
                type="password"
                placeholder="••••••••"
                class="form-input"
                required
                minlength="6"
              />
            </div>
          </div>

          <!-- Campo Rol -->
          <div class="form-group">
            <label for="rol" class="form-label">¿Qué tipo de usuario eres?</label>
            <div class="select-wrapper">
              <Briefcase class="select-icon" />
              <select
                id="rol"
                v-model="formData.rol"
                class="form-select"
                required
              >
                <option value="">-- Selecciona un rol --</option>
                <option value="tecnico_productivo">Técnico Productivo</option>
                <option value="tecnico_social">Técnico Social</option>
                <option value="facilitador">Facilitador</option>
              </select>
            </div>
          </div>

          <!-- Checkbox Términos -->
          <div class="terms-group">
            <input
              id="terms"
              v-model="formData.acceptTerms"
              type="checkbox"
              class="terms-checkbox"
              required
            />
            <label for="terms" class="terms-label">
              Acepto los
              <a href="#" @click.prevent="showTerms" class="terms-link">términos y condiciones</a>
            </label>
          </div>

          <!-- Mensaje de error -->
          <div v-if="error" class="error-message">
            <AlertCircle class="error-icon" />
            <span>{{ error }}</span>
          </div>

          <!-- Mensaje de éxito -->
          <div v-if="success" class="success-message">
            <CheckCircle class="success-icon" />
            <span>{{ success }}</span>
          </div>

          <!-- Botón registrarse -->
          <button
            type="submit"
            :disabled="loading || !!success"
            class="submit-button"
          >
            <span>{{ loading ? 'Registrando...' : 'Crear Cuenta' }}</span>
            <UserPlus v-if="!loading" class="button-icon" />
          </button>
        </form>

        <!-- Divider -->
        <div class="divider">
          <span>¿Ya tienes cuenta?</span>
        </div>

        <!-- Enlace a login -->
        <router-link to="/login" class="login-link">
          Inicia sesión aquí
        </router-link>
      </div>

      <!-- Footer -->
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1, transition: { delay: 600, duration: 600 } }"
        class="register-footer"
      >
        <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus, User, Mail, Lock, AlertCircle, CheckCircle, Briefcase } from 'lucide-vue-next'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')

const formData = ref({
  nombre: '',
  email: '',
  password: '',
  confirmPassword: '',
  rol: '',
  acceptTerms: false,
})

const handleRegister = async () => {
  // Limpiar mensajes
  error.value = ''
  success.value = ''

  // Validaciones locales
  if (!formData.value.nombre || formData.value.nombre.length < 2) {
    error.value = 'El nombre debe tener al menos 2 caracteres'
    return
  }

  if (!formData.value.email) {
    error.value = 'El correo electrónico es requerido'
    return
  }

  if (formData.value.password.length < 6) {
    error.value = 'La contraseña debe tener al menos 6 caracteres'
    return
  }

  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = 'Las contraseñas no coinciden'
    return
  }

  if (!formData.value.rol) {
    error.value = 'Debes seleccionar un rol'
    return
  }

  if (!formData.value.acceptTerms) {
    error.value = 'Debes aceptar los términos y condiciones'
    return
  }

  loading.value = true

  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    
    const response = await fetch(`${apiUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        nombre: formData.value.nombre,
        email: formData.value.email,
        password: formData.value.password,
        rol: formData.value.rol,
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'Error al registrar usuario')
    }

    const data = await response.json()
    
    success.value = `¡Cuenta creada exitosamente! Bienvenido ${data.nombre}`
    
    // Redirigir al login después de 2 segundos
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: any) {
    error.value = err.message || 'Error desconocido al registrar'
  } finally {
    loading.value = false
  }
}

const showTerms = () => {
  alert(
    '📋 Términos y Condiciones\n\n' +
      '1. Aceptas usar la plataforma de manera responsable\n' +
      '2. Mantendrás tu contraseña confidencial\n' +
      '3. No harás uso malicioso de la plataforma\n' +
      '4. Respetarás la privacidad de otros usuarios\n' +
      '5. Cumplirás con todas las leyes aplicables\n\n' +
      'Para más información, contacta a soporte@sistemaapp.com'
  )
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.register-container {
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
.register-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 500px;
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
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.logo-svg {
  width: 36px;
  height: 36px;
  color: white;
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
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

/* ========== REGISTER CARD ========== */
.register-card {
  width: 100%;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  margin-bottom: 1.5rem;
}

.register-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  text-align: center;
}

.register-subtitle {
  font-size: 0.9rem;
  color: #94a3b8;
  text-align: center;
  margin-bottom: 2rem;
}

/* ========== FORM ========== */
.register-form {
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
  color: #3b82f6;
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
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* ========== SELECT ========== */
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: #3b82f6;
  pointer-events: none;
  z-index: 1;
}

.form-select {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-select option {
  background-color: #1e293b;
  color: #e2e8f0;
}

/* ========== TERMS ========== */
.terms-group {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-top: 1rem;
}

.terms-checkbox {
  width: 20px;
  height: 20px;
  accent-color: #3b82f6;
  cursor: pointer;
  border-radius: 4px;
  margin-top: 2px;
  flex-shrink: 0;
}

.terms-label {
  font-size: 0.875rem;
  color: #cbd5e1;
  cursor: pointer;
  line-height: 1.5;
}

.terms-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.terms-link:hover {
  color: #60a5fa;
  text-decoration: underline;
}

/* ========== MESSAGES ========== */
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

.success-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #86efac;
  font-size: 0.875rem;
  animation: slideDown 0.3s ease;
}

.error-icon,
.success-icon {
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
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  margin-top: 0.5rem;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4);
}

.submit-button:active:not(:disabled) {
  transform: translateY(0);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

/* ========== LOGIN LINK ========== */
.login-link {
  width: 100%;
  display: block;
  text-align: center;
  background: rgba(148, 163, 184, 0.1);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 10px;
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.login-link:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.5);
  color: #60a5fa;
}

.login-link:active {
  transform: scale(0.98);
}

/* ========== FOOTER ========== */
.register-footer {
  text-align: center;
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 1rem;
}

.footer-highlight {
  color: #3b82f6;
  font-weight: 600;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 640px) {
  .register-content {
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

  .register-card {
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  .register-title {
    font-size: 1.25rem;
  }

  .register-subtitle {
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .register-form {
    gap: 1rem;
  }

  .form-input,
  .form-select {
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

  .error-message,
  .success-message {
    font-size: 0.8rem;
    padding: 0.6rem 0.8rem;
  }

  .terms-group {
    gap: 0.5rem;
  }

  .terms-label {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .register-content {
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

  .register-card {
    padding: 1.25rem;
  }

  .register-title {
    font-size: 1.1rem;
  }

  .form-input,
  .form-select {
    font-size: 16px; /* Previene zoom automático en iOS */
  }

  .register-form {
    gap: 0.875rem;
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
