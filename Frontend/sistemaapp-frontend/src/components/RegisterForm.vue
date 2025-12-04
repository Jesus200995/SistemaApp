<template>
  <div class="register-overlay" v-if="mostrarFormulario">
    <div class="register-modal">
      <!-- Header -->
      <div class="modal-header">
        <h2>Crear Nueva Cuenta</h2>
        <button class="close-btn" @click="cerrar">✕</button>
      </div>

      <!-- Form -->
      <form @submit.prevent="registrar" class="register-form">
        <!-- Nombre -->
        <div class="form-group">
          <label for="nombre">Nombre Completo *</label>
          <input
            id="nombre"
            v-model="formData.nombre"
            type="text"
            placeholder="Juan Pérez"
            required
            minlength="2"
          />
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email">Correo Electrónico *</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="juan@ejemplo.com"
            required
          />
        </div>

        <!-- Contraseña -->
        <div class="form-group">
          <label for="password">Contraseña *</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="Mínimo 6 caracteres"
            required
            minlength="6"
          />
        </div>

        <!-- Confirmar Contraseña -->
        <div class="form-group">
          <label for="confirm">Confirmar Contraseña *</label>
          <input
            id="confirm"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="Repite tu contraseña"
            required
            minlength="6"
          />
        </div>

        <!-- Rol -->
        <div class="form-group">
          <label for="rol">¿Qué tipo de usuario eres? *</label>
          <select v-model="formData.rol" id="rol" required>
            <option value="">-- Selecciona un rol --</option>
            <option value="tecnico">Técnico</option>
            <option value="facilitador">Facilitador</option>
          </select>
        </div>

        <!-- Términos -->
        <div class="form-group checkbox">
          <input
            id="terminos"
            v-model="formData.aceptaTerminos"
            type="checkbox"
            required
          />
          <label for="terminos">
            Acepto los
            <a href="#" @click.prevent="verTerminos">términos y condiciones</a>
          </label>
        </div>

        <!-- Errores -->
        <div v-if="error" class="error-message">{{ error }}</div>

        <!-- Botones -->
        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="cargando">
            {{ cargando ? "Registrando..." : "Crear Cuenta" }}
          </button>
          <button type="button" class="btn-secondary" @click="cerrar">
            Cancelar
          </button>
        </div>
      </form>

      <!-- Mensaje de éxito -->
      <div v-if="exito" class="success-message">
        <div class="success-icon">✓</div>
        <h3>¡Cuenta creada exitosamente!</h3>
        <p>Ahora puedes iniciar sesión con tus credenciales.</p>
        <button @click="irAlLogin" class="btn-primary">Ir al Login</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { getSecureApiUrl } from "../utils/api";

const props = defineProps({
  mostrar: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close"]);
const router = useRouter();

const mostrarFormulario = ref(props.mostrar);
const cargando = ref(false);
const error = ref("");
const exito = ref(false);

const formData = ref({
  nombre: "",
  email: "",
  password: "",
  confirmPassword: "",
  rol: "",
  aceptaTerminos: false,
});

// Cerrar modal
const cerrar = () => {
  if (!exito.value) {
    resetForm();
    emit("close");
  }
};

// Reset del formulario
const resetForm = () => {
  formData.value = {
    nombre: "",
    email: "",
    password: "",
    confirmPassword: "",
    rol: "",
    aceptaTerminos: false,
  };
  error.value = "";
  exito.value = false;
};

// Registrar usuario
const registrar = async () => {
  error.value = "";

  // Validaciones locales
  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = "Las contraseñas no coinciden";
    return;
  }

  if (!formData.value.aceptaTerminos) {
    error.value = "Debes aceptar los términos y condiciones";
    return;
  }

  cargando.value = true;

  try {
    const apiUrl = getSecureApiUrl();
    
    const response = await fetch(`${apiUrl}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nombre: formData.value.nombre,
        email: formData.value.email,
        password: formData.value.password,
        rol: formData.value.rol,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Error al registrar usuario");
    }

    const data = await response.json();
    exito.value = true;

    // Auto-cerrar después de 3 segundos
    setTimeout(() => {
      irAlLogin();
    }, 3000);
  } catch (err: any) {
    error.value = err.message || "Error desconocido";
  } finally {
    cargando.value = false;
  }
};

// Ir al login
const irAlLogin = () => {
  resetForm();
  emit("close");
  router.push("/login");
};

// Ver términos (placeholder)
const verTerminos = () => {
  alert(
    "Términos y condiciones:\n\n" +
      "1. Aceptas que tu información será usada para la plataforma\n" +
      "2. Mantendrás confidencial tu contraseña\n" +
      "3. No harás uso malicioso de la plataforma"
  );
};
</script>

<style scoped>
.register-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.register-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: white;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.register-form {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

.form-group.checkbox input {
  width: 18px;
  height: 18px;
  margin: 0;
  cursor: pointer;
}

.form-group.checkbox label {
  margin: 0;
  font-size: 0.85rem;
  cursor: pointer;
}

.form-group.checkbox a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.form-group.checkbox a:hover {
  text-decoration: underline;
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  flex: 1;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.success-message {
  padding: 2rem 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.success-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
}

.success-message h3 {
  color: #333;
  margin: 0;
  font-size: 1.3rem;
}

.success-message p {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .register-modal {
    width: 95%;
    max-width: 100%;
  }

  .modal-header h2 {
    font-size: 1.2rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    flex: 1;
  }
}
</style>
