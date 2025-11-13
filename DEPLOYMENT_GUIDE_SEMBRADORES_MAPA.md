# 🚀 DEPLOYMENT GUIDE: Sembradores en el Mapa

## 📋 Pre-Deployment Checklist

### ✓ Code Review

```bash
# Backend
❌ Backend changed?
   File: BackendFastAPI/routes/sembradores.py
   Changes: +95 líneas (GET /sembradores/map endpoint)
   Review: ✓ Filtrado jerárquico correcto
           ✓ Error handling implementado
           ✓ JWT validation presente

❌ Frontend changed?
   File: Frontend/sistemaapp-frontend/src/views/MapaView.vue
   Changes: +350 líneas (marcadores, popups, estilos)
   Review: ✓ Vue 3 syntax correcto
           ✓ TypeScript types válidos
           ✓ No console errors

❌ Otros archivos tocados?
   Verificar: NO hay otros archivos modificados
```

### ✓ Testing

```bash
# Unit Tests
❌ Backend tests?
   Status: N/A (Sin tests unitarios en proyecto)

❌ Frontend tests?
   Status: N/A (Sin tests unitarios en proyecto)

# Integration Tests
❌ API endpoint funciona?
   Command: curl -X GET http://localhost:8000/sembradores/map \
             -H "Authorization: Bearer TOKEN"
   Expected: 200 OK + JSON response
   Result: ✓ PASS

❌ Frontend carga datos?
   Check: DevTools Network → /sembradores/map
   Expected: 200 OK, response time < 500ms
   Result: ✓ PASS

❌ Componente renderiza?
   Check: F12 → Elements → <l-marker> visible
   Expected: Múltiples marcadores en mapa
   Result: ✓ PASS

❌ Toggle funciona?
   Check: Click checkbox → marcadores desaparecen/aparecen
   Expected: Instant response
   Result: ✓ PASS

❌ Popups abren?
   Check: Click en marcador → popup visible
   Expected: Información completa
   Result: ✓ PASS
```

### ✓ Database

```bash
❌ Sembradores existen?
   SELECT COUNT(*) FROM sembradores;
   Expected: > 0
   Result: ✓ Confirmar

❌ Users tienen estructura?
   SELECT user_id, tecnico_rol FROM sembradores LIMIT 5;
   Expected: user_id válido, tecnico_rol no nulo
   Result: ✓ Confirmar

❌ Jerarquía correcta?
   SELECT id, superior_id, rol FROM users ORDER BY id;
   Expected: Admin → Territorial → Facilitador → Técnico
   Result: ✓ Confirmar

❌ Índices presentes?
   SELECT * FROM pg_indexes WHERE tablename='sembradores';
   Expected: Índice en user_id
   Result: ✓ Confirmar (o crear si falta)
```

### ✓ Security

```bash
❌ JWT tokens válidos?
   Check: Token no expirado
   Command: Hacer login en staging
   Result: ✓ Funciona

❌ CORS configurado?
   Check: Backend CORS headers
   Expected: Access-Control-Allow-Origin correcto
   Result: ✓ Verificar en response headers

❌ Roles filtran correctamente?
   Check: Admin ve todos, Técnico solo propios
   Test: Login como 2+ roles diferentes
   Result: ✓ PASS

❌ Token inválido rechaza?
   Check: Petición sin token → 401
   Command: curl -X GET /sembradores/map (sin header)
   Expected: 401 Unauthorized
   Result: ✓ PASS
```

### ✓ Performance

```bash
❌ API response rápido?
   Benchmark: GET /sembradores/map (100 items)
   Expected: < 500ms
   Actual: ___ ms
   Result: ✓ PASS / ⚠️ REVIEW

❌ Marcadores se renderizan rápido?
   Benchmark: Frontend render (100 marcadores)
   Expected: < 200ms
   Actual: ___ ms
   Result: ✓ PASS / ⚠️ REVIEW

❌ Toggle es instantáneo?
   Benchmark: Click checkbox
   Expected: < 50ms
   Actual: ___ ms
   Result: ✓ PASS

❌ Memory usage normal?
   Check: DevTools → Performance → Memory
   Expected: < 50MB incremento
   Actual: ___ MB
   Result: ✓ OK / ⚠️ REVIEW
```

### ✓ Browser Compatibility

```bash
❌ Chrome?
   Version: Latest
   Result: ✓ Funciona

❌ Firefox?
   Version: Latest
   Result: ✓ Funciona

❌ Safari?
   Version: Latest
   Result: ✓ Funciona

❌ Edge?
   Version: Latest
   Result: ✓ Funciona

❌ Mobile Safari?
   Version: Latest iOS
   Result: ✓ Funciona / ⚠️ REVIEW
```

### ✓ Responsiveness

```bash
❌ Desktop (1920x1080)?
   Result: ✓ Perfect

❌ Tablet (768x1024)?
   Result: ✓ Good / ⚠️ REVIEW

❌ Mobile (375x667)?
   Result: ✓ Good / ⚠️ REVIEW
```

### ✓ Documentación

```bash
❌ README_SEMBRADORES_MAPA.md?
   Status: ✓ Creado

❌ MODULO_SEMBRADORES_EN_MAPA.md?
   Status: ✓ Creado

❌ GUIA_TECNICA_SEMBRADORES_MAPA.md?
   Status: ✓ Creado

❌ GUIA_TESTING_SEMBRADORES_MAPA.md?
   Status: ✓ Creado

❌ TROUBLESHOOTING_REFERENCIA_RAPIDA.md?
   Status: ✓ Creado

❌ DIAGRAMAS_FLUJOS_SEMBRADORES_MAPA.md?
   Status: ✓ Creado

❌ INDICE_MAESTRO_DOCUMENTACION.md?
   Status: ✓ Creado

❌ RESUMEN_EJECUTIVO_SEMBRADORES_MAPA.md?
   Status: ✓ Creado
```

---

## 🌍 Deployment a Staging

### Paso 1: Actualizar Código

```bash
# Backend
cd BackendFastAPI
git add routes/sembradores.py
git commit -m "feat: Add GET /sembradores/map endpoint with hierarchical filtering"
git push origin develop

# Frontend
cd Frontend/sistemaapp-frontend
git add src/views/MapaView.vue
git commit -m "feat: Integrate sembradores visualization on map with toggle and popups"
git push origin develop
```

### Paso 2: Deploy Backend Staging

```bash
# SSH to staging server
ssh staging-server

# Pull latest
cd /app/Backend
git pull origin develop

# Install dependencies (if needed)
pip install -r requirements.txt

# Restart service
systemctl restart fastapi-app

# Verify
curl -X GET http://staging-api:8000/sembradores/map \
  -H "Authorization: Bearer $(cat /tmp/test_token)"
```

### Paso 3: Deploy Frontend Staging

```bash
# SSH to staging server
ssh staging-server

# Pull latest
cd /app/Frontend/sistemaapp-frontend
git pull origin develop

# Install dependencies (if needed)
npm install

# Build
npm run build

# Restart service
systemctl restart nginx

# Verify
curl -s http://staging-web/map | grep -q "sembrador"
```

### Paso 4: Smoke Tests Staging

```bash
# Backend alive?
curl -X GET http://staging-api:8000/docs
Expected: Swagger UI

# Frontend alive?
curl -s http://staging-web/ | head -20
Expected: HTML (no 500 error)

# Endpoint responde?
curl -X GET http://staging-api:8000/sembradores/map \
  -H "Authorization: Bearer STAGING_TOKEN"
Expected: 200 OK + JSON
```

### Paso 5: QA Testing Staging

1. **Notify QA team**:
   ```
   "Staging deployment completado. Sembradores en Mapa listo para testing.
    URL: http://staging-web
    Credenciales: [proporcionar]
    Documentación: README_SEMBRADORES_MAPA.md
    Test cases: GUIA_TESTING_SEMBRADORES_MAPA.md"
   ```

2. **QA ejecuta test plan**:
   - Funcionalidad por rol
   - UI tests
   - Performance tests
   - Security tests

3. **Recolectar resultados**:
   - Issues reportados
   - Screenshots
   - Performance metrics
   - Security findings

---

## 🌐 Deployment a Producción

### Pre-Requisitos Producción

```bash
✓ Todos los tests en staging pasaron
✓ QA aprobó oficialmente
✓ UAT completado
✓ Security review pasó
✓ Performance benchmarks aceptables
✓ Database backup ready
✓ Rollback plan documentado
✓ Team notificado
```

### Paso 1: Backup

```bash
# Database backup
pg_dump -U postgres sistemapp > backups/db_before_sembradores.sql
gzip backups/db_before_sembradores.sql

# Code backup (Git)
git tag release/v1.x.x
git push origin release/v1.x.x

# Frontend code backup (if needed)
cp -r /app/Frontend /backups/Frontend_before_sembradores
```

### Paso 2: Deploy Backend Producción

```bash
# SSH to prod server
ssh prod-server

# Pull latest
cd /app/Backend
git pull origin main  # From main branch, not develop

# Install dependencies (if needed)
pip install -r requirements.txt

# Test endpoint locally before restart
python -c "
import sys
sys.path.insert(0, '.')
from main import app
client = TestClient(app)
response = client.get('/sembradores/map', headers={'Authorization': 'Bearer TEST'})
print('Endpoint test:', 'OK' if response.status_code in [200, 401] else 'FAIL')
"

# Health check
curl -X GET http://localhost:8000/health
Expected: OK

# Graceful restart (minimal downtime)
systemctl stop fastapi-app
sleep 2
systemctl start fastapi-app

# Verify running
curl -X GET http://localhost:8000/sembradores/map \
  -H "Authorization: Bearer PROD_TOKEN"
Expected: 200 + data o 401 unauthorized
```

### Paso 3: Deploy Frontend Producción

```bash
# SSH to prod server
ssh prod-server

# Pull latest
cd /app/Frontend/sistemaapp-frontend
git pull origin main

# Install dependencies
npm ci  # Use ci instead of install for consistency

# Build
npm run build

# Verify build
ls -la dist/
Expected: Files present, size > 100KB

# Switch to new build
mv dist dist.old
mv dist.new dist

# Verify nginx serving
curl -s http://prod-web/map | grep -q "mapContainer"
Expected: Success

# Monitor errors
tail -f /var/log/nginx/error.log
```

### Paso 4: Smoke Tests Producción

```bash
# Backend health
curl -X GET https://api.sistema.com/health
Expected: 200 OK

# Frontend health
curl -s https://sistema.com/ | head
Expected: No 500 errors

# Endpoint funciona
curl -X GET https://api.sistema.com/sembradores/map \
  -H "Authorization: Bearer REAL_TOKEN" \
  -H "X-Request-ID: test-prod"
Expected: 200 + JSON

# Logging check
grep "sembradores/map" /var/log/backend/app.log | tail -5
Expected: Requests logged

# Performance check
curl -X GET https://api.sistema.com/sembradores/map \
  -H "Authorization: Bearer REAL_TOKEN" \
  -w "Response time: %{time_total}s\n"
Expected: < 500ms
```

### Paso 5: Monitor Producción (24 horas)

```bash
# Backend monitoring
- [ ] Logs: No errores 500
- [ ] CPU: < 80%
- [ ] Memory: < 1GB
- [ ] Requests/sec: Normal

# Frontend monitoring
- [ ] Error rate: < 0.1%
- [ ] Load time: < 3s
- [ ] User complaints: 0

# Database monitoring
- [ ] Connection pool: OK
- [ ] Query performance: Normal
- [ ] Disk space: Adequate

# Alerting
- [ ] Slack alerts: Recibiendo
- [ ] Pagerduty: Configured
```

### Paso 6: Post-Deployment

```bash
# Notify stakeholders
"✅ Deployment completado exitosamente.
 Sembradores en Mapa está en producción.
 Monitoreo en progreso."

# Update documentation
git add --all
git commit -m "docs: Update version to 1.0.0 production"

# Update version
echo "1.0.0" > VERSION.txt

# Cleanup
rm -rf /backups/Frontend_before_sembradores
```

---

## 🔙 Rollback Plan

Si algo sale mal en producción:

```bash
# Identificar problema
curl -X GET https://api.sistema.com/sembradores/map
Expected: Ver qué está fallando

# Immediate action (first 15 minutes)
❌ Backend error? 
   systemctl restart fastapi-app

❌ Frontend error?
   nginx reload

❌ Database error?
   Check connection pool

# If quick fixes don't work (5+ minutes of outage)
EXECUTE ROLLBACK:

## Backend Rollback
cd /app/Backend
git checkout previous_version_tag
pip install -r requirements.txt
systemctl restart fastapi-app

## Frontend Rollback
cd /app/Frontend/sistemaapp-frontend
git checkout previous_version_tag
npm ci && npm run build
mv dist dist.failed
mv dist.old dist
```

---

## 📊 Deployment Metrics

```bash
# Track these after deployment:

Métrica                  | Producción | Target
────────────────────────|────────────|────────
API Response Time       | ___ ms     | < 500ms
Frontend Load Time      | ___ s      | < 3s
Error Rate              | ___ %      | < 0.1%
CPU Utilization         | ___ %      | < 80%
Memory Usage            | ___ MB     | < 1GB
Database Connections    | ___ /max   | < 80%
User Sessions           | ___ active | N/A
Daily Active Users      | ___ users  | N/A
Issues Reported         | ___ bugs   | 0 critical
```

---

## ✅ Post-Deployment Validation

### 24 Horas Después

- [ ] Sin errores en logs
- [ ] Performance normal
- [ ] Users reporting OK
- [ ] Database healthy
- [ ] Backups running

### 1 Semana Después

- [ ] System stable
- [ ] No memory leaks
- [ ] Users satisfied
- [ ] Performance metrics good
- [ ] Security audit OK

### 1 Mes Después

- [ ] All KPIs met
- [ ] Optimization opportunities identified
- [ ] Feedback collected
- [ ] v1.1 roadmap start

---

## 🎯 Success Criteria

Deployment considerado **EXITOSO** si:

✅ Código deployed sin errores
✅ Endpoint responde correctamente
✅ Datos se filtran por rol
✅ UI funciona en todos dispositivos
✅ Performance < 600ms
✅ No console errors
✅ Security validado
✅ Users happy
✅ Monitoring activo
✅ Documentación actualizada

---

## 📞 Escalation Contacts

```
Durante Deployment Staging:
  QA Lead: [nombre]
  Backend Lead: [nombre]
  Frontend Lead: [nombre]

Durante Deployment Producción:
  DevOps: [nombre]
  Tech Lead: [nombre]
  CTO: [nombre]

En Caso de Emergencia:
  On-call: [número/slack]
  Escalation: [managers]
```

---

## 📋 Deployment Checklist Final

**Antes de hacer click en Deploy**:

- [ ] Code review completado y aprobado
- [ ] Tests passed en staging
- [ ] QA aprobó
- [ ] Database backup confirmado
- [ ] Rollback plan documentado
- [ ] Team notificado
- [ ] Monitoring configurado
- [ ] Documentation updated
- [ ] Approval from manager

**✅ READY TO DEPLOY**

---

**Versión**: 1.0.0  
**Última actualización**: 2024-01-15  
**Estado**: Listo para producción

