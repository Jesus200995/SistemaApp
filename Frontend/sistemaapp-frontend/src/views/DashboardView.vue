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

        <!-- Sección de módulos especializados -->
        <div class="specialized-section">
          <h3 class="section-title">Módulos Especializados</h3>
          
          <div class="specialized-grid">
            <!-- Seguimiento de Campo - Solo técnicos -->
            <router-link
              v-if="auth.user?.rol && (auth.user.rol.includes('tecnico'))"
              to="/seguimiento"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 600, duration: 500 } }"
              class="specialized-card specialized-seguimiento"
            >
              <div class="specialized-icon-wrapper">
                <span class="specialized-icon">📋</span>
              </div>
              <h4 class="specialized-title">Seguimiento de Campo</h4>
              <p class="specialized-desc">Registrar visitas y avances</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Sembradores - Todos los roles -->
            <router-link
              to="/sembradores"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 700, duration: 500 } }"
              class="specialized-card specialized-sembradores"
            >
              <div class="specialized-icon-wrapper">
                <span class="specialized-icon">🌱</span>
              </div>
              <h4 class="specialized-title">Sembradores en Mapa</h4>
              <p class="specialized-desc">Gestionar sembradores</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Reportes - Facilitadores, Territoriales, Admins -->
            <router-link
              v-if="auth.user?.rol && ['facilitador', 'territorial', 'admin'].includes(auth.user.rol)"
              to="/estadisticas"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 800, duration: 500 } }"
              class="specialized-card specialized-reportes"
            >
              <div class="specialized-icon-wrapper">
                <span class="specialized-icon">📊</span>
              </div>
              <h4 class="specialized-title">Reportes y Estadísticas</h4>
              <p class="specialized-desc">Análisis general</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Solicitudes Jerárquicas - Todos los roles -->
            <router-link
              to="/solicitudes"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 850, duration: 500 } }"
              class="specialized-card specialized-solicitudes"
            >
              <div class="specialized-icon-wrapper">
                <FileText class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Solicitudes</h4>
              <p class="specialized-desc">Gestionar solicitudes jerárquicas</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Gestión de Usuarios - Solo admins -->
            <router-link
              v-if="auth.user?.rol === 'admin'"
              to="/usuarios"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 900, duration: 500 } }"
              class="specialized-card specialized-usuarios"
            >
              <div class="specialized-icon-wrapper">
                <span class="specialized-icon">👥</span>
              </div>
              <h4 class="specialized-title">Gestión de Usuarios</h4>
              <p class="specialized-desc">Administrar usuarios</p>
              <div class="card-arrow">→</div>
            </router-link>
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
import { useRouter } from 'vue-router'
import { LogOut, User, Mail, LayoutDashboard, BarChart3, Users, Settings, MapPin, Sprout, FileText } from 'lucide-vue-next'

const auth = useAuthStore()
const router = useRouter()

onMounted(() => {
  auth.fetchProfile()
})

const actions = [
  { title: 'Usuarios', icon: Users, route: '/usuarios' },
  { title: 'Estadísticas', icon: BarChart3, route: '/estadisticas' },
  { title: 'Solicitudes', icon: FileText, route: '/solicitudes' },
  { title: 'Mapa', icon: MapPin, route: '/mapa' },
  { title: 'Sembradores', icon: Sprout, route: '/sembradores' },
]

const goTo = (route) => {
  if (route === '/usuarios' || route === '/estadisticas' || route === '/mapa' || route === '/sembradores' || route === '/solicitudes') {
    router.push(route)
  } else {
    alert(`👉 Próximamente: ${route}`)
  }
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
  width: 100vw;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  overflow-x: hidden;
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
  font-size: 1.25rem;
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
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  font-size: 0.75rem;
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.logout-btn:active {
  transform: translateY(0);
}

.logout-icon {
  width: 16px;
  height: 16px;
}

.logout-text {
  font-size: 0.75rem;
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
  align-items: flex-start;
  justify-content: center;
  padding: 1.5rem 0.75rem;
  overflow-y: auto;
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
  padding: 1.25rem;
  backdrop-filter: blur(10px);
  text-align: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.profile-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 12px 48px rgba(16, 185, 129, 0.1);
}

.avatar-wrapper {
  position: relative;
  width: 110px;
  height: 110px;
  margin: 0 auto 1.25rem;
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
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.4; }
}

.avatar-image {
  position: relative;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  border: 4px solid #10b981;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.welcome-section {
  margin-bottom: 1rem;
}

.welcome-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #e2e8f0;
}

.user-name {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.info-box {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 0.875rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
}

.info-text {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.info-label {
  font-size: 0.65rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 0.85rem;
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
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #cbd5e1;
  text-align: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
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
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
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
  width: 48px;
  height: 48px;
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
  width: 24px;
  height: 24px;
  color: white;
}

.action-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #cbd5e1;
  text-align: center;
  transition: color 0.3s ease;
}

.action-card:hover .action-title {
  color: #10b981;
}

/* ========== SPECIALIZED MODULES SECTION ========== */
.specialized-section {
  margin-bottom: 1.5rem;
}

.specialized-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .specialized-grid {
    grid-template-columns: 1fr;
  }
}

.specialized-card {
  position: relative;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  text-decoration: none;
  color: inherit;
  overflow: hidden;
}

.specialized-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: 0;
}

.specialized-card:hover::before {
  left: 100%;
}

.specialized-card:hover {
  transform: translateY(-8px);
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 16px 32px rgba(16, 185, 129, 0.15);
}

.specialized-card:active {
  transform: translateY(-2px);
}

.specialized-icon-wrapper {
  position: relative;
  z-index: 1;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.specialized-icon {
  font-size: 2rem;
  transition: transform 0.3s ease;
}

.specialized-card:hover .specialized-icon {
  transform: scale(1.2);
}

/* Variantes de color por tarjeta */
.specialized-seguimiento .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(34, 197, 94, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.specialized-seguimiento:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(34, 197, 94, 0.25));
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.specialized-sembradores .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(16, 185, 129, 0.15));
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.specialized-sembradores:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(16, 185, 129, 0.25));
  box-shadow: 0 8px 16px rgba(34, 197, 94, 0.3);
}

.specialized-reportes .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.15));
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.specialized-reportes:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(37, 99, 235, 0.25));
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

.specialized-usuarios .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(139, 92, 246, 0.15));
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.specialized-usuarios:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(139, 92, 246, 0.25));
  box-shadow: 0 8px 16px rgba(168, 85, 247, 0.3);
}

.specialized-solicitudes .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.specialized-solicitudes:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(5, 150, 105, 0.25));
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.specialized-title {
  position: relative;
  z-index: 1;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: #e2e8f0;
  transition: color 0.3s ease;
}

.specialized-card:hover .specialized-title {
  color: #10b981;
}

.specialized-desc {
  position: relative;
  z-index: 1;
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
  transition: color 0.3s ease;
}

.specialized-card:hover .specialized-desc {
  color: #cbd5e1;
}

.card-arrow {
  position: absolute;
  bottom: 1rem;
  right: 1.5rem;
  font-size: 1.25rem;
  color: #10b981;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
  z-index: 1;
}

.specialized-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(16, 185, 129, 0.3);
}

.stat-icon {
  font-size: 1.4rem;
  margin-bottom: 0.25rem;
}

.stat-text {
  font-size: 0.65rem;
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
  padding: 1rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  font-size: 0.75rem;
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

  .specialized-grid {
    grid-template-columns: 1fr;
  }

  .specialized-card {
    padding: 1.25rem;
  }

  .specialized-icon-wrapper {
    width: 56px;
    height: 56px;
  }

  .specialized-icon {
    font-size: 1.75rem;
  }

  .specialized-title {
    font-size: 0.95rem;
  }

  .specialized-desc {
    font-size: 0.7rem;
  }

  .card-arrow {
    font-size: 1rem;
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
