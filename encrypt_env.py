"""
Script para encriptar el archivo .env
Ejecutar una sola vez para generar .env.encrypted
"""
import os
from cryptography.fernet import Fernet

# La misma clave hardcodeada que en config_loader.py
ENCRYPTION_KEY = b'XHPMYwkt9o5KW88IS9IWhvatduAK7issto2Zw2UHiAo='

def encrypt_env_file():
    """
    Encripta el archivo .env y genera .env.encrypted
    """
    env_path = '.env'
    encrypted_path = '.env.encrypted'
    
    if not os.path.exists(env_path):
        print(f"❌ Error: No se encontró el archivo {env_path}")
        return False
    
    try:
        # Leer el archivo .env
        with open(env_path, 'rb') as f:
            env_data = f.read()
        
        # Encriptar usando Fernet
        cipher = Fernet(ENCRYPTION_KEY)
        encrypted_data = cipher.encrypt(env_data)
        
        # Guardar el archivo encriptado
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        file_size = len(encrypted_data)
        print(f"✅ Archivo encriptado exitosamente")
        print(f"📁 Archivo generado: {encrypted_path}")
        print(f"📊 Tamaño: {file_size} bytes")
        print(f"\n⚠️  IMPORTANTE:")
        print(f"   1. Incluye '{encrypted_path}' en tu distribución")
        print(f"   2. NO incluyas el archivo '.env' original")
        print(f"   3. La aplicación desencriptará automáticamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al encriptar: {e}")
        return False

if __name__ == "__main__":
    print("=== Encriptador de archivo .env ===\n")
    encrypt_env_file()
