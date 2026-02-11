import pandas as pd
from classes.readers.reader import Reader
from datetime import datetime


class SituacionAcademicaReader(Reader):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.df = pd.read_csv(self.file_path, delimiter=';', skiprows=5, encoding='utf-8')

    def get_total_rows(self) -> int:
        """Retorna el número de filas del DataFrame"""
        return len(self.df)

    def _process_and_upsert(self, progress_callback=None):
        cursor = self.db_connection.cursor()
        
        # Función auxiliar para convertir a int de forma segura
        def safe_int(value):
            if not value or str(value).strip() == '' or str(value).lower() == 'nan':
                return 0
            try:
                return int(float(str(value).strip()))
            except (ValueError, TypeError):
                return 0
        
        # Función auxiliar para convertir fechas de DD-MM-YYYY a YYYY-MM-DD
        def convert_date(date_str):
            if not date_str or str(date_str).strip() == '' or str(date_str).lower() == 'nan':
                return None
            try:
                # Intenta convertir desde DD-MM-YYYY a YYYY-MM-DD
                date_obj = datetime.strptime(str(date_str).strip(), '%d-%m-%Y')
                return date_obj.strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                return None
        
        try:
            for index, row in self.df.iterrows():
                try:
                    if progress_callback:
                        progress_callback(index + 1)
                    
                    # Convertir RUT y DV a string para concatenación
                    rut_estudiante = str(row['RUT']).replace('.', '').strip() + '-' + str(row['DV']).strip()
                    periodo = str(row['PERIODO']).strip()

                    datos_estudiante = {
                        "rut": rut_estudiante,
                        "secciones_curriculares": int(row['SECCIONES CURRICULARES']) if row['SECCIONES CURRICULARES'] and str(row['SECCIONES CURRICULARES']).strip() != '' and str(row['SECCIONES CURRICULARES']).lower() != 'nan' else None,
                        "secciones_online": int(row['SECCIONES ONLINE']) if row['SECCIONES ONLINE'] and str(row['SECCIONES ONLINE']).strip() != '' and str(row['SECCIONES ONLINE']).lower() != 'nan' else None,
                        "asistencia_promedio": int(row['ASISTENCIA PROMEDIO']) if row['ASISTENCIA PROMEDIO'] and str(row['ASISTENCIA PROMEDIO']).strip() != '' and str(row['ASISTENCIA PROMEDIO']).lower() != 'nan' else None,
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
                        "ultima_asistencia": convert_date(row['ULTIMA ASISTENCIA']),
                    }
                    
                    datos_estudiante_semestre = {
                        "rut_estudiante": rut_estudiante,
                        "periodo_semestre": periodo,
                        "asignaturas_PE": safe_int(row['ASIGNATURAS PE']) or None,
                        "asignaturas_reprobadas": safe_int(row['ASIGNATURAS REPROBADAS CUARTA']) + safe_int(row['ASIGNATURAS REPROBADAS TERCERA']),
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
                
                except (ValueError, KeyError, TypeError) as e:
                    fila_num = index + 6  # +6 porque skiprows=5
                    raise ValueError(f"Error en fila {fila_num} (índice {index}): {str(e)}\nDatos de la fila: {dict(row)}")
        
        finally:
            cursor.close()
