"""
Script de prueba para verificar el sistema de encriptación
Valida que config_loader pueda desencriptar correctamente
"""
import config_loader
import os

print("=== Test de Sistema de Encriptación ===\n")

# Probar carga de config
print("1. Probando config_loader.load_config()...")
result = config_loader.load_config()

if result:
    print("   ✅ Archivo desencriptado correctamente\n")
    
    # Verificar variables de entorno
    print("2. Verificando variables de entorno cargadas...")
    
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    if db_host:
        print(f"   ✅ DB_HOST: {db_host}")
    else:
        print("   ❌ DB_HOST no cargada")
    
    if db_port:
        print(f"   ✅ DB_PORT: {db_port}")
    else:
        print("   ❌ DB_PORT no cargada")
    
    if db_name:
        print(f"   ✅ DB_NAME: {db_name}")
    else:
        print("   ❌ DB_NAME no cargada")
    
    if db_user:
        print(f"   ✅ DB_USER: {db_user}")
    else:
        print("   ❌ DB_USER no cargada")
    
    if db_password:
        print(f"   ✅ DB_PASSWORD: {'*' * len(db_password)} (oculta)")
    else:
        print("   ❌ DB_PASSWORD no cargada")
    
    print("\n✅ Sistema de encriptación funcionando correctamente")
else:
    print("   ❌ Error al desencriptar archivo")
