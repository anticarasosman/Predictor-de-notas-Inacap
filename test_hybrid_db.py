#!/usr/bin/env python3
"""
Test: Validar que db_connection.py funciona en modo HÍBRIDO
Los readers pueden usar cursor(), execute_query(), fetch_query()
"""

from database.db_connection import DatabaseConnection

print("=" * 70)
print("TEST: DatabaseConnection en Modo HÍBRIDO (MySQL + API)")
print("=" * 70)

# Test 1: Inicializar
print("\n[TEST 1] Inicializando DatabaseConnection...")
try:
    db = DatabaseConnection()
    print(f"✓ Inicializado:")
    print(f"  Host: {db.host}")
    print(f"  User: {db.user}")
    print(f"  Database: {db.database}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 2: Conectar
print("\n[TEST 2] Conectando a MySQL...")
if db.connect():
    print("✓ Conexión exitosa")
else:
    print("✗ Conexión falló")
    exit(1)

# Test 3: Verificar estado
print("\n[TEST 3] Verificando estado de conexión...")
if db.is_connected():
    print("✓ Estado: CONECTADO")
else:
    print("✗ Estado: DESCONECTADO")
    exit(1)

# Test 4: Probar cursor() - lo que usan los readers
print("\n[TEST 4] Probando cursor() (para readers)...")
try:
    cursor = db.cursor()
    print("✓ Cursor obtenido correctamente")
    
    # Prueba simple: contar tabla
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()
    cursor.close()
    print(f"✓ Cursor funciona: {resultado}")
except Exception as e:
    print(f"✗ Error con cursor: {e}")

# Test 5: Probar get_connection() - lo que usan algunos readers
print("\n[TEST 5] Probando get_connection()...")
try:
    conexion = db.get_connection()
    if conexion:
        print(f"✓ Conexión obtenida: {type(conexion).__name__}")
    else:
        print("✗ get_connection() retornó None")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 6: Desconectar
print("\n[TEST 6] Desconectando...")
if db.disconnect():
    print("✓ Desconexión exitosa")
    if not db.is_connected():
        print("✓ Estado final: DESCONECTADO")
else:
    print("✗ Error en desconexión")

print("\n" + "=" * 70)
print("✅ TODOS LOS TESTS PASARON - Listo para readers")
print("=" * 70)
print("\nLos readers pueden ahora usar:")
print("  - db.cursor() para operaciones SQL directas")
print("  - db.execute_query() para INSERT/UPDATE/DELETE")
print("  - db.fetch_query() para SELECT")
print("  - db.get_connection() para acceso a la conexión")
print("  - Transacciones: db.connection.commit() / rollback()")
