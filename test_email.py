#!/usr/bin/env python
"""
Script de prueba para verificar la configuración de email
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winespa.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Probar la configuración de email"""
    print("🔍 Verificando configuración de email...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {'Configurado' if settings.EMAIL_HOST_USER else 'NO CONFIGURADO'}")
    print(f"EMAIL_HOST_PASSWORD: {'Configurado' if settings.EMAIL_HOST_PASSWORD else 'NO CONFIGURADO'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()

def test_send_email():
    """Probar el envío de email"""
    print("📧 Probando envío de email...")
    
    try:
        resultado = send_mail(
            'Prueba de Email - WineSpa',
            'Este es un email de prueba para verificar la configuración.',
            settings.DEFAULT_FROM_EMAIL,
            ['test@example.com'],
            fail_silently=False,
        )
        
        print(f"✅ Email enviado exitosamente. Resultado: {resultado}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

if __name__ == '__main__':
    test_email_configuration()
    test_send_email()
