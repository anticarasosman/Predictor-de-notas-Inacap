"""
Script de prueba para APIClient
Verifica que la conexión a API Gateway funciona correctamente
"""

import sys
sys.path.insert(0, '.')

from aws.api_client import APIClient, APIClientError

def main():
    print("=" * 60)
    print("TEST: API CLIENT")
    print("=" * 60)
    
    # Crear cliente
    api_url = "https://r9862991zc.execute-api.sa-east-1.amazonaws.com/prod/consultar"
    client = APIClient(api_url, timeout=30)
    
    # Test 1: Verificar conexión
    print("\n[TEST 1] Verificando conexión...")
    try:
        conectado = client.verificar_conexion()
        if conectado:
            print("✓ Conexión exitosa a API Gateway")
        else:
            print("✗ No se pudo conectar")
            return
    except APIClientError as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 2: Listar estudiantes (debería fallar por tabla no existe)
    print("\n[TEST 2] Intentando listar estudiantes...")
    try:
        estudiantes, metadatos = client.listar_estudiantes(limite=5)
        print(f"✓ Encontrados {len(estudiantes)} estudiantes")
        print(f"  Total en BD: {metadatos.get('total_resultados', 0)}")
    except APIClientError as e:
        print(f"✗ Error esperado (tabla no existe): {e}")
    
    # Test 3: Buscar estudiante específico
    print("\n[TEST 3] Buscando estudiante ficticio...")
    try:
        estudiante = client.buscar_estudiante("12345678-9")
        if estudiante:
            print(f"✓ Encontrado: {estudiante.get('nombre')}")
        else:
            print("✓ No encontrado (esperado)")
    except APIClientError as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
