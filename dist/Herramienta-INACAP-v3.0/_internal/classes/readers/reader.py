from abc import ABC, abstractmethod
import pandas as pd
from mysql.connector import Error

class Reader(ABC):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
    
    @abstractmethod
    def _process_and_upsert(self):
        pass
    
    @abstractmethod
    def get_total_rows(self) -> int:
        """Retorna el número total de filas/registros a procesar"""
        pass

    def _estudiante_exists(self, cursor, rut):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT COUNT(*) FROM Estudiante WHERE rut = %s"
            cursor.execute(query, (rut,))
            result = cursor.fetchone()[0] > 0
            cursor.close()
            return result
        except Error as e:
            # Error 1146 es "Table doesn't exist"
            if e.errno == 1146:
                raise Exception(f"ERROR CRÍTICO: Tabla no existe. {str(e)}")
            print(f"✗ Error al verificar estudiante: {str(e)}")
            raise
        
    def _asignatura_exists(self, codigo):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT COUNT(*) FROM Asignatura WHERE codigo_asignatura = %s"
            cursor.execute(query, (codigo,))
            result = cursor.fetchone()[0] > 0
            cursor.close()
            return result
        except Error as e:
            # Error 1146 es "Table doesn't exist"
            if e.errno == 1146:
                raise Exception(f"ERROR CRÍTICO: Tabla no existe. {str(e)}")
            print(f"✗ Error al verificar asignatura: {str(e)}")
            raise
        
    def _asignatura_semestre_exists(self, cursor, codigo, periodo):
        try:
            query = "SELECT COUNT(*) FROM Asignatura_Semestre WHERE codigo_asignatura = %s AND periodo_semestre = %s"
            cursor.execute(query, (codigo, periodo))
            result = cursor.fetchone()[0] > 0
            return result
        except Error as e:
            # Error 1146 es "Table doesn't exist"
            if e.errno == 1146:
                raise Exception(f"ERROR CRÍTICO: Tabla no existe. {str(e)}")
            print(f"✗ Error al verificar asignatura_semestre: {str(e)}")
            raise
    
    def _estudiante_semestre_exists(self, cursor, rut, periodo):
        try:
            query = "SELECT COUNT(*) FROM Estudiante_Semestre WHERE rut_estudiante = %s AND periodo_semestre = %s"
            cursor.execute(query, (rut, periodo))
            result = cursor.fetchone()[0] > 0
            return result
        except Error as e:
            # Error 1146 es "Table doesn't exist"
            if e.errno == 1146:
                raise Exception(f"ERROR CRÍTICO: Tabla no existe. {str(e)}")
            print(f"✗ Error al verificar estudiante_semestre: {str(e)}")
            raise
        
    def _estudiante_asignatura_exists(self, cursor, rut, codigo, periodo):
        try:
            query = "SELECT COUNT(*) FROM Estudiante_Asignatura WHERE rut_estudiante = %s AND codigo_asignatura = %s AND periodo_semestre = %s"
            cursor.execute(query, (rut, codigo, periodo))
            result = cursor.fetchone()[0] > 0
            return result
        except Error as e:
            # Error 1146 es "Table doesn't exist"
            if e.errno == 1146:
                raise Exception(f"ERROR CRÍTICO: Tabla no existe. {str(e)}")
            print(f"✗ Error al verificar estudiante_asignatura: {str(e)}")
            raise
    
    # --- ESTUDIANTE ---
    
    def _insert_estudiante(self, cursor, rut, datos):
        """Inserta un nuevo estudiante"""
        try:
            query = """
                INSERT INTO Estudiante (
                    rut, nombre, programa_estudio, nombre_apoderado, terminal,
                    tiene_gratuidad, solicitud_interrupcion_estudios, 
                    solicitud_interrupcion_estudio_pendiente, interrupcion_estudio_pendiente,
                    beca_stem, tipo_alumno, estado_matricula, secciones_curriculares,
                    secciones_online, asistencia_promedio, promedio_media_matematica,
                    promedio_media_lenguaje, promedio_media_ingles, ultima_asistencia, deuda
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                rut,
                datos.get('nombre'),
                datos.get('programa_estudio'),
                datos.get('nombre_apoderado'),
                datos.get('terminal'),
                datos.get('tiene_gratuidad'),
                datos.get('solicitud_interrupcion_estudios'),
                datos.get('solicitud_interrupcion_estudio_pendiente'),
                datos.get('interrupcion_estudio_pendiente'),
                datos.get('beca_stem'),
                datos.get('tipo_alumno'),
                datos.get('estado_matricula'),
                datos.get('secciones_curriculares'),
                datos.get('secciones_online'),
                datos.get('asistencia_promedio'),
                datos.get('promedio_media_matematica'),
                datos.get('promedio_media_lenguaje'),
                datos.get('promedio_media_ingles'),
                datos.get('ultima_asistencia'),
                datos.get('deuda')
            )
            cursor.execute(query, values)
            print(f"✓ Estudiante {rut} creado")
        except Error as e:
            print(f"✗ Error al insertar estudiante {rut}: {str(e)}")
            raise
    
    def _update_estudiante(self, cursor, rut, datos):
        """Actualiza un estudiante existente (solo campos no None)"""
        try:
            campos = []
            valores = []
            for key, value in datos.items():
                if value is not None:
                    campos.append(f"{key} = %s")
                    valores.append(value)
            
            if not campos:
                print(f"→ No hay datos para actualizar en estudiante {rut}")
                return
            
            valores.append(rut)
            query = f"""
                UPDATE Estudiante SET
                    {', '.join(campos)}
                WHERE rut = %s
            """
            cursor.execute(query, valores)
            print(f"✓ Estudiante {rut} actualizado")
        except Error as e:
            print(f"✗ Error al actualizar estudiante {rut}: {str(e)}")
            raise
    
    # --- SEMESTRE ---
    
    def _insert_semestre(self, cursor, periodo):
        """Inserta un nuevo semestre solo si no existe"""
        try:
            query = "INSERT IGNORE INTO Semestre (periodo) VALUES (%s)"
            cursor.execute(query, (periodo,))
        
            if cursor.rowcount > 0:
                print(f"✓ Semestre {periodo} creado")
            else:
                print(f"→ Semestre {periodo} ya existe")
            
        except Error as e:
            print(f"✗ Error al insertar semestre: {str(e)}")
            raise
    
    # --- ASIGNATURA ---
    
    def _insert_asignatura(self, cursor, codigo, datos):
        """Inserta una nueva asignatura"""
        try:
            query = """
                INSERT INTO Asignatura (
                    codigo_asignatura, nombre, programa, area, COD_mencion, 
                    mencion, plan, modalidad, nivel, prerequisito_semestre_siguiente, ultimo_nivel
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                codigo,
                datos.get('nombre'),
                datos.get('programa'),
                datos.get('area'),
                datos.get('COD_mencion'),
                datos.get('mencion'),
                datos.get('plan'),
                datos.get('modalidad'),
                datos.get('nivel'),
                datos.get('prerequisito_semestre_siguiente'),
                datos.get('ultimo_nivel')
            )
            cursor.execute(query, values)
            print(f"✓ Asignatura {codigo} creada")
        except Error as e:
            print(f"✗ Error al insertar asignatura {codigo}: {str(e)}")
            raise
    
    def _update_asignatura(self, cursor, codigo, datos):
        """Actualiza una asignatura existente (solo campos no None)"""
        try:
            campos = []
            valores = []
            for key, value in datos.items():
                if value is not None:
                    campos.append(f"{key} = %s")
                    valores.append(value)
            
            if not campos:
                print(f"→ No hay datos para actualizar en asignatura {codigo}")
                return
            
            valores.append(codigo)
            query = f"""
                UPDATE Asignatura SET
                    {', '.join(campos)}
                WHERE codigo_asignatura = %s
            """
            cursor.execute(query, valores)
            print(f"✓ Asignatura {codigo} actualizada")
        except Error as e:
            print(f"✗ Error al actualizar asignatura {codigo}: {str(e)}")
            raise
    
    # --- ASIGNATURA_SEMESTRE ---
    
    def _insert_asignatura_semestre(self, cursor, codigo, periodo, datos):
        """Inserta asignatura en semestre"""
        try:
            query = """
                INSERT IGNORE INTO Asignatura_Semestre (
                    codigo_asignatura, periodo_semestre, secciones, alumnos, alumnos_en_riesgo,
                    alumnos_ayudantia, porcentaje_reprobacion_N1, porcentaje_reprobacion_N2,
                    porcentaje_reprobacion_N3, promedio_nota_uno, promedio_nota_dos,
                    promedio_nota_tres, ayudantia_virtual, ayudantia_sede
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                codigo,
                periodo,
                datos.get('secciones'),
                datos.get('alumnos'),
                datos.get('alumnos_en_riesgo'),
                datos.get('alumnos_ayudantia'),
                datos.get('porcentaje_reprobacion_N1'),
                datos.get('porcentaje_reprobacion_N2'),
                datos.get('porcentaje_reprobacion_N3'),
                datos.get('promedio_nota_uno'),
                datos.get('promedio_nota_dos'),
                datos.get('promedio_nota_tres'),
                datos.get('ayudantia_virtual'),
                datos.get('ayudantia_sede')
            )
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                print(f"✓ Asignatura_semestre {codigo}-{periodo} creada")
            else:
                print(f"→ Asignatura_semestre {codigo}-{periodo} ya existe")
        except Error as e:
            print(f"✗ Error al insertar asignatura_semestre {codigo}-{periodo}: {str(e)}")
            raise
    
    def _update_asignatura_semestre(self, cursor, codigo, periodo, datos):
        """Actualiza asignatura en semestre (solo campos no None)"""
        try:
            campos = []
            valores = []
            for key, value in datos.items():
                if value is not None:
                    campos.append(f"{key} = %s")
                    valores.append(value)
            
            if not campos:
                print(f"→ No hay datos para actualizar en asignatura_semestre {codigo}-{periodo}")
                return
            
            valores.extend([codigo, periodo])
            query = f"""
                UPDATE Asignatura_Semestre SET
                    {', '.join(campos)}
                WHERE codigo_asignatura = %s AND periodo_semestre = %s
            """
            cursor.execute(query, valores)
            print(f"✓ Asignatura_Semestre {codigo}-{periodo} actualizada")
        except Error as e:
            print(f"✗ Error al actualizar asignatura_semestre {codigo}-{periodo}: {str(e)}")
            raise
    
    # --- ESTUDIANTE_SEMESTRE ---
    
    def _insert_estudiante_semestre(self, cursor, rut, periodo, datos):
        """Inserta estudiante en semestre"""
        pass
    
    def _update_estudiante_semestre(self, cursor, rut, periodo, datos):
        """Actualiza estudiante en semestre"""
        pass
    
    # --- ESTUDIANTE_ASIGNATURA ---
    
    def _insert_estudiante_asignatura(self, cursor, rut, codigo, periodo, datos):
        """Inserta estudiante en asignatura"""
        pass
    
    def _update_estudiante_asignatura(self, cursor, rut, codigo, periodo, datos):
        """Actualiza estudiante en asignatura"""
        pass
    
    # --- REPORTE_FINANCIERO ---

    def _insert_reporte_financiero(self, cursor, rut, datos):
        """Inserta reporte financiero"""
        try:
            query = """
                INSERT INTO Reporte_financiero_estudiante (
                    rut_estudiante, cantidad_cuotas_pendientes_matriculas,
                    cantidad_cuotas_pendientes_colegiaturas, deuda_matriculas,
                    deuda_colegiaturas, otras_deudas, deuda_total,
                    monto_compromiso_matricula, monto_compromiso_colegiaturas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                rut,
                datos.get('cantidad_cuotas_pendientes_matriculas'),
                datos.get('cantidad_cuotas_pendientes_colegiaturas'),
                datos.get('deuda_matriculas'),
                datos.get('deuda_colegiaturas'),
                datos.get('otras_deudas'),
                datos.get('deuda_total'),
                datos.get('monto_compromiso_matricula'),
                datos.get('monto_compromiso_colegiaturas')
            )
            cursor.execute(query, values)
            print(f"✓ Reporte financiero para {rut} creado")
        except Error as e:
            print(f"✗ Error al insertar reporte financiero {rut}: {str(e)}")
            raise
    
    def _update_reporte_financiero(self, cursor, rut, datos):
        """Actualiza reporte financiero (solo campos no None)"""
        try:
            campos = []
            valores = []
            for key, value in datos.items():
                if value is not None:
                    campos.append(f"{key} = %s")
                    valores.append(value)
            
            if not campos:
                print(f"→ No hay datos para actualizar en reporte financiero {rut}")
                return
            
            valores.append(rut)
            query = f"""
                UPDATE Reporte_financiero_estudiante SET
                    {', '.join(campos)}
                WHERE rut_estudiante = %s
            """
            cursor.execute(query, valores)
            print(f"✓ Reporte financiero para {rut} actualizado")
        except Error as e:
            print(f"✗ Error al actualizar reporte financiero {rut}: {str(e)}")
            raise