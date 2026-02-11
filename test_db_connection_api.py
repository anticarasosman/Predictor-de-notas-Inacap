"""
Test de DatabaseConnection con API Gateway
Valida que la nueva implementación funciona correctamente
"""

from database.db_connection import DatabaseConnection
from aws.api_client import APIClientError

def main():
    print("=" * 60)
    print("TEST: DatabaseConnection con API Gateway")
    print("=" * 60)
    
    # Test 1: Inicialización
    print("\n[TEST 1] Inicializando DatabaseConnection...")
    try:
        db = DatabaseConnection()
        print("✓ DatabaseConnection inicializado correctamente")
        print(f"  API URL: {db.api_url}")
        print(f"  Timeout: {db.timeout}s")
    except ValueError as e:
        print(f"✗ Error: {e}")
        return
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return
    
    # Test 2: Conectar
    print("\n[TEST 2] Conectando a API Gateway...")
    try:
        if db.connect():
            print("✓ Conexión exitosa")
        else:
            print("✗ Conexión fallida")
            return
    except APIClientError as e:
        print(f"✗ Error de API: {e}")
        return
    
    # Test 3: Verificar estado de conexión
    print("\n[TEST 3] Verificando estado de conexión...")
    if db.is_connected():
        print("✓ Estado: CONECTADO")
    else:
        print("✗ Estado: DESCONECTADO")
    
    # Test 4: Listar estudiantes (esperamos error de tabla no existe)
    print("\n[TEST 4] Intentando listar estudiantes...")
    try:
        estudiantes, metadatos = db.listar_estudiantes(pagina=1, limite=5)
        print(f"✓ Resultado: {len(estudiantes)} estudiantes")
        print(f"  Metadatos: {metadatos}")
        if estudiantes:
            print(f"  Primer estudiante: {estudiantes[0]}")
    except APIClientError as e:
        print(f"✗ Error esperado (tabla no existe): {e}")
    
    # Test 5: Buscar estudiante ficticio
    print("\n[TEST 5] Buscando estudiante ficticio (12345678-9)...")
    try:
        estudiante = db.buscar_estudiante("12345678-9")
        if estudiante:
            print(f"✓ Estudiante encontrado: {estudiante}")
        else:
            print("✓ Estudiante no encontrado (esperado)")
    except APIClientError as e:
        print(f"✗ Error esperado (tabla no existe): {e}")
    
    # Test 6: Probar métodos deprecados
    print("\n[TEST 6] Verificando que métodos deprecados lanzan NotImplementedError...")
    
    try:
        db.cursor()
        print("✗ cursor() no lanzó NotImplementedError")
    except NotImplementedError:
        print("✓ cursor() correctamente deprecado")
    
    try:
        db.execute_query("SELECT 1")
        print("✗ execute_query() no lanzó NotImplementedError")
    except NotImplementedError:
        print("✓ execute_query() correctamente deprecado")
    
    try:
        db.fetch_query("SELECT 1")
        print("✗ fetch_query() no lanzó NotImplementedError")
    except NotImplementedError:
        print("✓ fetch_query() correctamente deprecado")
    
    # Test 7: Desconectar
    print("\n[TEST 7] Desconectando...")
    if db.disconnect():
        print("✓ Desconexión exitosa")
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETADOS")
    print("=" * 60)

if __name__ == "__main__":
    main()
