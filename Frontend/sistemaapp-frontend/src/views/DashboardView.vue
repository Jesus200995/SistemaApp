<template>
  <div class="dashboard-container">
    <!-- Header moderno -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <LayoutDashboard class="logo-svg" />
          </div>
          <div class="logo-text">
            <h1 class="app-title">SistemaApp</h1>
            <p class="app-subtitle">Panel de Control</p>
          </div>
        </div>
        <button @click="logout" class="logout-btn">
          <LogOut class="logout-icon" />
          <span class="logout-text">Salir</span>
        </button>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="dashboard-main">
      <div class="dashboard-content">
        <!-- Tarjeta de perfil -->
        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.8, y: 50 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
          class="profile-card"
        >
          <!-- Avatar con glow -->
          <div class="avatar-wrapper">
            <div class="avatar-glow"></div>
            <img
              src="https://ui-avatars.com/api/?name=Usuario&background=10b981&color=fff&size=200&bold=true&rounded=true"
              alt="avatar"
              class="avatar-image"
            />
          </div>

          <!-- Bienvenida -->
          <div class="welcome-section">
            <h2 class="welcome-title">¡Bienvenido! 👋</h2>
            <p class="user-name">{{ auth.user?.nombre || 'Usuario' }}</p>
          </div>

          <!-- Información -->
          <div class="info-box">
            <div class="info-item">
              <User class="info-icon" />
              <div class="info-text">
                <span class="info-label">Rol</span>
                <span class="info-value">{{ auth.user?.rol || 'N/A' }}</span>
              </div>
            </div>
            <div class="divider"></div>
            <div class="info-item">
              <Mail class="info-icon" />
              <div class="info-text">
                <span class="info-label">Correo</span>
                <span class="info-value">{{ auth.user?.email || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Sección de acciones -->
        <div class="actions-section">
          <h3 class="section-title">Acceso Rápido</h3>
          
          <div class="actions-grid">
            <div
              v-for="(action, index) in actions"
              :key="action.title"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 500 + index * 100, duration: 500 } }"
              @click="goTo(action.route)"
              class="action-card"
            >
              <div class="action-icon-wrapper">
                <component :is="action.icon" class="action-icon" />
              </div>
              <span class="action-title">{{ action.title }}</span>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div
          v-motion
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1, transition: { delay: 800, duration: 600 } }"
          class="stats-grid"
        >
          <div class="stat-card stat-online">
            <div class="stat-icon">✓</div>
            <p class="stat-text">Conectado</p>
          </div>
          <div class="stat-card stat-secure">
            <div class="stat-icon">🛡️</div>
            <p class="stat-text">Seguro</p>
          </div>
          <div class="stat-card stat-active">
            <div class="stat-icon">⚡</div>
            <p class="stat-text">Activo</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer
      v-motion
      :initial="{ opacity: 0 }"
      :enter="{ opacity: 1, transition: { delay: 1000, duration: 600 } }"
      class="dashboard-footer"
    >
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { LogOut, User, Mail, LayoutDashboard, BarChart3, Users, Settings, MapPin } from 'lucide-vue-next'

const auth = useAuthStore()

onMounted(() => {
  auth.fetchProfile()
})

const actions = [
  { title: 'Usuarios', icon: Users, route: '/usuarios' },
  { title: 'Estadísticas', icon: BarChart3, route: '/estadisticas' },
  { title: 'Mapa', icon: MapPin, route: '/mapa' },
  { title: 'Configuración', icon: Settings, route: '/config' },
]

const goTo = (route) => {
  alert(`👉 Próximamente: ${route}`)
}

const logout = () => {
  auth.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ========== HEADER ========== */
.dashboard-header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1rem 0;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.logo-svg {
  width: 28px;
  height: 28px;
  color: white;
}

.logo-text h1 {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text p {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.25rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.logout-btn:active {
  transform: translateY(0);
}

.logout-icon {
  width: 18px;
  height: 18px;
}

.logout-text {
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .logout-text {
    display: none;
  }

  .logout-btn {
    padding: 0.5rem;
  }

  .logo-icon {
    width: 40px;
    height: 40px;
  }

  .logo-text h1 {
    font-size: 1.25rem;
  }
}

/* ========== MAIN CONTENT ========== */
.dashboard-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.dashboard-content {
  width: 100%;
  max-width: 900px;
}

/* ========== PROFILE CARD ========== */
.profile-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 24px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.profile-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 12px 48px rgba(16, 185, 129, 0.1);
}

.avatar-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 0 auto 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-glow {
  position: absolute;
  inset: -10px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  border-radius: 50%;
  opacity: 0.2;
  blur: 20px;
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.4; }
}

.avatar-image {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #10b981;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.welcome-section {
  margin-bottom: 1.5rem;
}

.welcome-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #e2e8f0;
}

.user-name {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
}

.info-box {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  flex-shrink: 0;
}

.info-text {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.info-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  word-break: break-all;
}

.divider {
  height: 1px;
  background: rgba(148, 163, 184, 0.1);
}

/* ========== ACTIONS SECTION ========== */
.actions-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #cbd5e1;
  text-align: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (max-width: 768px) {
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
}

.action-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  transform: translateY(-8px);
  border-color: rgba(16, 185, 129, 0.5);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.2);
}

.action-card:active {
  transform: translateY(-2px);
}

.action-icon-wrapper {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
}

.action-icon {
  width: 28px;
  height: 28px;
  color: white;
}

.action-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #cbd5e1;
  text-align: center;
  transition: color 0.3s ease;
}

.action-card:hover .action-title {
  color: #10b981;
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(16, 185, 129, 0.3);
}

.stat-icon {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.stat-text {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.stat-online {
  border-left: 3px solid #10b981;
}

.stat-secure {
  border-left: 3px solid #3b82f6;
}

.stat-active {
  border-left: 3px solid #a855f7;
}

/* ========== FOOTER ========== */
.dashboard-footer {
  text-align: center;
  padding: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  font-size: 0.875rem;
  color: #94a3b8;
}

.footer-highlight {
  color: #10b981;
  font-weight: 600;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 640px) {
  .dashboard-main {
    padding: 1rem 0.75rem;
  }

  .profile-card {
    padding: 1.5rem 1rem;
    margin-bottom: 1.5rem;
  }

  .avatar-wrapper {
    width: 100px;
    height: 100px;
    margin-bottom: 1.5rem;
  }

  .avatar-image {
    width: 80px;
    height: 80px;
  }

  .welcome-title {
    font-size: 1.5rem;
  }

  .user-name {
    font-size: 1.5rem;
  }

  .info-box {
    padding: 1rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .action-card {
    padding: 1rem;
  }

  .action-icon-wrapper {
    width: 48px;
    height: 48px;
  }

  .action-icon {
    width: 24px;
    height: 24px;
  }
}

/* ========== ANIMACIONES ========== */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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
