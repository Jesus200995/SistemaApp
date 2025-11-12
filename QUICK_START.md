# ⚡ Quick Start - Comienza en 5 minutos

## 🎯 Objetivo
Iniciar MapaView con datos reales del backend en 5 minutos.

---

## Paso 1️⃣: Terminal 1 - Inicia Backend (2 min)

```bash
cd BackendFastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 9000
```

✅ Espera a ver:
```
Uvicorn running on http://0.0.0.0:9000
```

---

## Paso 2️⃣: Terminal 2 - Crea datos de prueba (2 min)

```bash
cd Frontend/sistemaapp-frontend

# En bash:
TOKEN=$(curl -s -X POST "http://localhost:9000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Crea punto ambiental
curl -X POST "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Bosque del Ajusco","lat":19.43,"lng":-99.13}'

# Crea punto productivo
curl -X POST "http://localhost:9000/layers/productiva" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Parcela de maíz","lat":19.45,"lng":-99.15}'

# Crea punto social
curl -X POST "http://localhost:9000/layers/social" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Centro comunitario","lat":19.42,"lng":-99.12}'

# Crea punto de infraestructura
curl -X POST "http://localhost:9000/layers/infraestructura" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Carretera principal","lat":19.40,"lng":-99.18}'
```

✅ Espera respuestas tipo:
```json
{"success":true,"id":1}
```

---

## Paso 3️⃣: Terminal 3 - Inicia Frontend (1 min)

```bash
cd Frontend/sistemaapp-frontend
npm run dev
```

✅ Espera a ver:
```
  VITE v5.x.x ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## 🌐 Paso 4: Abre navegador

```
http://localhost:5173
```

✅ Deberías ver:
- Login página (si no estás logueado)
- Introduce tus credenciales
- Dashboard

---

## 🗺️ Paso 5: Navega a MapaView

- Haz clic en "Capas Temáticas" (o la ruta correspondiente)

✅ Deberías ver:
- 4 marcadores en colores diferentes:
  - 🟢 Verde (Bosque del Ajusco)
  - 🟠 Naranja (Parcela de maíz)
  - 🔵 Azul (Centro comunitario)
  - ⚪ Gris (Carretera principal)

---

## 🖱️ Paso 6 (Opcional): Prueba crear punto

1. Haz clic en el mapa
2. Escribe: `ambiental`
3. Escribe: `Nuevo bosque de prueba`
4. ✅ Deberías ver: "✅ Punto agregado correctamente"
5. Nuevo punto aparece en el mapa

---

## 🎉 ¡Listo!

Ya tienes MapaView funcionando con datos reales del backend.

---

## 📌 Notas importantes

### CORS
Si ves error CORS, verifica que BackendFastAPI/main.py tenga:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Variables de entorno
Verifica que `.env` tenga:
```env
# Frontend
VITE_API_URL=http://localhost:9000

# Backend
DATABASE_URL=postgresql://...
SECRET_KEY=...
```

### Base de datos
Las tablas se crean automáticamente con SQLAlchemy.

---

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| "Connection refused" | Backend no está corriendo - Inicia con `uvicorn` |
| "No markers appear" | No hay datos - Ejecuta curl commands en Paso 2 |
| "401 Unauthorized" | Token inválido - Vuelve a hacer login |
| "CORS error" | Verifica CORS en main.py |
| "ModuleNotFoundError" | Instala dependencias: `pip install -r requirements.txt` |

---

## 📚 Documentación completa

Si necesitas más info, lee:
- **INTEGRATION_GUIDE.md** - Guía completa
- **INTERACTIVE_FLOW.md** - Diagramas de flujo
- **BackendFastAPI/LAYERS_API_DOCS.md** - API reference

---

## 🚀 Próximos pasos

Una vez que funcione:

1. **Prueba editando puntos** (próxima feature)
2. **Prueba eliminando puntos** (próxima feature)
3. **Agrega búsqueda** (próxima feature)
4. **Despliega a producción** (actualiza URLs)

---

## 💬 Preguntas?

Revisa el archivo correspondiente:
- ❓ "¿Cómo funciona?" → INTERACTIVE_FLOW.md
- ❓ "¿Qué cambios se hicieron?" → IMPLEMENTATION_SUMMARY.md
- ❓ "¿Cómo testear?" → BackendFastAPI/TESTING_GUIDE.md
- ❓ "¿Qué es cada endpoint?" → BackendFastAPI/LAYERS_API_DOCS.md

---

## ✅ Checklist

- [ ] Backend corriendo en puerto 9000
- [ ] Datos de prueba creados con curl
- [ ] Frontend corriendo en puerto 5173
- [ ] Abiste navegador en http://localhost:5173
- [ ] Iniciaste sesión
- [ ] Navegaste a MapaView
- [ ] Ves 4 marcadores en el mapa
- [ ] Intentaste crear un nuevo punto
- [ ] Punto nuevo aparece en el mapa

**Si todos están marcados ✅ = ¡Éxito! 🎉**

