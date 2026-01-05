<template>
  <aside class="desktop-sidebar">
    <!-- Logo del sidebar -->
    <div class="sidebar-header">
      <div class="sidebar-logo">
        <svg viewBox="0 0 64 64" width="36" height="36" class="sidebar-flower-svg" xmlns="http://www.w3.org/2000/svg">
          <g class="flower-petals">
            <ellipse cx="32" cy="16" rx="8" ry="12" fill="#16a34a" opacity="0.9"/>
            <ellipse cx="32" cy="16" rx="8" ry="12" fill="#22c55e" opacity="0.85" transform="rotate(60 32 32)"/>
            <ellipse cx="32" cy="16" rx="8" ry="12" fill="#16a34a" opacity="0.9" transform="rotate(120 32 32)"/>
            <ellipse cx="32" cy="16" rx="8" ry="12" fill="#22c55e" opacity="0.85" transform="rotate(180 32 32)"/>
            <ellipse cx="32" cy="16" rx="8" ry="12" fill="#16a34a" opacity="0.9" transform="rotate(240 32 32)"/>
            <ellipse cx="32" cy="16" rx="8" ry="12" fill="#22c55e" opacity="0.85" transform="rotate(300 32 32)"/>
          </g>
          <circle cx="32" cy="32" r="8" fill="#15803d"/>
          <circle cx="32" cy="32" r="5" fill="#facc15"/>
          <circle cx="32" cy="32" r="2.5" fill="#eab308"/>
        </svg>
      </div>
      <div class="sidebar-title">
        <span class="sidebar-app-name">Sistema de</span>
        <span class="sidebar-app-subtitle">Administración</span>
      </div>
    </div>

    <!-- Navegación del sidebar -->
    <nav class="sidebar-nav">
      <router-link to="/dashboard" class="sidebar-item" :class="{ active: currentRoute === '/dashboard' }">
        <LayoutDashboard :size="20" class="sidebar-icon" />
        <span class="sidebar-text">Directorio</span>
      </router-link>

      <router-link to="/solicitudes" class="sidebar-item" :class="{ active: currentRoute === '/solicitudes' }">
        <FileText :size="20" class="sidebar-icon" />
        <span class="sidebar-text">Solicitudes</span>
        <span v-if="pendingCount > 0" class="sidebar-badge">{{ pendingCount }}</span>
      </router-link>

      <router-link to="/sembradores" class="sidebar-item" :class="{ active: currentRoute === '/sembradores' }">
        <Upload :size="20" class="sidebar-icon" />
        <span class="sidebar-text">Importar Datos</span>
      </router-link>

      <router-link v-if="canViewUsers" to="/usuarios" class="sidebar-item" :class="{ active: currentRoute === '/usuarios' }">
        <Users :size="20" class="sidebar-icon" />
        <span class="sidebar-text">Usuarios</span>
      </router-link>

      <router-link v-if="canViewStats" to="/estadisticas" class="sidebar-item" :class="{ active: currentRoute === '/estadisticas' }">
        <BarChart3 :size="20" class="sidebar-icon" />
        <span class="sidebar-text">Estadísticas</span>
      </router-link>

      <router-link to="/mapa" class="sidebar-item" :class="{ active: currentRoute === '/mapa' }">
        <MapPin :size="20" class="sidebar-icon" />
        <span class="sidebar-text">Mapa</span>
      </router-link>
    </nav>

    <!-- Usuario del sidebar -->
    <div class="sidebar-user">
      <div class="sidebar-user-avatar">
        {{ getInitials(auth.user?.nombre || 'U') }}
      </div>
      <div class="sidebar-user-info">
        <span class="sidebar-user-name">{{ auth.user?.nombre?.split(' ')[0] || 'Usuario' }}</span>
        <span class="sidebar-user-role">{{ formatRole(auth.user?.rol || 'N/A') }}</span>
      </div>
      <button @click="logout" class="sidebar-logout" title="Cerrar sesión">
        <LogOut :size="18" />
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { 
  LayoutDashboard, FileText, Upload, Users, BarChart3, MapPin, LogOut 
} from 'lucide-vue-next'

const props = defineProps<{
  pendingCount?: number
}>()

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const currentRoute = computed(() => route.path)

const canViewUsers = computed(() => {
  const rol = auth.user?.rol || ''
  return ['admin', 'territorial', 'facilitador'].includes(rol)
})

const canViewStats = computed(() => {
  const rol = auth.user?.rol || ''
  return ['admin', 'territorial', 'facilitador'].includes(rol)
})

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

const logout = () => {
  auth.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
.desktop-sidebar {
  display: none;
}

@media (min-width: 1024px) {
  .desktop-sidebar {
    display: flex;
    flex-direction: column;
    width: 220px;
    min-width: 220px;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    background: linear-gradient(180deg, #14532d 0%, #166534 50%, #15803d 100%);
    border-right: 1px solid rgba(22, 163, 74, 0.3);
    z-index: 200;
    transition: all 0.3s ease;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  }
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-logo {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sidebar-flower-svg {
  width: 36px;
  height: 36px;
  filter: drop-shadow(0 2px 6px rgba(22, 163, 74, 0.4));
}

.sidebar-flower-svg .flower-petals {
  transform-origin: 32px 32px;
  animation: flowerSpin 8s linear infinite;
}

@keyframes flowerSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.sidebar-title {
  flex: 1;
  overflow: hidden;
}

.sidebar-app-name {
  font-size: 1.1rem;
  font-weight: 400;
  color: white;
  letter-spacing: 0.3px;
  display: block;
  line-height: 1.2;
}

.sidebar-app-subtitle {
  font-size: 1rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.9);
  display: block;
  line-height: 1.2;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem 0.75rem;
  gap: 0.25rem;
  overflow-y: auto;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
}

.sidebar-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.sidebar-item.active {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.3) 0%, rgba(22, 163, 74, 0.2) 100%);
  color: white;
  border-left: 3px solid #22c55e;
  margin-left: -3px;
  padding-left: calc(1rem + 3px);
}

.sidebar-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}

.sidebar-text {
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
}

.sidebar-badge {
  margin-left: auto;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-radius: 10px;
}

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.sidebar-user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.sidebar-user-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex: 1;
}

.sidebar-user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-user-role {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
}

.sidebar-logout {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 0.5rem;
  color: #fca5a5;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-logout:hover {
  background: rgba(239, 68, 68, 0.3);
  color: white;
}
</style>
