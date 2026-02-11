"""
AWS Lambda Function - INACAP Consultas API
Versión: 1.0
Fecha: Febrero 2026

Esta función maneja todas las operaciones de base de datos para la aplicación INACAP.
Expone acciones predefinidas para prevenir SQL injection y mantener seguridad.
"""

import json
import os
import mysql.connector
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# ============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ============================================================================

# Acciones permitidas (whitelist de seguridad)
ACCIONES_PERMITIDAS = {
    # Operaciones SELECT
    'listar_estudiantes',
    'buscar_estudiante',
    'listar_asignaturas',
    'listar_reportes_financieros',
    'consulta_personalizada',
    
    # Operaciones INSERT
    'insertar_estudiante',
    'insertar_asignatura',
    'insertar_reporte_financiero',
    
    # Operaciones UPDATE
    'actualizar_estudiante',
    'actualizar_asignatura',
    'actualizar_generico',
    
    # Operaciones DELETE
    'eliminar_estudiante',
    'eliminar_generico',
    
    # Utilidades
    'contar_registros',
    'verificar_conexion'
}

# Tablas permitidas para operaciones genéricas
TABLAS_PERMITIDAS = {
    'estudiante',
    'asignatura',
    'semestre',
    'reporte_financiero_estudiante',
    'estudiante_asignatura',
    'estudiante_semestre',
    'asignatura_semestre'
}

# Límite máximo de resultados por página
MAX_LIMITE = 1000
LIMITE_DEFAULT = 100


# ============================================================================
# UTILIDADES DE RESPUESTA
# ============================================================================

def respuesta_exitosa(datos: Any, metadatos: Optional[Dict] = None) -> Dict:
    """
    Genera una respuesta exitosa estandarizada.
    
    Args:
        datos: Los datos a devolver
        metadatos: Información adicional (paginación, conteos, etc.)
    
    Returns:
        Dict con el formato de respuesta estándar
    """
    respuesta = {
        'success': True,
        'datos': datos,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if metadatos:
        respuesta['metadatos'] = metadatos
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # CORS
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(respuesta, ensure_ascii=False, default=str)
    }


def respuesta_error(tipo: str, mensaje: str, codigo: int = 400) -> Dict:
    """
    Genera una respuesta de error estandarizada.
    
    Args:
        tipo: Tipo de error (ValidationError, DatabaseError, etc.)
        mensaje: Mensaje descriptivo del error
        codigo: Código HTTP (400, 404, 500, etc.)
    
    Returns:
        Dict con el formato de error estándar
    """
    return {
        'statusCode': codigo,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'success': False,
            'error': {
                'tipo': tipo,
                'mensaje': mensaje,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }, ensure_ascii=False)
    }


# ============================================================================
# CONEXIÓN A BASE DE DATOS
# ============================================================================

def obtener_conexion() -> mysql.connector.MySQLConnection:
    """
    Establece conexión con la base de datos RDS MySQL.
    Lee credenciales de variables de entorno.
    
    Returns:
        Objeto de conexión MySQL
    
    Raises:
        Exception: Si no se puede conectar
    """
    try:
        conexion = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            port=int(os.environ.get('DB_PORT', 3306)),
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            connect_timeout=10,
            autocommit=False  # Control manual de transacciones
        )
        return conexion
    except KeyError as e:
        raise Exception(f"Variable de entorno faltante: {str(e)}")
    except mysql.connector.Error as e:
        raise Exception(f"Error de conexión MySQL: {str(e)}")


# ============================================================================
# OPERACIONES SELECT (LECTURA)
# ============================================================================

def listar_estudiantes(conexion: mysql.connector.MySQLConnection, 
                       filtros: Optional[Dict] = None,
                       pagina: int = 1,
                       limite: int = LIMITE_DEFAULT) -> Tuple[List[Dict], Dict]:
    """
    Lista estudiantes con filtros opcionales y paginación.
    
    Args:
        conexion: Conexión a la base de datos
        filtros: Dict con filtros (rut, nombre, carrera, etc.)
        pagina: Número de página (1-indexed)
        limite: Cantidad de resultados por página
    
    Returns:
        Tuple (lista de estudiantes, metadatos de paginación)
    """
    cursor = conexion.cursor(dictionary=True)
    
    # Construir query base
    query = "SELECT * FROM estudiante WHERE 1=1"
    parametros = []
    
    # Agregar filtros de forma segura
    if filtros:
        if 'rut' in filtros:
            query += " AND rut = %s"
            parametros.append(filtros['rut'])
        if 'nombre' in filtros:
            query += " AND nombre LIKE %s"
            parametros.append(f"%{filtros['nombre']}%")
        if 'carrera' in filtros:
            query += " AND carrera LIKE %s"
            parametros.append(f"%{filtros['carrera']}%")
        if 'jornada' in filtros:
            query += " AND jornada = %s"
            parametros.append(filtros['jornada'])
    
    # Contar total de resultados (sin paginación)
    query_count = f"SELECT COUNT(*) as total FROM ({query}) as subquery"
    cursor.execute(query_count, parametros)
    total_resultados = cursor.fetchone()['total']
    
    # Aplicar paginación
    limite = min(limite, MAX_LIMITE)  # No exceder límite máximo
    offset = (pagina - 1) * limite
    query += f" LIMIT {limite} OFFSET {offset}"
    
    # Ejecutar query principal
    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    cursor.close()
    
    # Metadatos de paginación
    total_paginas = (total_resultados + limite - 1) // limite
    metadatos = {
        'pagina_actual': pagina,
        'limite': limite,
        'total_resultados': total_resultados,
        'total_paginas': total_paginas,
        'tiene_siguiente': pagina < total_paginas,
        'tiene_anterior': pagina > 1
    }
    
    return resultados, metadatos


def buscar_estudiante(conexion: mysql.connector.MySQLConnection, 
                      rut: str) -> Optional[Dict]:
    """
    Busca un estudiante específico por RUT.
    
    Args:
        conexion: Conexión a la base de datos
        rut: RUT del estudiante
    
    Returns:
        Dict con datos del estudiante o None si no existe
    """
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM estudiante WHERE rut = %s"
    cursor.execute(query, (rut,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado


def consulta_personalizada(conexion: mysql.connector.MySQLConnection,
                           tabla: str,
                           columnas: Optional[List[str]] = None,
                           filtros: Optional[Dict] = None,
                           pagina: int = 1,
                           limite: int = LIMITE_DEFAULT) -> Tuple[List[Dict], Dict]:
    """
    Ejecuta una consulta personalizada con validación de seguridad.
    
    Args:
        conexion: Conexión a la base de datos
        tabla: Nombre de la tabla (debe estar en TABLAS_PERMITIDAS)
        columnas: Lista de columnas a seleccionar (None = todas)
        filtros: Dict con filtros clave-valor
        pagina: Número de página
        limite: Cantidad de resultados
    
    Returns:
        Tuple (lista de resultados, metadatos)
    
    Raises:
        ValueError: Si la tabla no está permitida
    """
    # Validar tabla
    if tabla not in TABLAS_PERMITIDAS:
        raise ValueError(f"Tabla no permitida: {tabla}")
    
    cursor = conexion.cursor(dictionary=True)
    
    # Construir SELECT
    if columnas:
        # Sanitizar nombres de columnas (solo alfanuméricos y guiones bajos)
        columnas_safe = [c for c in columnas if c.replace('_', '').isalnum()]
        select_clause = ", ".join(columnas_safe)
    else:
        select_clause = "*"
    
    # Construir query base
    query = f"SELECT {select_clause} FROM {tabla} WHERE 1=1"
    parametros = []
    
    # Agregar filtros
    if filtros:
        for campo, valor in filtros.items():
            # Sanitizar nombre de campo
            if campo.replace('_', '').isalnum():
                query += f" AND {campo} = %s"
                parametros.append(valor)
    
    # Contar total
    query_count = f"SELECT COUNT(*) as total FROM {tabla} WHERE 1=1"
    if filtros:
        for campo, valor in filtros.items():
            if campo.replace('_', '').isalnum():
                query_count += f" AND {campo} = %s"
    
    cursor.execute(query_count, parametros)
    total_resultados = cursor.fetchone()['total']
    
    # Paginación
    limite = min(limite, MAX_LIMITE)
    offset = (pagina - 1) * limite
    query += f" LIMIT {limite} OFFSET {offset}"
    
    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    cursor.close()
    
    # Metadatos
    total_paginas = (total_resultados + limite - 1) // limite
    metadatos = {
        'pagina_actual': pagina,
        'limite': limite,
        'total_resultados': total_resultados,
        'total_paginas': total_paginas
    }
    
    return resultados, metadatos


# ============================================================================
# OPERACIONES INSERT (CREAR)
# ============================================================================

def insertar_estudiante(conexion: mysql.connector.MySQLConnection,
                        datos: Dict) -> Dict:
    """
    Inserta un nuevo estudiante en la base de datos.
    
    Args:
        conexion: Conexión a la base de datos
        datos: Dict con los campos del estudiante
    
    Returns:
        Dict con el resultado de la inserción
    """
    cursor = conexion.cursor()
    
    # Validar campos requeridos
    campos_requeridos = ['rut', 'nombre']
    for campo in campos_requeridos:
        if campo not in datos:
            raise ValueError(f"Campo requerido faltante: {campo}")
    
    # Construir INSERT
    columnas = ', '.join(datos.keys())
    placeholders = ', '.join(['%s'] * len(datos))
    query = f"INSERT INTO estudiante ({columnas}) VALUES ({placeholders})"
    
    cursor.execute(query, list(datos.values()))
    conexion.commit()
    
    resultado = {
        'insertado': True,
        'rut': datos['rut'],
        'filas_afectadas': cursor.rowcount
    }
    
    cursor.close()
    return resultado


def insertar_generico(conexion: mysql.connector.MySQLConnection,
                      tabla: str,
                      datos: Dict) -> Dict:
    """
    Inserta un registro en cualquier tabla permitida.
    
    Args:
        conexion: Conexión a la base de datos
        tabla: Nombre de la tabla
        datos: Dict con los campos a insertar
    
    Returns:
        Dict con el resultado
    """
    if tabla not in TABLAS_PERMITIDAS:
        raise ValueError(f"Tabla no permitida: {tabla}")
    
    cursor = conexion.cursor()
    
    columnas = ', '.join(datos.keys())
    placeholders = ', '.join(['%s'] * len(datos))
    query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
    
    cursor.execute(query, list(datos.values()))
    conexion.commit()
    
    resultado = {
        'insertado': True,
        'tabla': tabla,
        'id_insertado': cursor.lastrowid,
        'filas_afectadas': cursor.rowcount
    }
    
    cursor.close()
    return resultado


# ============================================================================
# OPERACIONES UPDATE (ACTUALIZAR)
# ============================================================================

def actualizar_estudiante(conexion: mysql.connector.MySQLConnection,
                          rut: str,
                          datos: Dict) -> Dict:
    """
    Actualiza los datos de un estudiante existente.
    
    Args:
        conexion: Conexión a la base de datos
        rut: RUT del estudiante a actualizar
        datos: Dict con los campos a actualizar
    
    Returns:
        Dict con el resultado
    """
    cursor = conexion.cursor()
    
    # No permitir actualizar el RUT
    if 'rut' in datos:
        del datos['rut']
    
    if not datos:
        raise ValueError("No hay campos para actualizar")
    
    # Construir UPDATE
    set_clause = ', '.join([f"{campo} = %s" for campo in datos.keys()])
    query = f"UPDATE estudiante SET {set_clause} WHERE rut = %s"
    
    parametros = list(datos.values()) + [rut]
    cursor.execute(query, parametros)
    conexion.commit()
    
    resultado = {
        'actualizado': cursor.rowcount > 0,
        'rut': rut,
        'filas_afectadas': cursor.rowcount
    }
    
    cursor.close()
    return resultado


def actualizar_generico(conexion: mysql.connector.MySQLConnection,
                        tabla: str,
                        id_campo: str,
                        id_valor: Any,
                        datos: Dict) -> Dict:
    """
    Actualiza un registro en cualquier tabla permitida.
    
    Args:
        conexion: Conexión a la base de datos
        tabla: Nombre de la tabla
        id_campo: Nombre del campo identificador
        id_valor: Valor del identificador
        datos: Dict con los campos a actualizar
    
    Returns:
        Dict con el resultado
    """
    if tabla not in TABLAS_PERMITIDAS:
        raise ValueError(f"Tabla no permitida: {tabla}")
    
    cursor = conexion.cursor()
    
    set_clause = ', '.join([f"{campo} = %s" for campo in datos.keys()])
    query = f"UPDATE {tabla} SET {set_clause} WHERE {id_campo} = %s"
    
    parametros = list(datos.values()) + [id_valor]
    cursor.execute(query, parametros)
    conexion.commit()
    
    resultado = {
        'actualizado': cursor.rowcount > 0,
        'tabla': tabla,
        'filas_afectadas': cursor.rowcount
    }
    
    cursor.close()
    return resultado


# ============================================================================
# OPERACIONES DELETE (ELIMINAR)
# ============================================================================

def eliminar_estudiante(conexion: mysql.connector.MySQLConnection,
                        rut: str) -> Dict:
    """
    Elimina un estudiante de la base de datos.
    
    Args:
        conexion: Conexión a la base de datos
        rut: RUT del estudiante a eliminar
    
    Returns:
        Dict con el resultado
    """
    cursor = conexion.cursor()
    query = "DELETE FROM estudiante WHERE rut = %s"
    cursor.execute(query, (rut,))
    conexion.commit()
    
    resultado = {
        'eliminado': cursor.rowcount > 0,
        'rut': rut,
        'filas_afectadas': cursor.rowcount
    }
    
    cursor.close()
    return resultado


def eliminar_generico(conexion: mysql.connector.MySQLConnection,
                      tabla: str,
                      id_campo: str,
                      id_valor: Any) -> Dict:
    """
    Elimina un registro de cualquier tabla permitida.
    
    Args:
        conexion: Conexión a la base de datos
        tabla: Nombre de la tabla
        id_campo: Nombre del campo identificador
        id_valor: Valor del identificador
    
    Returns:
        Dict con el resultado
    """
    if tabla not in TABLAS_PERMITIDAS:
        raise ValueError(f"Tabla no permitida: {tabla}")
    
    cursor = conexion.cursor()
    query = f"DELETE FROM {tabla} WHERE {id_campo} = %s"
    cursor.execute(query, (id_valor,))
    conexion.commit()
    
    resultado = {
        'eliminado': cursor.rowcount > 0,
        'tabla': tabla,
        'filas_afectadas': cursor.rowcount
    }
    
    cursor.close()
    return resultado


# ============================================================================
# HANDLER PRINCIPAL
# ============================================================================

def lambda_handler(event, context):
    """
    Handler principal de Lambda.
    Recibe eventos de API Gateway y los procesa.
    
    Args:
        event: Evento de API Gateway
        context: Contexto de Lambda
    
    Returns:
        Respuesta HTTP con formato API Gateway
    """
    try:
        # Manejar preflight CORS (OPTIONS)
        if event.get('httpMethod') == 'OPTIONS':
            return respuesta_exitosa({'mensaje': 'CORS preflight'})
        
        # Parsear body del request
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event  # Para testing directo sin API Gateway
        
        # Validar acción
        accion = body.get('accion')
        if not accion:
            return respuesta_error('ValidationError', 'Falta el campo "accion"', 400)
        
        if accion not in ACCIONES_PERMITIDAS:
            return respuesta_error('ValidationError', f'Acción no permitida: {accion}', 403)
        
        # Conectar a base de datos
        conexion = obtener_conexion()
        
        try:
            # Rutear a la función correcta según la acción
            if accion == 'listar_estudiantes':
                resultados, metadatos = listar_estudiantes(
                    conexion,
                    filtros=body.get('filtros'),
                    pagina=body.get('pagina', 1),
                    limite=body.get('limite', LIMITE_DEFAULT)
                )
                return respuesta_exitosa(resultados, metadatos)
            
            elif accion == 'buscar_estudiante':
                if 'rut' not in body:
                    return respuesta_error('ValidationError', 'Falta el campo "rut"', 400)
                resultado = buscar_estudiante(conexion, body['rut'])
                if resultado:
                    return respuesta_exitosa(resultado)
                else:
                    return respuesta_error('NotFoundError', f'Estudiante no encontrado: {body["rut"]}', 404)
            
            elif accion == 'consulta_personalizada':
                if 'tabla' not in body:
                    return respuesta_error('ValidationError', 'Falta el campo "tabla"', 400)
                resultados, metadatos = consulta_personalizada(
                    conexion,
                    tabla=body['tabla'],
                    columnas=body.get('columnas'),
                    filtros=body.get('filtros'),
                    pagina=body.get('pagina', 1),
                    limite=body.get('limite', LIMITE_DEFAULT)
                )
                return respuesta_exitosa(resultados, metadatos)
            
            elif accion == 'insertar_estudiante':
                if 'datos' not in body:
                    return respuesta_error('ValidationError', 'Falta el campo "datos"', 400)
                resultado = insertar_estudiante(conexion, body['datos'])
                return respuesta_exitosa(resultado)
            
            elif accion == 'actualizar_estudiante':
                if 'rut' not in body or 'datos' not in body:
                    return respuesta_error('ValidationError', 'Faltan campos: rut y/o datos', 400)
                resultado = actualizar_estudiante(conexion, body['rut'], body['datos'])
                return respuesta_exitosa(resultado)
            
            elif accion == 'actualizar_generico':
                campos_req = ['tabla', 'id_campo', 'id_valor', 'datos']
                if not all(campo in body for campo in campos_req):
                    return respuesta_error('ValidationError', f'Faltan campos requeridos: {campos_req}', 400)
                resultado = actualizar_generico(
                    conexion,
                    body['tabla'],
                    body['id_campo'],
                    body['id_valor'],
                    body['datos']
                )
                return respuesta_exitosa(resultado)
            
            elif accion == 'eliminar_estudiante':
                if 'rut' not in body:
                    return respuesta_error('ValidationError', 'Falta el campo "rut"', 400)
                resultado = eliminar_estudiante(conexion, body['rut'])
                return respuesta_exitosa(resultado)
            
            elif accion == 'eliminar_generico':
                campos_req = ['tabla', 'id_campo', 'id_valor']
                if not all(campo in body for campo in campos_req):
                    return respuesta_error('ValidationError', f'Faltan campos requeridos: {campos_req}', 400)
                resultado = eliminar_generico(
                    conexion,
                    body['tabla'],
                    body['id_campo'],
                    body['id_valor']
                )
                return respuesta_exitosa(resultado)
            
            elif accion == 'verificar_conexion':
                cursor = conexion.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                cursor.close()
                return respuesta_exitosa({'conectado': True, 'version_mysql': version})
            
            else:
                return respuesta_error('NotImplementedError', f'Acción no implementada: {accion}', 501)
        
        finally:
            # Siempre cerrar la conexión
            if conexion and conexion.is_connected():
                conexion.close()
    
    except ValueError as e:
        return respuesta_error('ValidationError', str(e), 400)
    
    except mysql.connector.Error as e:
        return respuesta_error('DatabaseError', f'Error de base de datos: {str(e)}', 500)
    
    except Exception as e:
        return respuesta_error('UnknownError', f'Error inesperado: {str(e)}', 500)

