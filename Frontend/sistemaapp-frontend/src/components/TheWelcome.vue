<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Sprout, BarChart3, Clipboard, Users, MessageCircle, MapPin } from 'lucide-vue-next'

const router = useRouter()

const navigateTo = (view: string) => {
  router.push({ name: view })
}
</script>

<template>
  <div class="welcome-wrapper">
    <div class="welcome-content">
      <div class="header-section">
        <h1 class="welcome-title">Bienvenido a SistemaApp</h1>
        <p class="welcome-subtitle">Gestión integral de agricultura y siembra</p>
      </div>

      <div class="quick-actions">
        <button class="action-card" @click="navigateTo('dashboard')">
          <div class="action-icon-box">
            <Sprout class="action-icon" />
          </div>
          <h3>Dashboard</h3>
          <p>Resumen de tus actividades</p>
        </button>

        <button class="action-card" @click="navigateTo('sembradores')">
          <div class="action-icon-box">
            <Users class="action-icon" />
          </div>
          <h3>Sembradores</h3>
          <p>Gestiona tus sembradores</p>
        </button>

        <button class="action-card" @click="navigateTo('usuarios')">
          <div class="action-icon-box">
            <Clipboard class="action-icon" />
          </div>
          <h3>Usuarios</h3>
          <p>Administra usuarios</p>
        </button>

        <button class="action-card" @click="navigateTo('mapa')">
          <div class="action-icon-box">
            <MapPin class="action-icon" />
          </div>
          <h3>Mapa</h3>
          <p>Visualiza ubicaciones</p>
        </button>

        <button class="action-card" @click="navigateTo('chat')">
          <div class="action-icon-box">
            <MessageCircle class="action-icon" />
          </div>
          <h3>Chat</h3>
          <p>Comunícate con el equipo</p>
        </button>

        <button class="action-card" @click="navigateTo('estadisticas')">
          <div class="action-icon-box">
            <BarChart3 class="action-icon" />
          </div>
          <h3>Estadísticas</h3>
          <p>Analiza tus datos</p>
        </button>
      </div>

      <div class="features-section">
        <h2 class="section-title">Características principales</h2>
        <ul class="features-list">
          <li><strong>Gestión de Sembradores:</strong> Administra toda tu información de sembradores</li>
          <li><strong>Mapeo Geográfico:</strong> Visualiza ubicaciones en tiempo real</li>
          <li><strong>Seguimiento:</strong> Monitorea el progreso de tus cultivos</li>
          <li><strong>Comunicación:</strong> Chat integrado para el equipo</li>
          <li><strong>Análisis:</strong> Estadísticas detalladas de tus operaciones</li>
          <li><strong>Solicitudes:</strong> Sistema de gestión de solicitudes</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-wrapper {
  padding: 2rem 1rem;
  min-height: 100%;
}

.welcome-content {
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
  animation: fadeInDown 0.6s ease-out;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 1.125rem;
  color: #94a3b8;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.action-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  backdrop-filter: blur(10px);
}

.action-card:hover {
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(16, 185, 129, 0.5);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.15);
}

.action-icon-box {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.action-icon {
  width: 28px;
  height: 28px;
  color: white;
}

.action-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.5rem;
}

.action-card p {
  font-size: 0.875rem;
  color: #cbd5e1;
}

.features-section {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
  text-align: center;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.features-list li {
  color: #cbd5e1;
  padding: 0.75rem;
  border-left: 2px solid #10b981;
  padding-left: 1rem;
}

.features-list strong {
  color: #10b981;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 1.875rem;
  }

  .welcome-subtitle {
    font-size: 1rem;
  }

  .quick-actions {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .action-card {
    padding: 1rem;
  }

  .features-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .welcome-wrapper {
    padding: 1rem;
  }

  .welcome-title {
    font-size: 1.5rem;
  }

  .quick-actions {
    grid-template-columns: 1fr;
  }

  .features-section {
    padding: 1rem;
  }
}
</style>
