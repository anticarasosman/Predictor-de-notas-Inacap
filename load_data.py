from database.db_connection import DatabaseConnection
from classes.readers.asignaturas_criticas_reader import AsignaturaCriticasReader


def main():
    """
    Ejemplo de cómo usar los readers
    """
    
    # 1. CREAR CONEXIÓN A LA BASE DE DATOS (usa variables de .env)
    db = DatabaseConnection()
    
    if not db.connect():
        print("No se pudo establecer conexión a la base de datos")
        return
    
    connection = db.get_connection()
    
    try:
        # 2. USAR EL READER DE ASIGNATURAS CRÍTICAS
        print("\n--- Procesando Asignaturas Críticas ---")
        reader_asignaturas = AsignaturaCriticasReader(
            file_path=r'data/Asignaturas Críticas.csv',
            db_connection=connection
        )
        reader_asignaturas.read()
        
        # 3. PUEDES USAR OTROS READERS DE LA MISMA FORMA
        # Por ejemplo, cuando implementes los demás readers:
        # reader_morosidad = ReporteMorosidadReader(
        #     file_path=r'data/REPORTE MOROSIDAD ALUMNOS ENERO 2026(Sheet1).csv',
        #     db_connection=connection
        # )
        # reader_morosidad.read()
        
    finally:
        # 4. CERRAR CONEXIÓN
        db.disconnect()


if __name__ == "__main__":
    main()
