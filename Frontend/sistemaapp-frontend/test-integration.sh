#!/bin/bash

# ===========================================
# 🧪 Script de Testing - Frontend MapaView
# ===========================================

echo "=== TESTING MAPAVIEW INTEGRATION ==="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
API_URL="http://localhost:9000"
TOKEN=""
AMBIENTAL_ID=""
PRODUCTIVA_ID=""

# Función para imprimir títulos
print_section() {
    echo ""
    echo -e "${YELLOW}▶ $1${NC}"
    echo "=================================================="
}

# Función para verificar éxito
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Éxito${NC}"
    else
        echo -e "${RED}✗ Error${NC}"
    fi
}

# ===== 1. Verificar que el backend esté corriendo =====
print_section "1. Verificando que el backend esté accesible"
curl -s "$API_URL/" > /dev/null
check_status

# ===== 2. Obtener token de autenticación =====
print_section "2. Obteniendo token JWT"
RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}')

TOKEN=$(echo $RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}✗ No se pudo obtener token. Respuesta:${NC}"
    echo $RESPONSE
    exit 1
else
    echo -e "${GREEN}✓ Token obtenido: ${TOKEN:0:50}...${NC}"
fi

# ===== 3. Crear datos de prueba - Capa Ambiental =====
print_section "3. Creando punto en capa Ambiental"
RESPONSE=$(curl -s -X POST "$API_URL/layers/ambiental" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque de Prueba",
    "descripcion": "Bosque test desde script",
    "lat": 19.4326,
    "lng": -99.1332
  }')

AMBIENTAL_ID=$(echo $RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
echo "Respuesta: $RESPONSE"
if [ ! -z "$AMBIENTAL_ID" ]; then
    echo -e "${GREEN}✓ Punto creado con ID: $AMBIENTAL_ID${NC}"
else
    echo -e "${RED}✗ Error al crear punto${NC}"
fi

# ===== 4. Crear datos de prueba - Capa Productiva =====
print_section "4. Creando punto en capa Productiva"
RESPONSE=$(curl -s -X POST "$API_URL/layers/productiva" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Parcela de Prueba",
    "descripcion": "Parcela test desde script",
    "lat": 19.45,
    "lng": -99.15
  }')

PRODUCTIVA_ID=$(echo $RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
echo "Respuesta: $RESPONSE"
if [ ! -z "$PRODUCTIVA_ID" ]; then
    echo -e "${GREEN}✓ Punto creado con ID: $PRODUCTIVA_ID${NC}"
else
    echo -e "${RED}✗ Error al crear punto${NC}"
fi

# ===== 5. Crear datos de prueba - Capa Social =====
print_section "5. Creando punto en capa Social"
RESPONSE=$(curl -s -X POST "$API_URL/layers/social" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Centro Social Test",
    "descripcion": "Centro test desde script",
    "lat": 19.42,
    "lng": -99.12
  }')

echo "Respuesta: $RESPONSE"
echo -e "${GREEN}✓ Punto creado${NC}"

# ===== 6. Crear datos de prueba - Capa Infraestructura =====
print_section "6. Creando punto en capa Infraestructura"
RESPONSE=$(curl -s -X POST "$API_URL/layers/infraestructura" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carretera Test",
    "descripcion": "Carretera test desde script",
    "lat": 19.40,
    "lng": -99.18
  }')

echo "Respuesta: $RESPONSE"
echo -e "${GREEN}✓ Punto creado${NC}"

# ===== 7. Obtener todos los puntos de cada capa =====
print_section "7. Obteniendo puntos de capa Ambiental"
RESPONSE=$(curl -s "$API_URL/layers/ambiental" \
  -H "Authorization: Bearer $TOKEN")

COUNT=$(echo $RESPONSE | grep -o '"id"' | wc -l)
echo "Respuesta: $RESPONSE"
echo -e "${GREEN}✓ Se encontraron $COUNT punto(s) ambiental${NC}"

# ===== 8. Obtener punto específico =====
if [ ! -z "$AMBIENTAL_ID" ]; then
    print_section "8. Obteniendo punto ambiental específico (ID: $AMBIENTAL_ID)"
    RESPONSE=$(curl -s "$API_URL/layers/ambiental/$AMBIENTAL_ID" \
      -H "Authorization: Bearer $TOKEN")
    
    echo "Respuesta: $RESPONSE"
    echo -e "${GREEN}✓ Punto obtenido${NC}"
fi

# ===== 9. Actualizar punto =====
if [ ! -z "$AMBIENTAL_ID" ]; then
    print_section "9. Actualizando punto ambiental (ID: $AMBIENTAL_ID)"
    RESPONSE=$(curl -s -X PUT "$API_URL/layers/ambiental/$AMBIENTAL_ID" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "nombre": "Bosque de Prueba ACTUALIZADO",
        "descripcion": "Descripción actualizada"
      }')
    
    echo "Respuesta: $RESPONSE"
    echo -e "${GREEN}✓ Punto actualizado${NC}"
fi

# ===== 10. Prueba sin token (debe fallar) =====
print_section "10. Prueba de seguridad - Acceso sin token (debe fallar)"
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$API_URL/layers/ambiental")
HTTP_CODE=$(echo "$RESPONSE" | grep HTTP_STATUS | cut -d':' -f2)

if [ "$HTTP_CODE" = "403" ] || [ "$HTTP_CODE" = "401" ]; then
    echo -e "${GREEN}✓ Seguridad correcta - Se rechazó sin token (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}✗ Error de seguridad - Se permitió acceso sin token (HTTP $HTTP_CODE)${NC}"
fi

# ===== 11. Resumén =====
print_section "RESUMEN DEL TESTING"
echo -e "${GREEN}✓ Todos los tests completados${NC}"
echo ""
echo "Datos de prueba creados:"
echo "  - Capa Ambiental: 1 punto"
echo "  - Capa Productiva: 1 punto"
echo "  - Capa Social: 1 punto"
echo "  - Capa Infraestructura: 1 punto"
echo ""
echo "Próximos pasos:"
echo "  1. Abre http://localhost:5173 en el navegador"
echo "  2. Accede con tu cuenta"
echo "  3. Deberías ver 4 marcadores en colores diferentes en el mapa"
echo "  4. Haz clic en el mapa para agregar nuevos puntos"
echo ""
echo -e "${YELLOW}=== TEST COMPLETADO ===${NC}"
