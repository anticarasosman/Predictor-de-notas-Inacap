import pandas as pd
from classes.readers.reader import Reader


class SeguimientoDeAlumnosReader(Reader):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.df = pd.read_csv(self.file_path, delimiter=';', skiprows=5, encoding='utf-8')

    def get_total_rows(self) -> int:
        """Retorna el número de filas del DataFrame"""
        return len(self.df)

    def _process_and_upsert(self, progress_callback=None):
        cursor = self.db_connection.cursor()
        
        try:
            for index, row in self.df.iterrows():
                if progress_callback:
                    progress_callback(index + 1)
                rut_estudiante = row['Rut Alumno']
                codigo_asignatura = row['Cod Asignatura']
                periodo = row['Periodo']

                datos_estudiante = {
                    "rut": rut_estudiante,
                    "secciones_curriculares": None,
                    "secciones_online": None,
                    "asistencia_promedio": None,
                    "nombre": row['Nombre Alumno'],
                    "programa_estudio": None,
                    "nombre_apoderado": None,
                    "terminal": False,
                    "tiene_gratuidad": None,
                    "solicitud_interrupcion_estudios": True if row['Solicitud Interrupción de Estudios'] == "Si" else False,
                    "solicitud_interrupcion_estudio_pendiente": None,
                    "interrupcion_estudio_pendiente": None,
                    "beca_stem": None,
                    "tipo_alumno": "NUEVO" if row['Alumno Nuevo Inacap'].upper() == "NUEVO" else "VIEJO",
                    "estado_matricula": None,
                    "promedio_media_matematica": None,
                    "promedio_media_lenguaje": None,
                    "promedio_media_ingles": None,
                    "ultima_asistencia": None,
                }

                datos_asignatura = {
                    "codigo_asignatura": codigo_asignatura,
                    "nombre": row['Asignatura'],
                    "programa": None,
                    "area": row['Área'],
                    "COD_mencion": None,
                    "mencion": None,
                    "plan": None,
                    "modalidad": None,
                    "nivel": None,
                    "prerequisito_semestre_siguiente": None,
                    "ultimo_nivel": None,
                }
                
                datos_estudiante_semestre = {
                    "rut_estudiante": rut_estudiante,
                    "periodo_semestre": periodo,
                    "asignaturas_PE": None,
                    "asignaturas_reprobadas_cuatro_veces": None,
                    "asignaturas_reprobadas_tres_veces": None,
                    "solicitud_reingreso": None,
                }

                datos_estudiante_asignatura = {
                    "rut_estudiante": rut_estudiante,
                    "codigo_asignatura": codigo_asignatura,
                    "periodo_semestre": periodo,
                    "nombre_docente": row['Nombre Docente'],
                    "notas_parciales": str(row['Notas Parciales']).replace("(Z)", "") if row['Notas Parciales'] and str(row['Notas Parciales']) != 'nan' else None,
                    "porcentaje_asistencia": int(row['% Asistencia']) if row['% Asistencia'] else None,
                    "riesgo": True if row['Riesgo'] == "RI" else False,
                }

                if self._estudiante_exists(cursor, rut_estudiante):
                    self._update_estudiante(cursor, rut_estudiante, datos_estudiante)
                else:
                    self._insert_estudiante(cursor, rut_estudiante, datos_estudiante)

                if self._estudiante_semestre_exists(cursor, rut_estudiante, periodo):
                    self._update_estudiante_semestre(cursor, rut_estudiante, periodo, datos_estudiante_semestre)
                else:
                    self._insert_estudiante_semestre(cursor, rut_estudiante, periodo, datos_estudiante_semestre)

                if self._asignatura_exists(codigo_asignatura):
                    self._update_asignatura(cursor, codigo_asignatura, datos_asignatura)
                else:
                    self._insert_asignatura(cursor, codigo_asignatura, datos_asignatura)

                if self._estudiante_asignatura_exists(cursor, rut_estudiante, codigo_asignatura, periodo):
                    self._update_estudiante_asignatura(cursor, rut_estudiante, codigo_asignatura, periodo, datos_estudiante_asignatura)
                else:
                    self._insert_estudiante_asignatura(cursor, rut_estudiante, codigo_asignatura, periodo, datos_estudiante_asignatura)
                    
        finally:
            cursor.close()
