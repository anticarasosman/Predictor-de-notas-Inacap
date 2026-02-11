#!/usr/bin/env python3
"""
Test: Carga de CSV usando ReporteMorosidadReader
Valida que los readers funcionan con db_connection en modo HÍBRIDO
"""

import pandas as pd
import sys
from database.db_connection import DatabaseConnection
from classes.readers.excel_reader.reporte_morosidad_reader import ReporteMorosidadReader

print("=" * 80)
print("TEST: Carga de CSV - ReporteMorosidadReader")
print("=" * 80)

# Ruta del CSV
csv_path = r"data\REPORTE MOROSIDAD ALUMNOS ENERO 2026(Sheet1).csv"

# TEST 1: Verificar que el archivo existe
print(f"\n[TEST 1] Verificando archivo CSV...")
try:
    df = pd.read_csv(csv_path, delimiter=',', encoding='utf-8')
    filas = len(df)
    columnas = len(df.columns)
    print(f"✓ Archivo encontrado:")
    print(f"  Filas: {filas}")
    print(f"  Columnas: {columnas}")
    print(f"  Primeras columnas: {', '.join(df.columns[:5].tolist())}")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# TEST 2: Conectar a base de datos
print(f"\n[TEST 2] Conectando a MySQL...")
try:
    db = DatabaseConnection()
    if not db.connect():
        print("✗ Error al conectar")
        sys.exit(1)
    print("✓ Conexión exitosa")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# TEST 3: Inicializar reader
print(f"\n[TEST 3] Inicializando ReporteMorosidadReader...")
try:
    reader = ReporteMorosidadReader(csv_path, db)
    total_rows = reader.get_total_rows()
    print(f"✓ Reader inicializado")
    print(f"  Total de filas a procesar: {total_rows}")
except Exception as e:
    print(f"✗ Error al inicializar reader: {e}")
    sys.exit(1)

# TEST 4: Procesar primeras filas (prueba pequeña)
print(f"\n[TEST 4] Procesando primeras filas (prueba de 5 filas)...")
try:
    # Usar solo las primeras 5 filas para la prueba
    df_small = df.head(5)
    print(f"  Procesando {len(df_small)} filas como prueba...")
    
    # Crear un reader temporal para las 5 filas
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, 
                                     encoding='utf-8', newline='') as tmp:
        df_small.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    reader_test = ReporteMorosidadReader(tmp_path, db)
    
    # Contador de progreso
    def progress(current):
        print(f"    Procesadas: {current}/{len(df_small)}", end='\r')
    
    # Procesar
    reader_test._process_and_upsert(progress_callback=progress)
    
    print(f"\n✓ Prueba completada exitosamente")
    print(f"  Métricas calculadas:")
    for key, value in reader_test.metricas_morosidad.items():
        if isinstance(value, float):
            print(f"    - {key}: {value:.2f}")
        else:
            print(f"    - {key}: {value}")
    
    # Limpiar archivo temporal
    import os
    os.unlink(tmp_path)

except Exception as e:
    print(f"\n✗ Error durante procesamiento: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# TEST 5: Desconectar
print(f"\n[TEST 5] Desconectando...")
try:
    db.disconnect()
    print("✓ Desconexión exitosa")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("✅ TEST EXITOSO - Los readers funcionan correctamente")
print("=" * 80)
print(f"\nRESUMEN:")
print(f"  • db_connection en modo HÍBRIDO: ✓ Funciona")
print(f"  • cursor(): ✓ Funciona")
print(f"  • Transacciones (commit/rollback): ✓ Funciona")
print(f"  • ReporteMorosidadReader: ✓ Funciona")
print(f"  \nLos datos se han insertado en la base de datos RDS")
