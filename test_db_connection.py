"""
Script de prueba para verificar conexión Docker + Python
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import DatabaseConnection

def test_connection():
    print("=" * 60)
    print("PRUEBA DE CONEXIÓN - Docker MySQL + Python")
    print("=" * 60)
    
    # Mostrar configuración
    print("\n📋 Configuración:")
    print(f"  Host: {os.getenv('DB_HOST')}")
    print(f"  Port: {os.getenv('DB_PORT')}")
    print(f"  User: {os.getenv('DB_USER')}")
    print(f"  Database: {os.getenv('DB_NAME')}")
    
    # Intentar conexión
    print("\n🔗 Intentando conexión...")
    db = DatabaseConnection()
    
    if db.connect():
        print("✓ Conexión exitosa!")
        
        # Prueba de query
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT DATABASE()")
            result = cursor.fetchone()
            print(f"\n✓ Base de datos actual: {result[0]}")
            
            # Contar tablas
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s
            """, (os.getenv('DB_NAME'),))
            table_count = cursor.fetchone()[0]
            print(f"✓ Tablas en la BD: {table_count}")
            
            cursor.close()
            
            print("\n" + "=" * 60)
            print("✅ TODA LAS PRUEBAS PASARON")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error en query: {e}")
    else:
        print("❌ Fallo en conexión")
        print("\n💡 Soluciones:")
        print("  1. Verifica que Docker Desktop está corriendo")
        print("  2. Ejecuta: docker-compose up -d")
        print("  3. Espera 30 segundos y reintenta")

if __name__ == "__main__":
    test_connection()
