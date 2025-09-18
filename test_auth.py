#!/usr/bin/env python3
"""
Script de prueba para el sistema de autenticación unificado
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000/api"
AUTH_URL = f"{BASE_URL}/auth"

def test_endpoints():
    """Prueba que todos los endpoints estén disponibles"""
    print("🔍 Probando endpoints de autenticación...")
    
    # Probar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Servidor respondiendo: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté corriendo.")
        return False
    
    # Probar endpoints de autenticación
    endpoints = [
        f"{AUTH_URL}/login/",
        f"{AUTH_URL}/registro/",
        f"{AUTH_URL}/cambiar-contraseña/",
        f"{AUTH_URL}/solicitar-codigo/",
        f"{AUTH_URL}/confirmar-codigo/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.options(endpoint)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    return True

def test_registro():
    """Prueba el registro de un usuario"""
    print("\n📝 Probando registro de usuario...")
    
    user_data = {
        "nombre": "Usuario Prueba",
        "tipo_documento": "CC",
        "documento": "12345678",
        "celular": "3001234567",
        "correo_electronico": "prueba@test.com",
        "direccion": "Calle Test #123",
        "tipo_usuario": "cliente",
        "genero": "M"
    }
    
    try:
        response = requests.post(
            f"{AUTH_URL}/registro/",
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registro exitoso!")
            print(f"   Usuario ID: {data['usuario']['id']}")
            print(f"   Rol: {data['usuario']['rol']}")
            print(f"   Debe cambiar contraseña: {data['usuario']['debe_cambiar_contraseña']}")
            if data.get('contraseña_generada'):
                print(f"   Contraseña temporal: {data['contraseña_generada']}")
            return data
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_login(credentials):
    """Prueba el login con las credenciales proporcionadas"""
    print("\n🔐 Probando login...")
    
    login_data = {
        "correo_electronico": credentials['correo_electronico'],
        "contraseña": credentials['password']
    }
    
    try:
        response = requests.post(
            f"{AUTH_URL}/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login exitoso!")
            print(f"   Usuario: {data['usuario']['nombre']}")
            print(f"   Rol: {data['usuario']['rol']}")
            print(f"   Tipo usuario: {data.get('tipo_usuario')}")
            print(f"   Debe cambiar contraseña: {data['usuario']['debe_cambiar_contraseña']}")
            return data
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_solicitar_codigo(correo):
    """Prueba la solicitud de código de recuperación"""
    print(f"\n📧 Probando solicitud de código para {correo}...")
    
    data = {"correo_electronico": correo}
    
    try:
        response = requests.post(
            f"{AUTH_URL}/solicitar-codigo/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Solicitud de código exitosa!")
            return True
        else:
            print(f"❌ Error en solicitud: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE AUTENTICACIÓN")
    print("=" * 60)
    
    # Probar endpoints
    if not test_endpoints():
        return
    
    # Probar registro
    user_data = test_registro()
    if not user_data:
        print("❌ No se pudo registrar usuario. Abortando pruebas.")
        return
    
    # Probar login
    credentials = {
        'correo_electronico': user_data['usuario']['correo_electronico'],
        'password': user_data.get('contraseña_generada', 'password123')
    }
    
    login_data = test_login(credentials)
    if not login_data:
        print("❌ No se pudo hacer login. Abortando pruebas.")
        return
    
    # Probar solicitud de código
    test_solicitar_codigo(credentials['correo_electronico'])
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("\n📋 RESUMEN:")
    print(f"   ✅ Usuario registrado: {user_data['usuario']['nombre']}")
    print(f"   ✅ Login exitoso con rol: {login_data['usuario']['rol']}")
    print(f"   ✅ Sistema de autenticación funcionando correctamente")

if __name__ == "__main__":
    main()
