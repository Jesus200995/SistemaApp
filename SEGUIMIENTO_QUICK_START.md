# ⚡ Quick Start - Módulo Seguimiento de Campo

## 🏃 5 Minutos para Empezar

### Paso 1: Iniciar Backend (2 min)

```powershell
# Terminal 1
cd Backend
python -m uvicorn main:app --reload --port 8000

# Esperado:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Paso 2: Iniciar Frontend (2 min)

```powershell
# Terminal 2
cd Frontend/sistemaapp-frontend
npm run dev

# Esperado:
# VITE v4.x.x ready in xxx ms
# ➜  Local:   http://localhost:5173
```

### Paso 3: Acceder a la Aplicación (1 min)

1. Abre navegador: `http://localhost:5173`
2. Login con credenciales de técnico
3. Busca "📊 Seguimiento" en la navbar
4. ¡Listo! 🎉

---

## 📝 Quick Reference

### URLs Principales
```
Frontend:  http://localhost:5173
Backend:   http://localhost:8000
Docs API:  http://localhost:8000/docs
DB:        PostgreSQL (localhost)
```

### Tabs Disponibles

| Tab | Para Quién | Qué Hace |
|-----|-----------|---------|
| 📝 Crear | Todos | Registrar nueva visita |
| 📊 Mis | Todos | Ver mis visitadas |
| 📈 Reportes | Supervisores | Analytics |

### Estados del Cultivo
```
🌱 Germinando      → Semillas brotando
🌿 Vegetativo      → Crecimiento de hojas
🌻 Floración       → Producción de flores
🍅 Fructificación  → Desarrollo de frutos
✂️ Cosecha         → Recolección
🐛 Plagas          → Problema encontrado
😷 Enfermedad      → Problema encontrado
```

---

## 🔍 Troubleshooting Rápido

### Backend no inicia
```powershell
# Verificar Python
python --version

# Reinstalar dependencias
pip install -r requirements.txt

# Verifica que PostgreSQL esté corriendo
```

### Frontend no inicia
```powershell
# Limpiar cache
rm -r node_modules
npm install

# Reiniciar
npm run dev
```

### No veo el enlace "Seguimiento"
```
1. Verifica que estés logueado
2. Recarga la página (F5)
3. Limpia cache (Ctrl+Shift+R)
```

### Error 404 al crear seguimiento
```
1. Verifica que el sembrador exista
2. Recarga la lista de sembradores
3. Crea un nuevo sembrador si es necesario
```

---

## 💾 Comandos Útiles

### Base de Datos
```sql
-- Verificar tabla existe
SELECT * FROM seguimientos LIMIT 1;

-- Contar registros
SELECT COUNT(*) FROM seguimientos;

-- Ver estructura
\d seguimientos

-- Limpiar (CUIDADO!)
DELETE FROM seguimientos;
```

### API Testing
```bash
# Get token
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}'

# Crear seguimiento
curl -X POST http://localhost:8000/seguimientos/crear \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sembrador_id":1,"fecha_visita":"2024-11-18T14:30:00","estado_cultivo":"Germinando","observaciones":"Test","avance_porcentaje":25}'

# Listar
curl -X GET http://localhost:8000/seguimientos/ \
  -H "Authorization: Bearer TOKEN"

# Reportes
curl -X GET http://localhost:8000/seguimientos/reportes/por-tecnico \
  -H "Authorization: Bearer TOKEN"
```

---

## 📊 Roles y Acceso

### Técnico
- ✅ Crear seguimientos
- ✅ Ver propios
- ✅ Ver reportes propios
- ❌ Ver otros técnicos

### Facilitador
- ✅ Ver técnicos
- ✅ Ver reportes de zona
- ✅ Crear propios

### Territorial
- ✅ Ver facilitadores
- ✅ Ver reportes territorio
- ✅ Crear propios

### Admin
- ✅ Ver todo
- ✅ Crear/editar/eliminar
- ✅ Reportes completos

---

## 🎯 Casos de Uso Comunes

### Registrar Visita
```
1. Click "📊 Seguimiento"
2. Selecciona sembrador
3. Elige estado cultivo
4. Pon progreso (slider)
5. Escribe observaciones
6. Click "✅ Guardar"
```

### Ver Progreso
```
1. Tab "Mis Seguimientos"
2. Ver tarjetas con barras
3. Click 🗑️ para eliminar
```

### Analizar Datos
```
1. Tab "Reportes"
2. Ver tabla por técnico
3. Ver tabla por cultivo
4. Comparar avances
```

---

## 📱 Responsive Design

### Desktop (1920x1080)
- Full 3-column grid
- Sidebar visible
- Tablas completas

### Tablet (768x1024)
- 2-column grid
- Menú colapsable
- Tablas comprimidas

### Mobile (375x667)
- 1-column stack
- Menú hamburguesa
- Tablas scrolleables

---

## 🔐 Credenciales Test (Ejemplo)

```
TÉCNICO:
  Email: tecnico@example.com
  Pass:  password123
  Rol:   tecnico_productivo

FACILITADOR:
  Email: facilitador@example.com
  Pass:  password123
  Rol:   facilitador

TERRITORIAL:
  Email: territorial@example.com
  Pass:  password123
  Rol:   territorial

ADMIN:
  Email: admin@example.com
  Pass:  password123
  Rol:   admin
```

---

## 🐛 Debug Mode

### Frontend Console
```javascript
// Ver estado actual
console.log(auth.user)

// Ver último error
console.log(localStorage.getItem('lastError'))

// Ver storage
localStorage
```

### Browser DevTools
- F12: Abrir DevTools
- Network: Ver API calls
- Application: Ver localStorage
- Console: Ver errores

### Backend Logs
```
# Terminal con uvicorn muestra:
INFO:     POST /seguimientos/crear
INFO:     Response status code: 200
```

---

## 💡 Tips & Tricks

### Copiar URLs de fotos
```
1. Usa https://imgur.com para subir gratis
2. Copia el enlace directo (termina en .jpg)
3. Pega en "URL de Foto"
```

### Editar sin eliminar
```
Funcionalidad en desarrollo
Por ahora: Elimina y crea nuevo
```

### Backup de datos
```bash
# Exportar datos
pg_dump sistemaapp > backup.sql

# Importar
psql sistemaapp < backup.sql
```

---

## 📞 Próximos Pasos

✅ **Completado**: Implementación básica  
🔄 **Haciendo**: Testing en staging  
⏳ **Próximo**: Deploy a producción  

```
Semana 1: Testing y fixes
Semana 2: Edición completa
Semana 3: Upload de fotos
Semana 4: Reportes avanzados
```

---

## 📚 Documentación Completa

Para más detalles, ver:
- `SEGUIMIENTO_SETUP.md` - Guía completa
- `SEGUIMIENTO_TESTING.md` - Testing exhaustivo
- `SEGUIMIENTO_IMPLEMENTATION.md` - Detalles técnicos

---

## 🆘 Si Algo No Funciona

1. **Recarga página**: F5
2. **Limpia cache**: Ctrl+Shift+R
3. **Abre DevTools**: F12 → Console
4. **Lee el error**: Red flag de error
5. **Revisa logs**: Backend terminal
6. **Reinicia todo**:
   ```
   Ctrl+C Backend
   Ctrl+C Frontend
   npm run dev
   python -m uvicorn main:app --reload
   ```

---

## ✨ Características Clave

- 🌱 Registro de visitas de campo
- 📊 Reportes por técnico
- 🌾 Reportes por cultivo
- 📈 Gráficos de progreso
- 🔐 Control de acceso jerárquico
- 📸 Soporte para fotos
- 🎨 Dark theme profesional
- 📱 Diseño responsive

---

**Versión**: 1.0.0  
**Última Actualización**: 18 Noviembre 2024  
**Status**: ✅ Listo para Usar  

¡Que disfrutes usando el módulo! 🎉
