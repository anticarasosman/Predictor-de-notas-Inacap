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

    def _estudiante_exists(self, cursor, rut):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT COUNT(*) FROM Estudiante WHERE rut = %s"
            cursor.execute(query, (rut,))
            result = cursor.fetchone() is not None
            cursor.close()
            return result
        except Error as e:
            print(f"✗ Error al verificar estudiante: {str(e)}")
            return False
        
    def _asignatura_exists(self, codigo):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT COUNT(*) FROM Asignatura WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            result = cursor.fetchone() is not None
            cursor.close()
            return result
        except Error as e:
            print(f"✗ Error al verificar asignatura: {str(e)}")
            return False
    
    # --- ESTUDIANTE ---
    
    def _insert_estudiante(self, cursor, rut, datos):
        """Inserta un nuevo estudiante"""
        pass
    
    def _update_estudiante(self, cursor, rut, datos):
        """Actualiza un estudiante existente"""
        pass
    
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
                INSERT IGNORE INTO Asignatura_semestre (
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
                UPDATE Asignatura_semestre SET
                    {', '.join(campos)}
                WHERE codigo_asignatura = %s AND periodo_semestre = %s
            """
            cursor.execute(query, valores)
            print(f"✓ Asignatura_semestre {codigo}-{periodo} actualizada")
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
                    deuda_colegiaturas, otras_deudas, deuda_total
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                rut,
                datos.get('cantidad_cuotas_pendientes_matriculas'),
                datos.get('cantidad_cuotas_pendientes_colegiaturas'),
                datos.get('deuda_matriculas'),
                datos.get('deuda_colegiaturas'),
                datos.get('otras_deudas'),
                datos.get('deuda_total')
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