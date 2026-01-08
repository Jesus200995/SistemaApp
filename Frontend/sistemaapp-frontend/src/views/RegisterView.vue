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
      <div class="logo-section">
        <h1 class="app-title">Sistema de Administración</h1>
        <p class="app-subtitle">Crea tu cuenta</p>
      </div>

      <!-- Tarjeta de registro -->
      <div class="register-card">
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
                placeholder="JUAN PÉREZ"
                class="form-input"
                required
                minlength="2"
                @input="formData.nombre = formData.nombre.toUpperCase()"
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

          <!-- Campo CURP -->
          <div class="form-group">
            <label for="curp" class="form-label">CURP</label>
            <div class="input-wrapper">
              <IdCard class="input-icon" />
              <input
                id="curp"
                v-model="formData.curp"
                type="text"
                placeholder="XXXX######HXXXXX##"
                class="form-input"
                maxlength="18"
                minlength="18"
                pattern="[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}"
                @input="formData.curp = formData.curp.toUpperCase()"
                required
              />
            </div>
            <p class="field-hint">18 caracteres alfanuméricos (obligatorio)</p>
          </div>

          <!-- Campo Teléfono -->
          <div class="form-group">
            <label for="telefono" class="form-label">Número de Teléfono</label>
            <div class="input-wrapper">
              <Phone class="input-icon" />
              <input
                id="telefono"
                v-model="formData.telefono"
                type="tel"
                placeholder="10 dígitos"
                class="form-input"
                maxlength="10"
                minlength="10"
                pattern="[0-9]{10}"
                @input="formData.telefono = formData.telefono.replace(/[^0-9]/g, '').slice(0, 10)"
              />
            </div>
            <p class="field-hint" v-if="formData.telefono && formData.telefono.length > 0 && formData.telefono.length < 10">{{ formData.telefono.length }}/10 dígitos</p>
          </div>

          <!-- Campo Territorio -->
          <div class="form-group">
            <label for="territorio" class="form-label">Territorio <span class="required-mark">*</span></label>
            <div class="select-wrapper">
              <MapPin class="select-icon" />
              <select
                id="territorio"
                v-model="formData.territorio"
                class="form-select"
                required
              >
                <option value="">-- Selecciona tu territorio --</option>
                <option value="Acapulco - Centro - Norte - Tierra Caliente">Acapulco - Centro - Norte - Tierra Caliente</option>
                <option value="Acayucan">Acayucan</option>
                <option value="Balancán">Balancán</option>
                <option value="Chihuahua / Sonora">Chihuahua / Sonora</option>
                <option value="Colima">Colima</option>
                <option value="Comalcalco">Comalcalco</option>
                <option value="Córdoba">Córdoba</option>
                <option value="Costa Chica - Montaña">Costa Chica - Montaña</option>
                <option value="Costa Grande - Sierra">Costa Grande - Sierra</option>
                <option value="Durango / Zacatecas">Durango / Zacatecas</option>
                <option value="Hidalgo">Hidalgo</option>
                <option value="Istmo">Istmo</option>
                <option value="Michoacán">Michoacán</option>
                <option value="Mixteca">Mixteca</option>
                <option value="Morelos">Morelos</option>
                <option value="Nayarit / Jalisco">Nayarit / Jalisco</option>
                <option value="Ocosingo">Ocosingo</option>
                <option value="Palenque">Palenque</option>
                <option value="Papantla">Papantla</option>
                <option value="Pichucalco">Pichucalco</option>
                <option value="Puebla">Puebla</option>
                <option value="San Luis Potosí">San Luis Potosí</option>
                <option value="Sinaloa">Sinaloa</option>
                <option value="Tamaulipas">Tamaulipas</option>
                <option value="Tantoyuca">Tantoyuca</option>
                <option value="Tapachula">Tapachula</option>
                <option value="Teapa">Teapa</option>
                <option value="Tlaxcala / Estado de México">Tlaxcala / Estado de México</option>
                <option value="Tzucacab / Opb">Tzucacab / Opb</option>
                <option value="Xpujil">Xpujil</option>
                <option value="Oficinas Centrales">Oficinas Centrales</option>
              </select>
            </div>
          </div>

          <!-- Campo Rol -->
          <div class="form-group">
            <label for="rol" class="form-label">¿Qué tipo de técnico eres?</label>
            <div class="select-wrapper">
              <Briefcase class="select-icon" />
              <select
                id="rol"
                v-model="formData.rol"
                class="form-select"
                required
              >
                <option value="">-- Selecciona tu rol --</option>
                <option value="tecnico_productivo">Técnico Productivo</option>
                <option value="tecnico_social">Técnico Social</option>
              </select>
            </div>
            <p class="rol-hint">
              ¿Eres Facilitador, Territorial o Admin? Debes ser creado por tu supervisor. Solicita a tu superior jerárquico que te registre.
            </p>
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
      <div class="register-footer">
        <p>© 2025 <span class="footer-highlight">Sistema de Administración</span>. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Mail, Lock, AlertCircle, CheckCircle, Briefcase, ArrowLeft, IdCard, Phone, MapPin } from 'lucide-vue-next'
import { getSecureApiUrl } from '../utils/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')

const formData = ref({
  nombre: '',
  email: '',
  password: '',
  confirmPassword: '',
  curp: '',
  telefono: '',
  territorio: '',
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

  // Validar CURP obligatorio
  if (!formData.value.curp || !formData.value.curp.trim()) {
    error.value = 'El CURP es obligatorio'
    return
  }

  const curpRegex = /^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$/
  if (!curpRegex.test(formData.value.curp.toUpperCase())) {
    error.value = 'El CURP no tiene un formato válido (18 caracteres)'
    return
  }

  // Validar teléfono si se proporciona
  if (formData.value.telefono && formData.value.telefono.trim()) {
    const telefonoLimpio = formData.value.telefono.replace(/[^0-9]/g, '')
    if (telefonoLimpio.length < 10) {
      error.value = 'El teléfono debe tener al menos 10 dígitos'
      return
    }
  }

  // Validar territorio (obligatorio)
  if (!formData.value.territorio) {
    error.value = 'Debes seleccionar un territorio'
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
    const apiUrl = getSecureApiUrl()
    
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
        curp: formData.value.curp || null,
        telefono: formData.value.telefono || null,
        territorio: formData.value.territorio,
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
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: clamp(1rem, 2.5vw, 2.5rem) 0;
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

/* ========== BACK BUTTON ========== */
.back-button {
  position: fixed;
  top: clamp(1rem, 2.5vw, 2rem);
  left: clamp(1rem, 2.5vw, 2rem);
  width: clamp(36px, 5vw, 50px);
  height: clamp(36px, 5vw, 50px);
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
  width: clamp(18px, 2.5vw, 24px);
  height: clamp(18px, 2.5vw, 24px);
  color: white;
  stroke-width: 2.5;
}

/* ========== CONTENT ========== */
.register-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: clamp(280px, 45vw, 450px);
  padding: clamp(0.5rem, 1vw, 1rem) clamp(0.4rem, 1vw, 1rem);
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ========== LOGO SECTION ========== */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: clamp(0.6rem, 1.5vw, 1.2rem);
  text-align: center;
  width: 100%;
}

/* Animación de maceta con flor */
.flowerpot-animation {
  width: clamp(70px, 12vw, 120px);
  height: clamp(85px, 14vw, 140px);
  margin-bottom: clamp(0.75rem, 1.5vw, 1.5rem);
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
  font-size: clamp(1rem, 2vw, 1.5rem);
  font-weight: 700;
  background: linear-gradient(135deg, #15803d, #166534);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: clamp(0.15rem, 0.4vw, 0.3rem);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.app-subtitle {
  font-size: clamp(0.65rem, 1.2vw, 0.9rem);
  color: #166534;
  font-weight: 400;
  letter-spacing: 0.01em;
}

/* ========== REGISTER CARD ========== */
.register-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: clamp(14px, 2.5vw, 24px);
  padding: clamp(0.7rem, 1.5vw, 1.2rem) clamp(0.6rem, 1.2vw, 1rem);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(22, 163, 74, 0.1), 0 0 1px rgba(16, 185, 129, 0.2);
  margin-bottom: clamp(0.4rem, 0.8vw, 0.7rem);
}

.register-title {
  font-size: clamp(1rem, 1.8vw, 1.4rem);
  font-weight: 700;
  color: #15803d;
  margin-bottom: clamp(0.15rem, 0.4vw, 0.35rem);
  text-align: center;
  letter-spacing: -0.01em;
}

.register-subtitle {
  font-size: clamp(0.65rem, 1.2vw, 0.9rem);
  color: #166534;
  text-align: center;
  margin-bottom: clamp(0.7rem, 1.5vw, 1.2rem);
  font-weight: 400;
}

/* ========== FORM ========== */
.register-form {
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 1vw, 0.8rem);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: clamp(0.25rem, 0.5vw, 0.45rem);
}

.form-label {
  font-size: clamp(0.6rem, 1.1vw, 0.75rem);
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
  padding: clamp(0.45rem, 0.9vw, 0.65rem) clamp(0.7rem, 1.2vw, 1rem) clamp(0.45rem, 0.9vw, 0.65rem) clamp(1.8rem, 3vw, 2.5rem);
  color: #1e3a2f;
  font-size: clamp(0.7rem, 1.3vw, 0.9rem);
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

/* ========== SELECT ========== */
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-icon {
  position: absolute;
  left: clamp(10px, 1.5vw, 14px);
  width: clamp(15px, 2.2vw, 22px);
  height: clamp(15px, 2.2vw, 22px);
  color: #10b981;
  pointer-events: none;
  z-index: 1;
}

.form-select {
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  border: 1.5px solid rgba(22, 163, 74, 0.3);
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.5rem, 0.9vw, 0.7rem) clamp(0.7rem, 1.2vw, 1rem) clamp(0.5rem, 0.9vw, 0.7rem) clamp(1.8rem, 3vw, 2.6rem);
  color: #1e3a2f;
  font-size: clamp(0.7rem, 1.3vw, 0.9rem);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2315803d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-select:focus {
  outline: none;
  border-color: #16a34a;
  background-color: #ffffff;
  box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.15);
}

.form-select option {
  background-color: #ffffff;
  color: #1e3a2f;
}

.rol-hint {
  font-size: clamp(0.55rem, 1vw, 0.7rem);
  color: #166534;
  margin-top: clamp(0.25rem, 0.5vw, 0.45rem);
  font-style: italic;
  line-height: 1.3;
}

.field-hint {
  font-size: clamp(0.55rem, 1vw, 0.7rem);
  color: #166534;
  margin-top: clamp(0.2rem, 0.4vw, 0.35rem);
  font-style: italic;
}

.required-mark {
  color: #ef4444;
  font-weight: bold;
}

/* ========== TERMS ========== */
.terms-group {
  display: flex;
  align-items: flex-start;
  gap: clamp(0.5rem, 1vw, 0.85rem);
  margin-top: clamp(0.7rem, 1.3vw, 1.2rem);
}

.terms-checkbox {
  width: clamp(14px, 2vw, 20px);
  height: clamp(14px, 2vw, 20px);
  accent-color: #10b981;
  cursor: pointer;
  border-radius: 4px;
  margin-top: 2px;
  flex-shrink: 0;
}

.terms-label {
  font-size: clamp(0.65rem, 1.2vw, 0.85rem);
  color: #166534;
  cursor: pointer;
  line-height: 1.4;
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

/* ========== SUCCESS MESSAGE ========== */
.success-message {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1vw, 0.85rem);
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.6rem, 1.2vw, 1rem) clamp(0.8rem, 1.5vw, 1.3rem);
  color: #86efac;
  font-size: clamp(0.7rem, 1.3vw, 0.9rem);
  animation: slideDown 0.3s ease;
  font-weight: 500;
}

.error-icon,
.success-icon {
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
  gap: clamp(0.35rem, 0.7vw, 0.6rem);
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.55rem, 1vw, 0.85rem) clamp(0.9rem, 1.5vw, 1.4rem);
  font-size: clamp(0.7rem, 1.3vw, 0.95rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
  margin-top: clamp(0.2rem, 0.5vw, 0.4rem);
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
  width: clamp(14px, 2vw, 20px);
  height: clamp(14px, 2vw, 20px);
}

/* ========== DIVIDER ========== */
.divider {
  position: relative;
  height: 1px;
  background: rgba(22, 163, 74, 0.2);
  margin: clamp(1rem, 2vw, 2rem) 0;
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

/* ========== LOGIN LINK ========== */
.login-link {
  width: 100%;
  display: block;
  text-align: center;
  background: rgba(22, 163, 74, 0.08);
  color: #15803d;
  border: 1.5px solid rgba(22, 163, 74, 0.4);
  border-radius: clamp(8px, 1.5vw, 14px);
  padding: clamp(0.5rem, 0.9vw, 0.75rem) clamp(0.9rem, 1.5vw, 1.4rem);
  font-size: clamp(0.7rem, 1.3vw, 0.9rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  text-decoration: none;
  margin-top: clamp(0.2rem, 0.5vw, 0.4rem);
}

.login-link:hover {
  background: rgba(22, 163, 74, 0.15);
  border-color: rgba(22, 163, 74, 0.7);
  color: #166534;
  transform: translateY(-1px);
}

.login-link:active {
  transform: scale(0.98);
}

/* ========== FOOTER ========== */
.register-footer {
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
</style>
