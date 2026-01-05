<template>
  <header class="desktop-header">
    <div class="breadcrumb-nav">
      <router-link to="/dashboard" class="breadcrumb-item">
        <Home :size="16" />
        <span>Directorio</span>
      </router-link>
      <ChevronRight :size="14" class="breadcrumb-separator" />
      <router-link to="/solicitudes" class="breadcrumb-item">
        <FileText :size="16" />
        <span>Solicitudes</span>
      </router-link>
      <ChevronRight :size="14" class="breadcrumb-separator" />
      <router-link to="/sembradores" class="breadcrumb-item">
        <Upload :size="16" />
        <span>Importar Datos</span>
      </router-link>
      <span class="breadcrumb-item catalogs">Catálogos</span>
    </div>
    <div class="header-user-section">
      <User :size="18" class="header-user-icon" />
      <span class="header-user-name">{{ formatRole(auth.user?.rol || 'Usuario') }}</span>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { Home, FileText, Upload, User, ChevronRight } from 'lucide-vue-next'

const auth = useAuthStore()

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
.desktop-header {
  display: none;
}

@media (min-width: 1024px) {
  .desktop-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(10px);
    position: sticky;
    top: 0;
    z-index: 100;
  }
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.75rem;
  font-size: 0.85rem;
  color: #374151;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.breadcrumb-item:hover {
  background: rgba(22, 163, 74, 0.08);
  color: #15803d;
}

.breadcrumb-item.catalogs {
  color: #6b7280;
  cursor: default;
}

.breadcrumb-item.catalogs:hover {
  background: transparent;
}

.breadcrumb-separator {
  color: #9ca3af;
}

.header-user-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(30, 58, 95, 0.05);
  border-radius: 8px;
}

.header-user-icon {
  color: #1e3a5f;
}

.header-user-name {
  font-size: 0.85rem;
  font-weight: 500;
  color: #1e3a5f;
}
</style>
