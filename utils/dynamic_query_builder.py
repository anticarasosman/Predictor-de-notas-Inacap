def build_query_for_custom_sheet(rut: str, table: str, columns: list) -> tuple:
    """
    Construye una consulta SQL dinámica para obtener datos de una tabla específica
    
    Args:
        rut: RUT del estudiante (sin puntos)
        table: Nombre de la tabla
        columns: Lista de columnas a seleccionar
        
    Returns:
        tuple: (query, (params)) - Query SQL y parámetros para execute()
    """
    
    # Validar que no esté vacío
    if not columns or not table:
        raise ValueError("Tabla y columnas son requeridas")
    
    # Escapar nombres de columnas y tabla (evitar SQL injection)
    safe_columns = ", ".join([f"`{col}`" for col in columns])
    safe_table = f"`{table}`"
    
    # Detectar si es tabla bridge (contiene rut_estudiante) o tabla normal
    if "rut_estudiante" in columns or table.lower().startswith("estudiante_"):
        # Es tabla bridge - usar rut_estudiante como filtro
        query = f"SELECT {safe_columns} FROM {safe_table} WHERE rut_estudiante = %s"
    else:
        # Es tabla normal - usar rut como filtro
        query = f"SELECT {safe_columns} FROM {safe_table} WHERE rut = %s"
    
    return query, (rut,)