<template>
  <div class="register-container">
    <!-- Fondo animado -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Botón de regresar -->
    <router-link to="/login" class="back-button">
      <ArrowLeft class="back-icon" />
    </router-link>

    <!-- Contenido principal -->
    <div class="register-content">
      <!-- Logo y título -->
      <div
        v-motion
        :initial="{ opacity: 0, y: -50 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="logo-section"
      >
        <h1 class="app-title">Sistema de Administración</h1>
        <p class="app-subtitle">Crea tu cuenta</p>
      </div>

      <!-- Tarjeta de registro -->
      <div
        v-motion
        :initial="{ opacity: 0, scale: 0.9, y: 50 }"
        :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
        class="register-card"
      >
        <h2 class="register-title">Crear Cuenta</h2>
        <p class="register-subtitle">Completa el formulario</p>

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
        <p>© 2025 <span class="footer-highlight">Sistema de Administración</span>. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Mail, Lock, AlertCircle, CheckCircle, Briefcase, ArrowLeft } from 'lucide-vue-next'

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
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 1rem 0;
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

/* ========== BACK BUTTON ========== */
.back-button {
  position: fixed;
  top: 2rem;
  left: 2rem;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
  z-index: 20;
  text-decoration: none;
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(16, 185, 129, 0.45);
}

.back-button:active {
  transform: translateY(0);
}

.back-icon {
  width: 24px;
  height: 24px;
  color: white;
  stroke-width: 2.5;
}

/* ========== CONTENT ========== */
.register-content {
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
  width: 110px;
  height: 130px;
  margin-bottom: 1.25rem;
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

/* ========== REGISTER CARD ========== */
.register-card {
  width: 100%;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.85) 100%);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 24px;
  padding: 1.8rem 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 1px rgba(16, 185, 129, 0.1);
  margin-bottom: 1rem;
}

.register-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 0.4rem;
  text-align: center;
  letter-spacing: -0.01em;
}

.register-subtitle {
  font-size: 0.9rem;
  color: #cbd5e1;
  text-align: center;
  margin-bottom: 1.5rem;
  font-weight: 400;
}

/* ========== FORM ========== */
.register-form {
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

/* ========== SELECT ========== */
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-icon {
  position: absolute;
  left: 14px;
  width: 20px;
  height: 20px;
  color: #10b981;
  pointer-events: none;
  z-index: 1;
}

.form-select {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1.5px solid rgba(148, 163, 184, 0.25);
  border-radius: 12px;
  padding: 0.85rem 1.2rem 0.85rem 2.8rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  border-color: #10b981;
  background-color: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15);
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
  width: 18px;
  height: 18px;
  accent-color: #10b981;
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
  font-weight: 500;
}

.terms-link {
  color: #10b981;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.terms-link:hover {
  color: #6ee7b7;
  text-decoration: underline;
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

/* ========== SUCCESS MESSAGE ========== */
.success-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  padding: 0.85rem 1.2rem;
  color: #86efac;
  font-size: 0.875rem;
  animation: slideDown 0.3s ease;
  font-weight: 500;
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

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(16, 185, 129, 0.45);
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
  margin: 1.75rem 0;
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

/* ========== LOGIN LINK ========== */
.login-link {
  width: 100%;
  display: block;
  text-align: center;
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
  margin-top: 0.5rem;
}

.login-link:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.6);
  color: #10b981;
  transform: translateY(-1px);
}

.login-link:active {
  transform: scale(0.98);
}

/* ========== FOOTER ========== */
.register-footer {
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
  .register-content {
    max-width: 420px;
  }

  .app-title {
    font-size: 1.6rem;
  }

  .back-button {
    top: 1.5rem;
    left: 1.5rem;
    width: 46px;
    height: 46px;
  }

  .back-icon {
    width: 22px;
    height: 22px;
  }
}

/* ========== RESPONSIVE - TABLET (641px - 768px) ========== */
@media (max-width: 768px) {
  .register-container {
    padding: 1rem 0;
  }

  .back-button {
    top: 1.25rem;
    left: 1.25rem;
    width: 44px;
    height: 44px;
  }

  .back-icon {
    width: 20px;
    height: 20px;
  }

  .register-content {
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
    width: 100px;
    height: 120px;
    margin-bottom: 1.25rem;
  }

  .register-card {
    padding: 1.75rem 1.5rem;
    margin-bottom: 1.25rem;
    border-radius: 20px;
  }

  .register-title {
    font-size: 1.35rem;
  }

  .register-subtitle {
    font-size: 0.9rem;
    margin-bottom: 1.75rem;
  }

  .register-form {
    gap: 1.2rem;
  }

  .form-label {
    font-size: 0.8rem;
  }

  .form-input,
  .form-select {
    padding: 0.75rem 1rem 0.75rem 2.4rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  .input-icon,
  .select-icon {
    left: 12px;
    width: 18px;
    height: 18px;
  }

  .submit-button {
    padding: 0.8rem 1.25rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  .login-link {
    padding: 0.8rem 1.25rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  .register-footer {
    font-size: 0.75rem;
  }
}

/* ========== RESPONSIVE - MOBILE (577px - 640px) ========== */
@media (max-width: 640px) {
  .register-container {
    padding: 0.75rem 0;
  }

  .back-button {
    top: 1rem;
    left: 1rem;
    width: 42px;
    height: 42px;
  }

  .back-icon {
    width: 19px;
    height: 19px;
  }

  .register-content {
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
    width: 90px;
    height: 110px;
    margin-bottom: 1rem;
  }

  .register-card {
    padding: 1.5rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 18px;
  }

  .register-title {
    font-size: 1.2rem;
    margin-bottom: 0.4rem;
  }

  .register-subtitle {
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .register-form {
    gap: 1rem;
  }

  .form-group {
    gap: 0.4rem;
  }

  .form-label {
    font-size: 0.75rem;
    letter-spacing: 0.06em;
  }

  .form-input,
  .form-select {
    padding: 0.65rem 0.9rem 0.65rem 2.2rem;
    font-size: 16px;
    border-radius: 9px;
  }

  .input-icon,
  .select-icon {
    left: 11px;
    width: 17px;
    height: 17px;
  }

  .terms-group {
    gap: 0.4rem;
  }

  .terms-checkbox {
    width: 16px;
    height: 16px;
  }

  .terms-label {
    font-size: 0.8rem;
  }

  .submit-button {
    padding: 0.7rem 1.1rem;
    font-size: 0.85rem;
    border-radius: 9px;
    margin-top: 0.4rem;
  }

  .error-message,
  .success-message {
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

  .login-link {
    padding: 0.7rem 1.1rem;
    font-size: 0.85rem;
    border-radius: 9px;
  }

  .register-footer {
    font-size: 0.7rem;
    margin-top: 1rem;
  }
}

/* ========== RESPONSIVE - MOBILE PEQUEÑO (481px - 576px) ========== */
@media (max-width: 576px) {
  .register-container {
    padding: 0.5rem 0;
  }

  .back-button {
    top: 0.9rem;
    left: 0.9rem;
    width: 40px;
    height: 40px;
  }

  .back-icon {
    width: 18px;
    height: 18px;
  }

  .register-content {
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
    width: 80px;
    height: 100px;
    margin-bottom: 0.85rem;
  }

  .register-card {
    padding: 1.4rem 1.1rem;
    margin-bottom: 0.8rem;
    border-radius: 16px;
  }

  .register-title {
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
  }

  .register-subtitle {
    font-size: 0.8rem;
    margin-bottom: 1.3rem;
  }

  .register-form {
    gap: 0.9rem;
  }

  .form-group {
    gap: 0.35rem;
  }

  .form-label {
    font-size: 0.7rem;
    letter-spacing: 0.05em;
  }

  .form-input,
  .form-select {
    padding: 0.6rem 0.85rem 0.6rem 2.1rem;
    font-size: 15px;
    border-radius: 8px;
  }

  .input-icon,
  .select-icon {
    left: 10px;
    width: 16px;
    height: 16px;
  }

  .terms-group {
    gap: 0.35rem;
  }

  .terms-checkbox {
    width: 15px;
    height: 15px;
  }

  .terms-label {
    font-size: 0.75rem;
  }

  .submit-button {
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    border-radius: 8px;
    gap: 0.35rem;
    margin-top: 0.3rem;
  }

  .error-message,
  .success-message {
    font-size: 0.7rem;
    padding: 0.55rem 0.8rem;
    border-radius: 8px;
  }

  .divider {
    margin: 1rem 0;
    height: 0.5px;
  }

  .divider span {
    font-size: 0.7rem;
    padding: 0 0.6rem;
  }

  .login-link {
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    border-radius: 8px;
  }

  .register-footer {
    font-size: 0.65rem;
    margin-top: 0.8rem;
  }
}

/* ========== RESPONSIVE - MOBILE ULTRA PEQUEÑO (320px - 480px) ========== */
@media (max-width: 480px) {
  .register-container {
    padding: 0.5rem 0;
  }

  .back-button {
    top: 0.8rem;
    left: 0.8rem;
    width: 38px;
    height: 38px;
  }

  .back-icon {
    width: 17px;
    height: 17px;
  }

  .register-content {
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
    width: 75px;
    height: 95px;
    margin-bottom: 0.75rem;
  }

  .register-card {
    padding: 1.2rem 0.95rem;
    margin-bottom: 0.7rem;
    border-radius: 14px;
  }

  .register-title {
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }

  .register-subtitle {
    font-size: 0.75rem;
    margin-bottom: 1.1rem;
  }

  .register-form {
    gap: 0.8rem;
  }

  .form-group {
    gap: 0.3rem;
  }

  .form-label {
    font-size: 0.65rem;
    letter-spacing: 0.04em;
  }

  .form-input,
  .form-select {
    padding: 0.55rem 0.8rem 0.55rem 2rem;
    font-size: 14px;
    border-radius: 7px;
  }

  .input-icon,
  .select-icon {
    left: 9px;
    width: 15px;
    height: 15px;
  }

  .terms-group {
    gap: 0.3rem;
  }

  .terms-checkbox {
    width: 14px;
    height: 14px;
  }

  .terms-label {
    font-size: 0.7rem;
  }

  .submit-button {
    padding: 0.6rem 0.9rem;
    font-size: 0.75rem;
    border-radius: 7px;
    gap: 0.3rem;
    margin-top: 0.25rem;
  }

  .error-message,
  .success-message {
    font-size: 0.65rem;
    padding: 0.5rem 0.75rem;
    border-radius: 7px;
  }

  .divider {
    margin: 0.9rem 0;
    height: 0.5px;
  }

  .divider span {
    font-size: 0.65rem;
    padding: 0 0.5rem;
  }

  .login-link {
    padding: 0.6rem 0.9rem;
    font-size: 0.75rem;
    border-radius: 7px;
  }

  .register-footer {
    font-size: 0.6rem;
    margin-top: 0.7rem;
  }
}

/* ========== RESPONSIVE - MOBILE TINY (280px - 320px) ========== */
@media (max-width: 320px) {
  .register-container {
    padding: 0.25rem 0;
  }

  .back-button {
    top: 0.7rem;
    left: 0.7rem;
    width: 36px;
    height: 36px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .register-content {
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
    width: 65px;
    height: 85px;
    margin-bottom: 0.65rem;
  }

  .register-card {
    padding: 1rem 0.8rem;
    margin-bottom: 0.6rem;
    border-radius: 12px;
  }

  .register-title {
    font-size: 0.95rem;
    margin-bottom: 0.2rem;
  }

  .register-subtitle {
    font-size: 0.7rem;
    margin-bottom: 1rem;
  }

  .register-form {
    gap: 0.7rem;
  }

  .form-group {
    gap: 0.25rem;
  }

  .form-label {
    font-size: 0.6rem;
    letter-spacing: 0.03em;
  }

  .form-input,
  .form-select {
    padding: 0.5rem 0.7rem 0.5rem 1.9rem;
    font-size: 13px;
    border-radius: 6px;
  }

  .input-icon,
  .select-icon {
    left: 8px;
    width: 14px;
    height: 14px;
  }

  .terms-group {
    gap: 0.25rem;
  }

  .terms-checkbox {
    width: 13px;
    height: 13px;
  }

  .terms-label {
    font-size: 0.65rem;
  }

  .submit-button {
    padding: 0.55rem 0.8rem;
    font-size: 0.7rem;
    border-radius: 6px;
    gap: 0.25rem;
    margin-top: 0.2rem;
  }

  .error-message,
  .success-message {
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

  .login-link {
    padding: 0.55rem 0.8rem;
    font-size: 0.7rem;
    border-radius: 6px;
  }

  .register-footer {
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
</style>
