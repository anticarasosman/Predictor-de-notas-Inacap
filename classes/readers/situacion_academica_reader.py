import pandas as pd
from classes.readers.reader import Reader


class SituacionAcademicaReader(Reader):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.df = pd.read_csv(self.file_path, delimiter=';', skiprows=5, encoding='utf-8')

    def _process_and_upsert(self):
        cursor = self.db_connection.cursor()
        
        try:
            for index, row in self.df.iterrows():
                rut_estudiante = row['RUT'] + '-' + str(row['DV'])
                periodo = row['PERIODO']

                datos_estudiante = {
                    "rut": rut_estudiante,
                    "secciones_curriculares": int(row['SECCIONES CURRICULARES']) if row['SECCIONES CURRICULARES'] else None,
                    "secciones_online": int(row['SECCIONES ONLINE']) if row['SECCIONES ONLINE'] else None,
                    "asistencia_promedio": int(row['ASISTENCIA PROMEDIO']) if row['ASISTENCIA PROMEDIO'] else None,
                    "nombre": row['NOMBRE'],
                    "programa_estudio": row['PROGRAMA'],
                    "nombre_apoderado": row['TUTOR'] if row['TUTOR'] and str(row['TUTOR']).strip() else None,
                    "terminal": True if row['ALUMNO TERMINAL'] == "SI" else False,
                    "tiene_gratuidad": True if row['TIENE GRATUIDAD'] == "SI" else False,
                    "solicitud_interrupcion_estudios": True if row['SOLICITUD INTERRUPCION PENDIENTE'] == "NO" else False,
                    "solicitud_interrupcion_estudio_pendiente": True if row['SOLICITUD INTERRUPCION PENDIENTE'] == "SI" else False,
                    "interrupcion_estudio_pendiente": True if row['INTERRUPCION ESTUDIO ANTERIOR'] == "SI" else False,
                    "beca_stem": True if row['BECA STEM'] == "SI" else False,
                    "tipo_alumno": row['TIPO ALUMNO SIES'],
                    "estado_matricula": row['ESTADO MATRICULA'],
                    "promedio_media_matematica": None,
                    "promedio_media_lenguaje": None,
                    "promedio_media_ingles": None,
                    "ultima_asistencia": row['ULTIMA ASISTENCIA'],
                }
                
                datos_estudiante_semestre = {
                    "rut_estudiante": rut_estudiante,
                    "periodo_semestre": periodo,
                    "asignaturas_PE": int(row['ASIGNATURAS PE']) if row['ASIGNATURAS PE'] else None,
                    "asignaturas_reprobadas": int(row['ASIGNATURAS REPROBADAS CUARTA']) + int(row['ASIGNATURAS REPROBADAS TERCERA']) if row['ASIGNATURAS REPROBADAS CUARTA'] and row['ASIGNATURAS REPROBADAS TERCERA'] else 0,
                    "promedio_notas_semestre": None,
                    "estado_situacion_academica": row['ESTADO MATRICULA'],
                }

                if self._estudiante_exists(cursor, rut_estudiante):
                    self._update_estudiante(cursor, rut_estudiante, datos_estudiante)
                else:
                    self._insert_estudiante(cursor, rut_estudiante, datos_estudiante)

                if self._estudiante_semestre_exists(cursor, rut_estudiante, periodo):
                    self._update_estudiante_semestre(cursor, rut_estudiante, periodo, datos_estudiante_semestre)
                else:
                    self._insert_estudiante_semestre(cursor, rut_estudiante, periodo, datos_estudiante_semestre)
        finally:
            cursor.close()
