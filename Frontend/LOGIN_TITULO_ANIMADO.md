# ✨ Login - Título con Animación y Subtítulo Verde

## 🎯 Cambios Realizados

### 1️⃣ Título con Animación de Gradiente

**Antes:**
```css
.app-title {
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  /* Sin animación */
}
```

**Después:**
```css
.app-title {
  background: linear-gradient(90deg, #ffffff 0%, #10b981 25%, #ffffff 50%, #10b981 75%, #ffffff 100%);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-flow 4s ease-in-out infinite;
  font-weight: 600;
}

@keyframes gradient-flow {
  0% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
  100% {
    background-position: 0% center;
  }
}
```

✅ **Resultado:** Título con flujo de color blanco-verde suave de lado a lado (4s cycle)

### 2️⃣ Subtítulo "SEMBRANDO VIDA" en Verde

**Antes:**
```html
<p class="app-subtitle">Acceso seguro</p>
```

```css
.app-subtitle {
  color: #cbd5e1;
  font-weight: 400;
}
```

**Después:**
```html
<p class="app-subtitle">SEMBRANDO VIDA</p>
```

```css
.app-subtitle {
  color: #10b981;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

✅ **Resultado:** Subtítulo en MAYÚSCULAS, verde (#10b981), con espaciado

## 🎨 Visual Final

```
┌─────────────────────────────────────┐
│  🌱 Maceta con flores             │
│                                     │
│  Sistema de Administración         │  ← Blanco → Verde → Blanco (animado)
│  SEMBRANDO VIDA                    │  ← Verde, mayúsculas
│                                     │
└─────────────────────────────────────┘
```

## 📝 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `LoginView.vue` | Subtítulo: "Acceso seguro" → "SEMBRANDO VIDA" |
| `LoginView.vue` | CSS: Animación gradiente al título |
| `LoginView.vue` | CSS: Color verde y mayúsculas al subtítulo |

## ✨ Características

- ✅ Título con animación blanco-verde suave
- ✅ Subtítulo "SEMBRANDO VIDA" en mayúsculas verde
- ✅ Identidad visual coherente con Dashboard
- ✅ Responsive en todos los tamaños
- ✅ Animación smooth 4s cycle

## 🚀 Próximos Pasos

Build y deploy del frontend con estos cambios cosméticos.
