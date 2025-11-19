import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// @ts-ignore
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      // @ts-ignore
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/login',
      name: 'login',
      // @ts-ignore
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      // @ts-ignore
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      // @ts-ignore
      component: () => import('../views/UsuariosView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/estadisticas',
      name: 'estadisticas',
      // @ts-ignore
      component: () => import('../views/EstadisticasView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/mapa',
      name: 'mapa',
      // @ts-ignore
      component: () => import('../views/MapaView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/chat',
      name: 'chat',
      // @ts-ignore
      component: () => import('../views/ChatView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/sembradores',
      name: 'sembradores',
      // @ts-ignore
      component: () => import('../views/SembradoresView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/seguimiento',
      name: 'seguimiento',
      // @ts-ignore
      component: () => import('../views/SeguimientoView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/solicitudes',
      name: 'solicitudes',
      // @ts-ignore
      component: () => import('../views/SolicitudesView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida
    },
    {
      path: '/admin-panel',
      name: 'admin-panel',
      // @ts-ignore
      component: () => import('../views/AdminDashboardView.vue'),
      meta: { requiresAuth: true }, // 🔒 protegida, solo admin
    },
  ],
})

// ✅ Middleware de protección y autenticación
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  const token = auth.token

  // 🔄 Primera carga: si hay token pero no hay usuario, obtener perfil
  if (token && !auth.user && from.path === '/') {
    try {
      await auth.fetchProfile()
    } catch (error) {
      console.error('Error al cargar perfil:', error)
      // Si el token es inválido, limpiar sesión
      auth.logout()
      return next('/login')
    }
  }

  // 🔒 Si la ruta requiere autenticación pero no hay token
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  // 🏠 Si está loguado y trata de ir a login/register, redirigir a dashboard
  if (token && (to.name === 'login' || to.name === 'register')) {
    return next('/dashboard')
  }

  // 🚀 Si está loguado y trata de acceder a / (home), redirigir a dashboard
  if (token && to.path === '/') {
    return next('/dashboard')
  }

  // ✅ Continuar normalmente
  next()
})

export default router
