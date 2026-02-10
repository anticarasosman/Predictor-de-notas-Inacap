#!/usr/bin/env python3
"""
Ejemplo de uso: Cómo procesar el reporte de morosidad y acceder a las métricas
"""

from database.db_connection import DatabaseConnection
from classes.readers.excel_reader.reporte_morosidad_reader import ReporteMorosidadReader

def main():
    # 1. Conectar a la base de datos
    db = DatabaseConnection()
    if not db.connect():
        print("Error: No se pudo conectar a la base de datos")
        return
    
    try:
        # 2. Crear el reader
        file_path = 'data/REPORTE MOROSIDAD ALUMNOS ENERO 2026(Sheet1).csv'
        reader = ReporteMorosidadReader(file_path, db)
        
        print(f"Procesando {reader.get_total_rows()} estudiantes...")
        
        # 3. Procesar y cargar datos (con callback de progreso opcional)
        def mostrar_progreso(actual):
            if actual % 10 == 0:  # Mostrar cada 10 registros
                print(f"  Procesados: {actual} registros...")
        
        reader._process_and_upsert(progress_callback=mostrar_progreso)
        
        # 4. Acceder a las métricas calculadas
        print("\n" + "="*60)
        print("MÉTRICAS DE MOROSIDAD")
        print("="*60)
        
        metricas = reader.metricas_morosidad
        
        print(f"\n📅 Fecha de actualización: {metricas['fecha_actualizacion']}")
        print(f"\n👥 Estudiantes:")
        print(f"   - Total: {metricas['numero_estudiantes_total']} estudiantes")
        print(f"   - Con deuda: {metricas['numero_estudiantes_con_deuda']} ({metricas['porcentaje_estudiantes_con_deuda']}%)")
        
        print(f"\n💰 Deuda:")
        print(f"   - Monto total adeudado: ${metricas['monto_total_adeudado']:,}")
        print(f"   - Monto total compromisos: ${metricas['monto_total_compromisos']:,}")
        
        print(f"\n📊 Cuotas y Morosidad:")
        print(f"   - Promedio cuotas pendientes: {metricas['promedio_cuotas_pendientes']} cuotas")
        print(f"   - % de Morosidad: {metricas['porcentaje_morosidad']}%")
        
        # 5. Acceder a resumen desde la BD
        print("\n" + "="*60)
        print("Datos persistidos en Base de Datos")
        print("="*60)
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM Resumen_reporte_morosidad 
            ORDER BY fecha_generacion DESC LIMIT 1
        """)
        resultado = cursor.fetchone()
        
        if resultado:
            print("\n✓ Último resumen en la BD:")
            for key, value in resultado.items():
                print(f"   {key}: {value}")
        
        cursor.close()
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()
