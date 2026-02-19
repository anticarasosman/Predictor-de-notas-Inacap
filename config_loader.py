"""
Módulo para cargar configuración desde .env.encrypted
Desencripta automáticamente sin intervención del usuario
"""
import os
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from io import StringIO

# Clave de encriptación hardcodeada (NO compartir en repositorios públicos)
ENCRYPTION_KEY = b'XHPMYwkt9o5KW88IS9IWhvatduAK7issto2Zw2UHiAo='

def load_config():
    """
    Carga las variables de entorno desde .env.encrypted
    Desencripta automáticamente usando la clave hardcodeada
    """
    # Determinar la ruta base (desarrollo o ejecutable)
    if getattr(sys, 'frozen', False):
        # Estamos en un ejecutable empaquetado
        application_path = os.path.dirname(sys.executable)
    else:
        # Estamos en desarrollo
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    encrypted_env_path = os.path.join(application_path, '.env.encrypted')
    
    print(f"[CONFIG] Buscando .env.encrypted en: {encrypted_env_path}")
    
    if not os.path.exists(encrypted_env_path):
        print("[CONFIG] ✗ ADVERTENCIA: Archivo .env.encrypted NO encontrado")
        return False
    
    try:
        # Leer archivo encriptado
        with open(encrypted_env_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Desencriptar
        cipher = Fernet(ENCRYPTION_KEY)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Cargar variables de entorno desde el contenido desencriptado
        env_content = decrypted_data.decode('utf-8')
        load_dotenv(stream=StringIO(env_content))
        
        print("[CONFIG] ✓ Archivo .env.encrypted desencriptado y cargado exitosamente")
        return True
        
    except Exception as e:
        print(f"[CONFIG] ✗ Error al desencriptar .env.encrypted: {e}")
        return False
