#!/usr/bin/env python3
"""
Script de prueba del endpoint /auth/register
Uso: python test_register.py
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_register():
    """Probar registro de nuevo usuario"""
    print("=" * 60)
    print("TEST: /auth/register")
    print("=" * 60)
    
    # 1. Caso exitoso
    print("\n✅ Test 1: Registro exitoso")
    data = {
        "nombre": "Juan Técnico",
        "email": f"juan.tecnico@ejemplo.com",
        "password": "password123",
        "rol": "tecnico"
    }
    
    response = requests.post(f"{API_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 2. Error: Email duplicado
    print("\n❌ Test 2: Email duplicado")
    response = requests.post(f"{API_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 3. Error: Contraseña muy corta
    print("\n❌ Test 3: Contraseña muy corta")
    data_short_pwd = {
        "nombre": "Test User",
        "email": "test2@ejemplo.com",
        "password": "123",  # < 6
        "rol": "tecnico"
    }
    response = requests.post(f"{API_URL}/auth/register", json=data_short_pwd)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 4. Error: Nombre muy corto
    print("\n❌ Test 4: Nombre muy corto")
    data_short_name = {
        "nombre": "A",
        "email": "test3@ejemplo.com",
        "password": "password123",
        "rol": "tecnico"
    }
    response = requests.post(f"{API_URL}/auth/register", json=data_short_name)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 5. Error: Rol inválido
    print("\n❌ Test 5: Rol inválido")
    data_invalid_rol = {
        "nombre": "Test User",
        "email": "test4@ejemplo.com",
        "password": "password123",
        "rol": "superadmin"
    }
    response = requests.post(f"{API_URL}/auth/register", json=data_invalid_rol)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 6. Test: Facilitador
    print("\n✅ Test 6: Registro como facilitador")
    data_fac = {
        "nombre": "María Facilitadora",
        "email": "maria.fac@ejemplo.com",
        "password": "password123",
        "rol": "facilitador"
    }
    response = requests.post(f"{API_URL}/auth/register", json=data_fac)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_register()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar a http://localhost:8000")
        print("Asegúrate de que FastAPI está corriendo:")
        print("  cd BackendFastAPI")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
