<template>
  <div class="about-container">
    <!-- Header -->
    <header class="about-header">
      <button @click="goBack" class="back-button">
        <ArrowLeft class="back-icon" />
      </button>
      <h1 class="page-title">Acerca de SistemaApp</h1>
    </header>

    <!-- Decorative Background -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Content -->
    <main class="about-main">
      <div class="about-content">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-wrapper">
            <div class="logo-glow"></div>
            <div class="logo-box">
              <LayoutDashboard class="logo-icon" />
            </div>
          </div>
          <h2 class="app-name">SistemaApp</h2>
          <p class="app-version">v1.0.0</p>
        </div>

        <!-- Description Section -->
        <section class="info-section">
          <h3 class="section-title">
            <Info class="section-icon" />
            Descripción
          </h3>
          <p class="section-text">
            SistemaApp es una plataforma integral diseñada para optimizar la gestión de operaciones agrícolas. 
            Facilita el seguimiento de sembradores, monitoreo de campos, gestión de solicitudes jerárquicas y 
            análisis estadístico de datos en tiempo real.
          </p>
        </section>

        <!-- Features Section -->
        <section class="info-section">
          <h3 class="section-title">
            <Sparkles class="section-icon" />
            Características Principales
          </h3>
          <div class="features-list">
            <div class="feature-item">
              <div class="feature-icon">
                <MapPin class="icon-svg" />
              </div>
              <div class="feature-content">
                <h4 class="feature-title">Gestión de Mapas</h4>
                <p class="feature-desc">Visualiza y gestiona sembradores en mapas interactivos</p>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <BarChart3 class="icon-svg" />
              </div>
              <div class="feature-content">
                <h4 class="feature-title">Estadísticas en Tiempo Real</h4>
                <p class="feature-desc">Análisis profundo de datos y métricas de desempeño</p>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <Clipboard class="icon-svg" />
              </div>
              <div class="feature-content">
                <h4 class="feature-title">Seguimiento de Campo</h4>
                <p class="feature-desc">Registro detallado de visitas y avances en terreno</p>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <Users class="icon-svg" />
              </div>
              <div class="feature-content">
                <h4 class="feature-title">Gestión de Usuarios</h4>
                <p class="feature-desc">Control administrativo con roles y permisos personalizados</p>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <FileText class="icon-svg" />
              </div>
              <div class="feature-content">
                <h4 class="feature-title">Solicitudes Jerárquicas</h4>
                <p class="feature-desc">Sistema de aprobaciones estructurado según niveles jerárquicos</p>
              </div>
            </div>

            <div class="feature-item">
              <div class="feature-icon">
                <MessageCircle class="icon-svg" />
              </div>
              <div class="feature-content">
                <h4 class="feature-title">Chat en Tiempo Real</h4>
                <p class="feature-desc">Comunicación directa entre equipos de trabajo</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Technology Section -->
        <section class="info-section">
          <h3 class="section-title">
            <Zap class="section-icon" />
            Tecnología
          </h3>
          <div class="tech-grid">
            <div class="tech-item">
              <span class="tech-name">Vue.js 3</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">TypeScript</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">Vite</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">Pinia</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">Prisma</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">Node.js</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">PostgreSQL</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">WebSocket</span>
            </div>
          </div>
        </section>

        <!-- Footer Info -->
        <section class="info-section footer-section">
          <div class="footer-content">
            <p class="footer-text">© 2025 SistemaApp. Todos los derechos reservados.</p>
            <p class="footer-version">Versión 1.0.0 • Última actualización: Enero 2025</p>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { 
  ArrowLeft, 
  LayoutDashboard, 
  Info, 
  Sparkles, 
  MapPin, 
  BarChart3, 
  Clipboard, 
  Users, 
  FileText, 
  MessageCircle, 
  Zap 
} from 'lucide-vue-next'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.about-container {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #e2e8f0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  position: relative;
  overflow-x: hidden;
}

/* ========== DECORATIVE BACKGROUND ========== */
.background-decoration {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  opacity: 0.15;
  filter: blur(40px);
}

.blob-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  top: -100px;
  left: -100px;
  animation: float 8s ease-in-out infinite;
}

.blob-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #8b5cf6, #10b981);
  bottom: -50px;
  right: -50px;
  animation: float 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #06b6d4, #f59e0b);
  top: 50%;
  right: 10%;
  animation: float 9s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(20px, -20px); }
  50% { transform: translate(-20px, 20px); }
  75% { transform: translate(20px, 20px); }
}

/* ========== HEADER ========== */
.about-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.back-button {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.back-button:hover {
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.back-icon {
  width: 20px;
  height: 20px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ========== MAIN CONTENT ========== */
.about-main {
  flex: 1;
  position: relative;
  z-index: 5;
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  overflow-y: auto;
}

.about-content {
  width: 100%;
  max-width: 900px;
}

/* ========== LOGO SECTION ========== */
.logo-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
  border-radius: 24px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(10px);
}

.logo-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-glow {
  position: absolute;
  inset: -15px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  border-radius: 50%;
  opacity: 0.2;
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.4; }
}

.logo-box {
  position: relative;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.3);
}

.logo-icon {
  width: 56px;
  height: 56px;
  color: white;
}

.app-name {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.app-version {
  color: #94a3b8;
  font-size: 0.9rem;
}

/* ========== INFO SECTION ========== */
.info-section {
  margin-bottom: 2rem;
  padding: 1.75rem;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.7));
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.info-section:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #e2e8f0;
}

.section-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
}

.section-text {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #cbd5e1;
}

/* ========== FEATURES LIST ========== */
.features-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.feature-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.feature-item:hover {
  border-color: rgba(16, 185, 129, 0.3);
  background: rgba(16, 185, 129, 0.05);
  transform: translateY(-4px);
}

.feature-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg {
  width: 24px;
  height: 24px;
  color: #10b981;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}

.feature-desc {
  font-size: 0.8rem;
  color: #94a3b8;
}

/* ========== TECH GRID ========== */
.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.tech-item {
  padding: 0.75rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
}

.tech-item:hover {
  background: rgba(16, 185, 129, 0.2);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.tech-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #10b981;
}

/* ========== FOOTER SECTION ========== */
.footer-section {
  background: transparent;
  border: none;
  text-align: center;
  margin-top: 1rem;
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-text {
  font-size: 0.9rem;
  color: #cbd5e1;
}

.footer-version {
  font-size: 0.75rem;
  color: #64748b;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .about-header {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.25rem;
  }

  .about-main {
    padding: 1rem 0.75rem;
  }

  .logo-section {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  .app-name {
    font-size: 1.5rem;
  }

  .info-section {
    padding: 1.25rem;
  }

  .section-title {
    font-size: 1.1rem;
  }

  .features-list {
    grid-template-columns: 1fr;
  }

  .tech-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 480px) {
  .about-header {
    padding: 0.75rem;
  }

  .page-title {
    font-size: 1rem;
  }

  .back-button {
    width: 36px;
    height: 36px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .logo-wrapper {
    width: 100px;
    height: 100px;
  }

  .logo-box {
    width: 85px;
    height: 85px;
  }

  .logo-icon {
    width: 45px;
    height: 45px;
  }

  .app-name {
    font-size: 1.25rem;
  }

  .about-main {
    padding: 1rem 0.5rem;
  }

  .info-section {
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .tech-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
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
