# 📊 Módulo de Reportes y Estadísticas - Manual de Usuario

## 🎯 Descripción General

El **Módulo de Reportes y Estadísticas** es una herramienta integral para visualizar datos agregados del sistema en tiempo real. Proporciona gráficas, tablas y métricas clave para análisis de campo.

---

## 👥 Acceso por Rol

### ✅ Pueden acceder:
- **Administrador**: Ve todos los datos del sistema
- **Territorial**: Ve datos de su territorio y subordinados
- **Facilitador**: Ve datos de técnicos asignados

### ❌ No pueden acceder:
- **Técnico**: No tiene acceso directo

---

## 🚀 Cómo Acceder

### Método 1: Desde el Dashboard
1. Inicia sesión en tu cuenta
2. Ve al **Dashboard** (desde el menú principal)
3. Busca la sección **"Módulos Especializados"**
4. Haz clic en el botón **"📊 Reportes y Estadísticas"**

### Método 2: Acceso Directo
- URL: `http://localhost:3000/estadisticas` (desarrollo)
- O tu dominio: `https://tudominio.com/estadisticas` (producción)

---

## 📊 Componentes de la Interfaz

### 1️⃣ Header
```
┌─────────────────────────────────────────┐
│ 📊 Reportes y Estadísticas              │
│    Análisis en tiempo real del sistema  │
└─────────────────────────────────────────┘
```
- Título descriptivo
- Subtítulo explicativo
- Icono visual

---

### 2️⃣ Tarjetas KPI (Tres Métricas)

#### 🌱 Total de Sembradores
```
┌──────────────────────────────┐
│ 🌱                            │
│ Total Sembradores             │
│ 42                            │
│ ↑ Activos                     │
└──────────────────────────────┘
```
**Qué significa**: Número total de sembradores registrados en el sistema (o territorio según tu rol)
**Usos**: Conocer tamaño de operación, detectar crecimiento

---

#### 📋 Seguimientos Realizados
```
┌──────────────────────────────┐
│ 📋                            │
│ Seguimientos Realizados       │
│ 127                           │
│ Registros                     │
└──────────────────────────────┘
```
**Qué significa**: Total de visitas de campo registradas
**Usos**: Medir cobertura de técnicos, actividad del campo

---

#### 📈 Promedio de Avance
```
┌──────────────────────────────┐
│ 📊                            │
│ Promedio de Avance           │
│ 72.5%                         │
│ [██████████░░░░░░]           │
└──────────────────────────────┘
```
**Qué significa**: Porcentaje promedio de avance de los cultivos
**Usos**: Evaluar salud de cosechas, detectar problemas

---

### 3️⃣ Gráfico de Distribución de Cultivos 🌾

```
Distribución de Cultivos
Cantidad de sembradores por tipo de cultivo

  25 ┤     ╭────╮
     │     │    │        ╭────╮
  20 ┤     │    │        │    │
     │     │    │   ╭────┤    │
  15 ┤     │    │   │    │    │
     │ ╭───┤    ├───┤    │    ├───╮
  10 ┤ │   │    │   │    │    │   │
     │ │   │    │   │    │    │   │
   5 ┤ │   │    │   │    │    │   │
     ├─┼───┼────┼───┼────┼────┼───┼─
     0 └───┴────┴───┴────┴────┴───┘
          Maíz Frijol Papa Tomate ...
```

**Características**:
- Barras de colores diferentes por cultivo
- Hover para ver valores exactos
- Eje Y: cantidad de sembradores
- Eje X: tipos de cultivos

**Usos**:
- Ver qué cultivos son más comunes
- Identificar oportunidades de mercado
- Planificar recursos por cultivo

---

### 4️⃣ Tabla Detallada de Cultivos

```
Detalle por Cultivo

┌──────────────────────────────────────────┐
│ Tipo de Cultivo │ Cantidad │ % │ Barra  │
├──────────────────────────────────────────┤
│ 🌾 Maíz        │    25    │38%│███████░│
│ 🌾 Frijol      │    18    │27%│█████░░░│
│ 🌾 Papa        │    15    │23%│████░░░░│
│ 🌾 Tomate      │     8    │12%│██░░░░░░│
└──────────────────────────────────────────┘
```

**Columnas**:
1. **Tipo de Cultivo**: Nombre del cultivo
2. **Cantidad**: Número de sembradores con ese cultivo
3. **Porcentaje**: % respecto al total
4. **Barra Visual**: Representación gráfica del porcentaje

**Usos**:
- Análisis detallado de cada cultivo
- Comparar proporciones
- Exportar datos (futuro)

---

### 5️⃣ Resumen General

```
Resumen General

┌────────────────────────────────────────────┐
│ 📊 Total de 42 sembradores registrados     │
│ 📋 Se han realizado 127 visitas de campo   │
│ 🌾 Hay 4 tipos de cultivos diferentes      │
│ 📈 Promedio de avance general es 72.5%    │
└────────────────────────────────────────────┘
```

**Información**:
- Resumen de métricas principales
- Contexto y conclusiones rápidas
- Recomendaciones (futuro)

---

## 🔄 Flujo de Datos

```
┌─────────────────┐
│  Backend        │
│  Endpoint:      │
│ /seguimientos   │
│  /stats         │
└────────┬────────┘
         │ (GET con JWT)
         │
    ┌────▼─────────────────┐
    │ Filtra por RBAC      │
    │ • Admin: Todo        │
    │ • Territorial: Zona  │
    │ • Facilitador: Técns │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Calcula Métricas:     │
    │ • Total Sembradores   │
    │ • Total Seguimientos  │
    │ • Promedio Avance     │
    │ • Cultivos Distrib.   │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Retorna JSON          │
    │ {                     │
    │  "total_sembradores": │
    │  "total_seguimientos":│
    │  "promedio_avance":   │
    │  "cultivos": {...}    │
    │ }                     │
    └────┬──────────────────┘
         │
┌────────▼─────────────────────┐
│   Frontend Vue Component      │
│   EstadisticasView.vue        │
│                              │
│  Renderiza:                  │
│  ✓ Tarjetas KPI             │
│  ✓ Gráfico Chart.js         │
│  ✓ Tabla HTML               │
│  ✓ Resumen                  │
└──────────────────────────────┘
```

---

## 💡 Consejos de Uso

### Para Administradores
1. **Usa esta vista para**: Monitoreo global del sistema
2. **Verifica**: Crecimiento de sembradores, cobertura de seguimientos
3. **Detecta**: Patrones de cultivos, zonas de bajo seguimiento

### Para Territoriales
1. **Monitorea**: Actividad en tu territorio
2. **Compara**: Desempeño de subordinados
3. **Identifica**: Fortalezas y debilidades por zona

### Para Facilitadores
1. **Supervisa**: Trabajo de tus técnicos
2. **Evalúa**: Cumplimiento de seguimientos
3. **Planifica**: Próximas intervenciones

---

## ⚙️ Personalización

### Futuros Filtros (En Desarrollo)
- [ ] Filtrar por rango de fechas
- [ ] Exportar datos a PDF/Excel
- [ ] Comparar períodos
- [ ] Filtrar por zona/técnico
- [ ] Alertas automáticas

### Gráficas Futuras
- [ ] Gráfico de pastel (cultivos)
- [ ] Gráfico de línea (evolución en tiempo)
- [ ] Gráfico de área (tendencias)
- [ ] Heatmap (actividad por zona)

---

## 🐛 Solución de Problemas

### "No veo datos"
**Posibles causas**:
1. No hay seguimientos registrados aún
2. Tu rol no tiene permisos (intenta con admin)
3. Sesión expirada

**Solución**:
1. Crea varios seguimientos primero
2. Verifica tu rol en Configuración
3. Cierra sesión y vuelve a iniciar

---

### "La gráfica no aparece"
**Posibles causas**:
1. JavaScript deshabilitado
2. Navegador antiguo (IE 11)
3. Error en conexión

**Solución**:
1. Habilita JavaScript
2. Usa Chrome, Firefox, Safari o Edge
3. Recarga la página (Ctrl+R)

---

### "Error 401 Unauthorized"
**Posible causa**:
- Tu token JWT expiró

**Solución**:
1. Cierra sesión
2. Vuelve a iniciar sesión
3. Reinicia la página

---

### "Datos incorrectos"
**Posible causa**:
- Datos en la base de datos están mal

**Solución**:
1. Verifica los datos en `/seguimiento` tab "Historial"
2. Contacta al administrador si hay inconsistencias

---

## 📱 Versión Móvil

La vista es totalmente responsive:

### En Móvil (< 480px)
- Las tarjetas se apilan verticalmente
- La tabla se comprime (scrolleable)
- El gráfico se reduce
- Todo es fácil de leer

### Tips para Mobile
- Usa orientación horizontal para mejor vista
- Desplázate horizontal en la tabla
- Toca los elementos para ver más info

---

## 🔐 Notas de Seguridad

1. **Tus datos están seguros**: Solo ves lo que tu rol permite
2. **JWT válida**: Tu sesión se valida en cada request
3. **Filtrado en backend**: No es posible por-saltear restricciones
4. **Token expira**: Tu sesión termina después de cierto tiempo

---

## 📧 Contacto y Soporte

Si tienes problemas o sugerencias:
1. Verifica la guía de pruebas: `TESTING_GUIDE_ESTADISTICAS.md`
2. Revisa el documento técnico: `ESTADISTICAS_MODULE_SUMMARY.md`
3. Contacta al equipo técnico con detalles del problema

---

## 📚 Recursos Adicionales

- **Documentación técnica**: `ESTADISTICAS_MODULE_SUMMARY.md`
- **Guía de pruebas**: `TESTING_GUIDE_ESTADISTICAS.md`
- **Archivo completado**: `ESTADISTICAS_COMPLETED.md`

---

**Versión**: 1.0.0
**Última actualización**: 2025
**Estado**: ✅ Producción
