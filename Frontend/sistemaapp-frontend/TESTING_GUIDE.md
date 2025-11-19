# 🧪 Guía de Verificación y Testing

## ✅ Checklist de Verificación Local

### 1. Compilación
```bash
cd Frontend/sistemaapp-frontend

# Instalar dependencias (si no están instaladas)
npm install

# Compilar en desarrollo
npm run dev

# Compilar para producción
npm run build
```

**Esperado**: Sin errores de compilación ✅

---

## 📱 Testing en Navegador (Desktop)

### Abrir DevTools
1. **F12** o **Right-click → Inspect**
2. Ir a **Device Toolbar** (Ctrl+Shift+M)

### Tamaños para Probar

```
iPhone SE (320px)     → 🔴 CRÍTICO
iPhone 12 (390px)     → 🔴 CRÍTICO
iPhone 14 Pro (430px) → 🟡 IMPORTANTE
Galaxy S21 (360px)    → 🔴 CRÍTICO
iPad Mini (768px)     → 🟡 IMPORTANTE
iPad Pro (1024px)     → 🟢 OK
```

### En cada Breakpoint, Verificar

#### 🌐 **Navbar**
- [ ] Logo visible sin cortes
- [ ] Texto "SistemaApp" legible
- [ ] Botón logout no se superpone
- [ ] Notificaciones dropdown cabe en pantalla
- [ ] Espaciado top correcto (sin ocupar mucho)
- [ ] Height: 44-56px respetado

#### 🏠 **Dashboard**
- [ ] Avatar visible sin cortes
- [ ] Nombre usuario legible
- [ ] Rol e información visible
- [ ] Botones de acción rápido en grid correcto
- [ ] Tarjetas de módulos especializados adaptan bien
- [ ] Notificaciones lista no muy alta
- [ ] Footer legible

#### 🔐 **Login/Register**
- [ ] Flor SVG visible sin cortes
- [ ] Título centrado
- [ ] Inputs rellena todo el ancho
- [ ] Botón login visible sin scroll
- [ ] Enlace "Crear cuenta" o "Volver" visible
- [ ] Errores se muestran sin ocultar inputs

---

## 🎮 Testing en Dispositivo Real

### iOS (iPhone)

#### Instalación PWA
1. Abre Safari
2. Navega a: `https://tuapp.com`
3. Toca **Compartir** (↑)
4. Toca **Añadir a pantalla de inicio**
5. Asigna nombre: "SistemaApp"
6. Toca **Añadir**

#### Verificar en App Instalada
- [ ] Navbar visible correctamente
- [ ] Sin scroll horizontal
- [ ] Seguro que no toca el notch
- [ ] Safe area respetada (si tiene Dynamic Island)
- [ ] Bottom no sale fuera de pantalla

#### Gestos
- [ ] Scroll vertical suave
- [ ] Tap en botones funciona
- [ ] Swipe no causa problemas

### Android (Samsung, etc.)

#### Instalación PWA
1. Abre Chrome
2. Navega a: `https://tuapp.com`
3. Menú (⋮) → **Instalar aplicación**
4. Confirma instalación

#### Verificar en App Instalada
- [ ] Navbar visible correctamente
- [ ] Sin scroll horizontal
- [ ] Status bar respetada
- [ ] Botón home y back funcionan
- [ ] Navbar notch bottom respetada

#### Gestos
- [ ] Scroll vertical suave
- [ ] Back button funciona
- [ ] Swipe gestures OK

---

## 🔍 Verificación Visual

### Pantalla iPhone SE (320px) - CRÍTICA

```
┌─────────────────────┐ ← Navbar 44-48px
│ 🌱 SistemaApp  ⚙️   │
├─────────────────────┤ 
│  [Avatar] ✨        │ ← Sin scroll horizontal
│  Bienvenido         │
│  ─────────────      │
│  Técnico / Admin    │
├─────────────────────┤
│  [Inicio] [Mapa]    │ ← 2 columnas
│  [Chat]   [Reporte] │
├─────────────────────┤
│  📋 Seguimiento     │ ← 1 columna
│  🌾 Sembradores     │
│  📊 Reportes        │
├─────────────────────┤
│  Notificaciones: 0  │
│  © 2025 SistemaApp │
└─────────────────────┘
```

### Pantalla iPad (768px) - OK

```
┌──────────────────────────────────────────┐
│ 🌱 SistemaApp │ Links │ Notif │ 👤 Salir│
├──────────────────────────────────────────┤
│         [Avatar]                         │
│     Bienvenido, Usuario                 │
│  ───────────────────────────────────    │
│  [Inicio] [Mapa] [Chat] [Usuarios]     │
├──────────────────────────────────────────┤
│ ⬜ Seguimiento │ 🌾 Sembradores         │
│ 📊 Reportes   │ 📁 Solicitudes         │
│ ⚙️ Admin      │                         │
└──────────────────────────────────────────┘
```

---

## 🐛 Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| Navbar toca notch iPhone | ✅ Ya fijo con min-height 48px |
| Content muy pegado | ✅ Ya optimizado padding |
| Scroll horizontal | ✅ Ancho max-width ajustado |
| Fuente demasiado pequeña | Puede aumentar si es necesario |
| Elementos se superponen | ✅ Gaps y padding optimizados |
| Botones difíciles de tocar | ✅ Todos +44x44px mínimo |

---

## 📊 Performance Check

### Lighthouse (Chrome DevTools)

1. **Abre DevTools** (F12)
2. **Lighthouse** tab
3. Click **Analyze page load**

**Objetivo**:
- Performance: >85
- Accessibility: >90
- Best Practices: >90
- SEO: >90
- PWA: >90

---

## 🔄 PWA Auto-Update Test

### Paso 1: Instala en Móvil
```bash
# En tu servidor
npm run build
# Sube /dist a hosting
```

### Paso 2: Abre app en móvil
Navega a tu dominio y instala PWA

### Paso 3: Hace un cambio pequeño
En `Dashboard View` cambia:
```vue
<!-- Antes -->
<p>© 2025 SistemaApp</p>

<!-- Después -->
<p>© 2025 SistemaApp v1.1</p>
```

### Paso 4: Sube cambios
```bash
npm run build
# Sube nuevos archivos
```

### Paso 5: Verifica en móvil
- [ ] Reabre app (no cierre completamente)
- [ ] Ver modal "Actualizando..." 🔄
- [ ] Spinner gira 2 segundos
- [ ] Modal "App Actualizada ✅"
- [ ] Recarga automática
- [ ] Ves "© 2025 SistemaApp v1.1" ✅

---

## 🎯 Checklist Final de Deployment

### Antes de Subir a Producción

- [ ] npm run build sin errores
- [ ] Probado en iPhone SE (320px)
- [ ] Probado en Galaxy (360px)
- [ ] Probado en iPad (768px)
- [ ] Navbar funciona en todos
- [ ] Scroll sin problemas
- [ ] Botones accesibles (44x44px+)
- [ ] PWA se instala bien
- [ ] Auto-update funciona
- [ ] Lighthouse score >85
- [ ] Sin console errors
- [ ] Sin warnings críticos

### Archivos Críticos Modificados

```
✅ src/components/Navbar.vue
✅ src/views/DashboardView.vue
✅ src/views/LoginView.vue
✅ src/views/RegisterView.vue
✅ src/components/UpdateModal.vue
✅ src/composables/usePWAUpdate.ts
✅ src/App.vue
```

---

## 📝 Comandos Útiles

```bash
# Desarrollo con hot-reload
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview

# Lint code
npm run lint

# Type check
npm run type-check

# Test PWA localmente
python -m http.server 8000  # En carpeta dist/
# Abre http://localhost:8000
```

---

## 🆘 Si Algo Sale Mal

### Error de Build
```bash
# Limpia cache y reinstala
rm -rf node_modules
rm package-lock.json
npm install
npm run build
```

### Cambios No Se Ven en Mobile
```bash
# Fuerza refresh de PWA
1. Abre DevTools
2. Storage → Clear All
3. Cierra app completamente
4. Reabre
```

### Navbar Se Ve Mal
- Abre el archivo en VS Code
- Busca `.navbar-container`
- Verifica: `padding: 0.6rem 1rem;` (correcto)
- Verifica: `min-height: 56px;` (correcto)

---

## 📞 Soporte

Si encuentras problemas:

1. **Verifica console** (F12 → Console)
2. **Busca errores** en output
3. **Compara con este doc** punto por punto
4. **Reinstala dependencias** si persiste

---

## ✨ Última Verificación

Abre tu app en mobile y responde:

```
¿Se ve la parte superior bien?                  SI ☐ NO ☐
¿Cabe todo sin scroll horizontal?               SI ☐ NO ☐
¿Los botones son tocables (suficientemente grandes)? SI ☐ NO ☐
¿Las fuentes son legibles?                      SI ☐ NO ☐
¿Navbar no toca el notch?                       SI ☐ NO ☐
¿Dashboard se carga rápido?                     SI ☐ NO ☐
¿Puedo hacer login sin problemas?               SI ☐ NO ☐
¿PWA auto-update funciona?                      SI ☐ NO ☐
```

**Si todo es "SI" → ¡Felicidades! 🎉 Tu app está lista para producción.**

---

**Última actualización**: 19 de Noviembre de 2025
**Estado**: ✅ Completado y Validado
