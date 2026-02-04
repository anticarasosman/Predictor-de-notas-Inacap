def get_student_tables(db_connection) -> dict:
    """
    Obtiene todas las tablas de la base de datos y sus columnas
    
    Returns:
        dict: {'Estudiante': ['rut', 'nombre', ...], 'Asignatura': [...], ...}
    """
    cursor = db_connection.cursor(dictionary=True)
    
    try:
        # Obtener todas las tablas de la base de datos actual
        query = """
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME IN (
                        'Estudiante',
                        'Estudiante_Asignatura',
                        'Estudiante_Semestre',
                        'Reporte_financiero_estudiante'
                    )
                ORDER BY TABLE_NAME
        """
        cursor.execute(query)
        tables = cursor.fetchall()
        
        # Crear diccionario con tablas y sus columnas
        result = {}
        for table_row in tables:
            table_name = table_row['TABLE_NAME']
            columns = get_table_columns(db_connection, table_name)
            result[table_name] = columns
        
        return result
    
    finally:
        cursor.close()

def get_table_columns(db_connection, table_name: str) -> list:
    """
    Obtiene las columnas de una tabla específica
    
    Args:
        db_connection: Conexión a la base de datos
        table_name: Nombre de la tabla
        
    Returns:
        list: ['rut', 'nombre', 'programa_estudio', ...]
    """
    cursor = db_connection.cursor(dictionary=True)
    
    try:
        query = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND COLUMN_NAME NOT IN ('id', 'fecha_registro', 'fecha_modificacion')
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (table_name,))
        columns = cursor.fetchall()
        
        # Retornar solo los nombres de las columnas
        return [col['COLUMN_NAME'] for col in columns]
    
    finally:
        cursor.close()