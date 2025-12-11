<template>
  <div class="hamburger-menu-wrapper">
    <!-- Overlay para cerrar menú al hacer clic fuera -->
    <div v-if="menuOpen" class="menu-overlay" @click="closeMenu"></div>

    <!-- Botón de menú hamburguesa flotante -->
    <button @click="toggleMenu" class="hamburger-btn" :class="{ 'menu-active': menuOpen }">
      <Menu v-if="!menuOpen" :size="18" />
      <X v-else :size="18" />
    </button>

    <!-- Menú desplegable -->
    <Transition name="slide-menu">
      <nav v-if="menuOpen" class="hamburger-menu">
        <div class="menu-header">
          <div class="menu-user-info">
            <div class="menu-avatar">
              {{ getInitials(auth.user?.nombre || 'U') }}
            </div>
            <div class="menu-user-details">
              <span class="menu-user-name">{{ auth.user?.nombre || 'Usuario' }}</span>
              <span class="menu-user-role">{{ formatRole(auth.user?.rol || 'N/A') }}</span>
            </div>
          </div>
        </div>

        <div class="menu-divider"></div>

        <ul class="menu-list">
          <!-- Dashboard/Inicio -->
          <li class="menu-item" @click="navigateTo('/dashboard')">
            <Home :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Inicio</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Panel Global - Solo Admin -->
          <li v-if="auth.user?.rol === 'admin'" class="menu-item" @click="navigateTo('/admin-panel')">
            <Settings :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Panel Global</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Usuarios - Admin, Territorial, Facilitador -->
          <li v-if="['admin', 'territorial', 'facilitador'].includes(auth.user?.rol)" class="menu-item" @click="navigateTo('/usuarios')">
            <Users :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Usuarios</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Estadísticas - Admin, Territorial, Facilitador -->
          <li v-if="['admin', 'territorial', 'facilitador'].includes(auth.user?.rol)" class="menu-item" @click="navigateTo('/estadisticas')">
            <BarChart3 :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Estadísticas</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Solicitudes - Todos -->
          <li class="menu-item" @click="navigateTo('/solicitudes')">
            <FileText :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Solicitudes</span>
            <span v-if="pendingCount > 0" class="menu-badge">{{ pendingCount }}</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Sembradores - Todos -->
          <li class="menu-item" @click="navigateTo('/sembradores')">
            <Sprout :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Sembradores</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Mapa - Todos -->
          <li class="menu-item" @click="navigateTo('/mapa')">
            <MapPin :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Mapa</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>

          <!-- Seguimiento - Solo Técnicos -->
          <li v-if="auth.user?.rol?.includes('tecnico')" class="menu-item" @click="navigateTo('/seguimiento')">
            <Clipboard :size="20" class="menu-item-icon" />
            <span class="menu-item-text">Seguimiento</span>
            <ChevronRight :size="18" class="menu-item-arrow" />
          </li>
        </ul>

        <div class="menu-divider"></div>

        <!-- Botón de cerrar sesión -->
        <button @click="logout" class="menu-logout-btn">
          <LogOut :size="20" />
          <span>Cerrar Sesión</span>
        </button>
      </nav>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { 
  Menu, X, Home, Settings, Users, BarChart3, FileText, 
  Sprout, MapPin, Clipboard, LogOut, ChevronRight 
} from 'lucide-vue-next'

// Props opcionales
defineProps<{
  pendingCount?: number
}>()

const auth = useAuthStore()
const router = useRouter()
const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

const navigateTo = (route: string) => {
  menuOpen.value = false
  router.push(route)
}

const logout = () => {
  menuOpen.value = false
  auth.logout()
  window.location.href = '/login'
}

const getInitials = (name: string): string => {
  if (!name) return 'U'
  const parts = name.split(' ').filter(p => p.length > 0)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

const formatRole = (role: string): string => {
  const roleMap: { [key: string]: string } = {
    admin: 'Administrador',
    territorial: 'Territorial',
    coordinador: 'Coordinador',
    facilitador: 'Facilitador',
    tecnico_productivo: 'Técnico Productivo',
    tecnico_social: 'Técnico Social',
    sembrador: 'Sembrador',
    usuario: 'Usuario',
  }
  return roleMap[role?.toLowerCase()] || role
}
</script>

<style scoped>
/* ========== WRAPPER ========== */
.hamburger-menu-wrapper {
  position: relative;
  z-index: 1000;
}

/* ========== HAMBURGER BUTTON ========== */
.hamburger-btn {
  position: fixed;
  top: 12px;
  right: 16px;
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(15, 23, 42, 0.9);
  border: 1.5px solid rgba(132, 204, 22, 0.5);
  border-radius: 50%;
  color: #84cc16;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

.hamburger-btn:hover {
  background: rgba(132, 204, 22, 0.2);
  border-color: rgba(132, 204, 22, 0.7);
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(132, 204, 22, 0.3);
}

.hamburger-btn:active {
  transform: scale(0.95);
}

.hamburger-btn.menu-active {
  background: linear-gradient(135deg, #10b981 0%, #84cc16 100%);
  color: #0f172a;
  border-color: transparent;
  box-shadow: 0 4px 20px rgba(132, 204, 22, 0.4);
}

/* ========== OVERLAY ========== */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 998;
  animation: fade-in 0.3s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ========== MENU PANEL ========== */
.hamburger-menu {
  position: fixed;
  top: 0;
  right: 0;
  width: 280px;
  max-width: 85vw;
  height: 100vh;
  background: linear-gradient(
    135deg,
    rgba(15, 23, 42, 0.65) 0%,
    rgba(30, 41, 59, 0.55) 50%,
    rgba(15, 23, 42, 0.65) 100%
  );
  border-left: 1px solid rgba(132, 204, 22, 0.25);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  z-index: 999;
  display: flex;
  flex-direction: column;
  box-shadow: 
    -8px 0 32px rgba(0, 0, 0, 0.3),
    inset 1px 0 0 rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  overflow: hidden;
}

/* Transiciones del menú */
.slide-menu-enter-active,
.slide-menu-leave-active {
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.slide-menu-enter-from,
.slide-menu-leave-to {
  transform: translateX(100%);
}

/* ========== MENU HEADER ========== */
.menu-header {
  padding: 1.25rem 1rem;
  padding-top: 1.5rem;
  background: linear-gradient(135deg, rgba(132, 204, 22, 0.08) 0%, rgba(16, 185, 129, 0.05) 100%);
  border-bottom: 1px solid rgba(132, 204, 22, 0.15);
  position: relative;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.menu-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #10b981 0%, #84cc16 50%, #10b981 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
}

@keyframes shimmer {
  0% { background-position: 100% 0; }
  100% { background-position: -100% 0; }
}

.menu-user-info {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.menu-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981 0%, #84cc16 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
  flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(132, 204, 22, 0.3);
}

.menu-user-details {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  overflow: hidden;
}

.menu-user-name {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-user-role {
  font-size: 0.75rem;
  color: #84cc16;
  font-weight: 500;
  text-transform: capitalize;
}

/* ========== DIVIDER ========== */
.menu-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(132, 204, 22, 0.3), transparent);
  margin: 0.5rem 1rem;
}

/* ========== NAVIGATION LIST ========== */
.menu-list {
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
  flex: 1;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  border-radius: 8px;
  margin: 0.15rem 0.5rem;
}

.menu-item:hover {
  background: rgba(132, 204, 22, 0.12);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 
    inset 0 0 0 1px rgba(132, 204, 22, 0.15),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.menu-item:active {
  background: rgba(132, 204, 22, 0.2);
}

.menu-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background: linear-gradient(180deg, #10b981 0%, #84cc16 100%);
  border-radius: 0 3px 3px 0;
  transition: height 0.25s ease;
}

.menu-item:hover::before {
  height: 60%;
}

.menu-item-icon {
  color: #84cc16;
  flex-shrink: 0;
}

.menu-item-text {
  flex: 1;
  font-size: 0.9rem;
  color: #e2e8f0;
  font-weight: 500;
}

.menu-item-arrow {
  color: rgba(148, 163, 184, 0.5);
  transition: all 0.25s ease;
}

.menu-item:hover .menu-item-arrow {
  color: #84cc16;
  transform: translateX(3px);
}

/* ========== BADGE ========== */
.menu-badge {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.15rem 0.4rem;
  border-radius: 8px;
  min-width: 18px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
  animation: pulse-badge 2s infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* ========== LOGOUT BUTTON ========== */
.menu-logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  margin: 0.75rem;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 10px;
  color: #ef4444;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.menu-logout-btn:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.menu-logout-btn:active {
  transform: translateY(0);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 480px) {
  .hamburger-btn {
    top: 12px;
    right: 10px;
    width: 36px;
    height: 36px;
  }

  .hamburger-menu {
    width: 100%;
    max-width: 100%;
  }
  
  .menu-header {
    padding: 1rem 0.85rem;
  }
  
  .menu-avatar {
    width: 42px;
    height: 42px;
    font-size: 1rem;
  }
  
  .menu-user-name {
    font-size: 0.95rem;
  }
}
</style>
