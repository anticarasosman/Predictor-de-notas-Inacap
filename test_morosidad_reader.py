#!/usr/bin/env python3
"""
Script de prueba para verificar que ReporteMorosidadReader funciona correctamente
y calcula las métricas de morosidad
"""

import pandas as pd
import sys
sys.path.insert(0, '.')

from database.db_connection import DatabaseConnection
from classes.readers.excel_reader.reporte_morosidad_reader import ReporteMorosidadReader

def test_morosidad_reader():
    """Test del reader de morosidad"""
    
    print("=" * 60)
    print("TEST: REPORTE MOROSIDAD READER")
    print("=" * 60)
    
    # Conectar a la base de datos
    db = DatabaseConnection()
    if not db.connect():
        print("✗ No se pudo conectar a la base de datos")
        return False
    
    try:
        # Crear reader
        file_path = 'data/REPORTE MOROSIDAD ALUMNOS ENERO 2026(Sheet1).csv'
        reader = ReporteMorosidadReader(file_path, db)
        
        print(f"✓ Reader creado exitosamente")
        print(f"  Total de filas a procesar: {reader.get_total_rows()}")
        
        # Procesar y cargar datos
        print("\nProcesando registros...")
        reader._process_and_upsert(progress_callback=lambda x: print(f"  Procesados: {x}/{reader.get_total_rows()}", end='\r'))
        
        # Mostrar métricas calculadas
        print("\n" + "=" * 60)
        print("MÉTRICAS DE MOROSIDAD CALCULADAS")
        print("=" * 60)
        
        if reader.metricas_morosidad:
            metricas = reader.metricas_morosidad
            print(f"\n✓ Fecha de actualización: {metricas['fecha_actualizacion']}")
            print(f"✓ Número de estudiantes total: {metricas['numero_estudiantes_total']}")
            print(f"✓ Número de estudiantes con deuda: {metricas['numero_estudiantes_con_deuda']}")
            print(f"✓ Porcentaje con deuda: {metricas['porcentaje_estudiantes_con_deuda']}%")
            print(f"✓ Monto total adeudado: ${metricas['monto_total_adeudado']:,}")
            print(f"✓ Monto total compromisos: ${metricas['monto_total_compromisos']:,}")
            print(f"✓ Promedio de cuotas pendientes: {metricas['promedio_cuotas_pendientes']}")
            print(f"✓ Porcentaje de morosidad: {metricas['porcentaje_morosidad']}%")
        else:
            print("✗ No se calcularon métricas")
            return False
        
        # Verificar que se insertaron datos en la BD
        print("\n" + "=" * 60)
        print("VERIFICACIÓN EN BASE DE DATOS")
        print("=" * 60)
        
        cursor = db.cursor()
        
        # Contar estudiantes en tabla
        cursor.execute("SELECT COUNT(*) FROM Estudiante")
        count_estudiantes = cursor.fetchone()[0]
        print(f"\n✓ Estudiantes en BD: {count_estudiantes}")
        
        # Contar reportes financieros
        cursor.execute("SELECT COUNT(*) FROM Reporte_financiero_estudiante")
        count_reportes = cursor.fetchone()[0]
        print(f"✓ Reportes financieros en BD: {count_reportes}")
        
        # Contar resúmenes de morosidad
        cursor.execute("SELECT COUNT(*) FROM Resumen_reporte_morosidad")
        count_resumenes = cursor.fetchone()[0]
        print(f"✓ Resúmenes de morosidad en BD: {count_resumenes}")
        
        # Mostrar último resumen
        cursor.execute("""
            SELECT fecha_actualizacion, numero_estudiantes_total, numero_estudiantes_con_deuda,
                   porcentaje_estudiantes_con_deuda, monto_total_adeudado, monto_total_compromisos,
                   promedio_cuotas_pendientes, porcentaje_morosidad
            FROM Resumen_reporte_morosidad
            ORDER BY fecha_generacion DESC
            LIMIT 1
        """)
        resultado = cursor.fetchone()
        if resultado:
            print(f"\n✓ Último resumen en BD:")
            print(f"  - Fecha: {resultado[0]}")
            print(f"  - Total estudiantes: {resultado[1]}")
            print(f"  - Con deuda: {resultado[2]} ({resultado[3]}%)")
            print(f"  - Deuda total: ${resultado[4]:,}")
            print(f"  - Compromisos total: ${resultado[5]:,}")
            print(f"  - Promedio cuotas: {resultado[6]}")
            print(f"  - % Morosidad: {resultado[7]}%")
        
        cursor.close()
        print("\n✓ TEST COMPLETADO EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"\n✗ Error durante el test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = test_morosidad_reader()
    sys.exit(0 if success else 1)
