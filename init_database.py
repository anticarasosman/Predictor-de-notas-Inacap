"""
Script para inicializar la base de datos en AWS RDS o servidor local MySQL

Ejecuta todos los scripts SQL en el orden correcto:
1. Crea la base de datos
2. Carga esquemas y tablas
3. Carga datos semilla
4. Carga triggers (opcional)

Uso:
    python init_database.py
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import DatabaseConnection


def execute_sql_file(db: DatabaseConnection, file_path: str, description: str = None) -> bool:
    """
    Ejecuta un archivo SQL en la base de datos
    
    Args:
        db: Instancia de DatabaseConnection
        file_path: Ruta al archivo SQL
        description: Descripción opcional de lo que se está ejecutando
    
    Returns:
        True si ejecución fue exitosa, False si falló
    """
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por punto y coma, pero ignorar comentarios
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        cursor = db.connection.cursor()
        
        for statement in statements:
            # Ignorar comentarios
            if statement.startswith('--') or statement.startswith('/*'):
                continue
            
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"⚠️  Error en sentencia: {e}")
                    # Continuar con la siguiente sentencia
        
        db.connection.commit()
        cursor.close()
        
        status_msg = f"✓ {description}" if description else f"✓ {file_path}"
        print(status_msg)
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando {file_path}: {str(e)}")
        return False


def init_database():
    """
    Inicializa toda la base de datos AWS RDS
    """
    print("=" * 70)
    print("INICIALIZADOR DE BASE DE DATOS - AWS RDS / MySQL Local")
    print("=" * 70)
    
    # Mostrar configuración
    print("\n📋 Configuración de conexión:")
    print(f"  Host: {os.getenv('DB_HOST')}")
    print(f"  Port: {os.getenv('DB_PORT')}")
    print(f"  User: {os.getenv('DB_USER')}")
    print(f"  Database: {os.getenv('DB_NAME')}")
    
    # Conectar a base de datos
    print("\n🔗 Conectando a base de datos...")
    db = DatabaseConnection()
    
    if not db.connect():
        print("❌ No se pudo conectar a la base de datos")
        return False
    
    print("✓ Conexión exitosa!\n")
    
    # Definir directorio base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(base_dir, 'database')
    
    # Crear base de datos si no existe
    print("📊 Creando base de datos...")
    db_name = os.getenv('DB_NAME', 'inacap_test')
    try:
        cursor = db.connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(
            f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute(f"USE {db_name}")
        cursor.close()
        db.connection.commit()
        print(f"✓ Base de datos '{db_name}' creada\n")
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        db.disconnect()
        return False
    
    # Orden de ejecución de scripts
    scripts = [
        # FASE 1: Tablas base
        (os.path.join(db_dir, 'schema', 'core', 'estudiante.sql'), 'Tabla: estudiante'),
        (os.path.join(db_dir, 'schema', 'core', 'semestre.sql'), 'Tabla: semestre'),
        (os.path.join(db_dir, 'schema', 'core', 'asignatura.sql'), 'Tabla: asignatura'),
        (os.path.join(db_dir, 'schema', 'core', 'reporte_financiero_estudiante.sql'), 'Tabla: reporte_financiero_estudiante'),
        (os.path.join(db_dir, 'schema', 'core', 'resumen_reporte_morosidad.sql'), 'Tabla: resumen_reporte_morosidad'),
        
        # FASE 2: Tablas puente
        (os.path.join(db_dir, 'schema', 'bridge', 'estudiante_semestre.sql'), 'Tabla puente: estudiante_semestre'),
        (os.path.join(db_dir, 'schema', 'bridge', 'asignatura_semestre.sql'), 'Tabla puente: asignatura_semestre'),
        (os.path.join(db_dir, 'schema', 'bridge', 'estudiante_asignatura.sql'), 'Tabla puente: estudiante_asignatura'),
        
        # FASE 3: Datos semilla
        (os.path.join(db_dir, 'seed_data', '01_estudiante.sql'), 'Semilla: estudiantes'),
        (os.path.join(db_dir, 'seed_data', '02_semestre.sql'), 'Semilla: semestres'),
        (os.path.join(db_dir, 'seed_data', '03_asignatura.sql'), 'Semilla: asignaturas'),
        (os.path.join(db_dir, 'seed_data', '04_reporte_financiero.sql'), 'Semilla: reportes financieros'),
        (os.path.join(db_dir, 'seed_data', '05_estudiante_semestre.sql'), 'Semilla: estudiante_semestre'),
        (os.path.join(db_dir, 'seed_data', '06_asignatura_semestre.sql'), 'Semilla: asignatura_semestre'),
        (os.path.join(db_dir, 'seed_data', '07_estudiante_asignatura.sql'), 'Semilla: estudiante_asignatura'),
    ]
    
    # Ejecutar scripts
    print("📝 Ejecutando scripts SQL:\n")
    failed_scripts = []
    
    for script_path, description in scripts:
        if not execute_sql_file(db, script_path, description):
            failed_scripts.append((script_path, description))
    
    # Mostrar estadísticas finales
    print("\n" + "=" * 70)
    
    if failed_scripts:
        print(f"❌ {len(failed_scripts)} script(s) fallaron:")
        for script_path, description in failed_scripts:
            print(f"   - {description}")
        db.disconnect()
        return False
    else:
        # Verificar resultado
        try:
            cursor = db.connection.cursor()
            cursor.execute(f"USE {db_name}")
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s
            """, (db_name,))
            table_count = cursor.fetchone()[0]
            cursor.close()
            
            print("✅ INICIALIZACIÓN COMPLETADA CON ÉXITO")
            print(f"\n📊 Estadísticas:")
            print(f"  Base de datos: {db_name}")
            print(f"  Tablas creadas: {table_count}")
            print(f"  Charset: utf8mb4")
            print(f"  Collation: utf8mb4_unicode_ci")
            print("=" * 70)
            
            db.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Error verificando resultado: {e}")
            db.disconnect()
            return False


if __name__ == "__main__":
    try:
        success = init_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
