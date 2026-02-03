import pandas as pd
from classes.readers.reader import Reader
import re

class ReporteMorosidadReader(Reader):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.patron_año = r'(\d{4})'
        self.df = pd.read_csv(self.file_path, delimiter=',', skiprows=0, encoding='utf-8')
        # Limpiar nombres de columnas (eliminar espacios)
        self.df.columns = self.df.columns.str.strip()

    def get_total_rows(self) -> int:
        """Retorna el número de filas del DataFrame"""
        return len(self.df)

    def _process_and_upsert(self, progress_callback=None):
        cursor = self.db_connection.cursor()
        
        try:
            for index, row in self.df.iterrows():
                if progress_callback:
                    progress_callback(index + 1)
                try:
                    rut_estudiante = row['Rut Alumno']
                    periodo = self._convert_periodo(row["Semestre"])

                    self._insert_semestre(cursor, periodo)

                    datos_estudiante = {
                        "rut": rut_estudiante,
                        "secciones_curriculares": None,
                        "secciones_online": None,
                        "deuda": int(str(row['Total Saldo']).replace('$', '').replace(',', '')) if row['Total Saldo'] and str(row['Total Saldo']) != '$0' else 0,
                        "asistencia_promedio": None,
                        "nombre": None,
                        "programa_estudio": row['Programa de Estudio'],
                        "nombre_apoderado": row['Nombre Apoderado'],
                        "terminal": False,
                        "tiene_gratuidad": True if row['Tiene Gratuidad'] == 1 or row['Tiene Gratuidad'] == "Si" or str(row['Tiene Gratuidad']).upper() == 'YES' else False,
                        "solicitud_interrupcion_estudios": None,
                        "solicitud_interrupcion_estudio_pendiente": None,
                        "interrupcion_estudio_pendiente": None,
                        "beca_stem": None,
                        "tipo_alumno": row['Tipo Alumno'],
                        "estado_matricula": row['Estado Matricula'],
                        "promedio_media_matematica": None,
                        "promedio_media_lenguaje": None,
                        "promedio_media_ingles": None,
                        "ultima_asistencia": None,
                    }
                    
                    datos_reporte_financiero_estudiante = {
                        "rut_estudiante": rut_estudiante,
                        "cantidad_cuotas_pendientes_matriculas": int(row['Cantidad Cuotas Pendientes Matricula']) if row['Cantidad Cuotas Pendientes Matricula'] else 0,
                        "cantidad_cuotas_pendientes_colegiaturas": int(row['Cantidad Cuotas Pendientes Colegiaturas']) if row['Cantidad Cuotas Pendientes Colegiaturas'] else 0,
                        "deuda_matriculas": int(str(row['Deuda Matriculas']).replace('$', '').replace(',', '')) if row['Deuda Matriculas'] and str(row['Deuda Matriculas']) != '$0' else 0,
                        "deuda_colegiaturas": int(str(row['Deuda Colegiaturas']).replace('$', '').replace(',', '')) if row['Deuda Colegiaturas'] and str(row['Deuda Colegiaturas']) != '$0' else 0,
                        "otras_deudas": int(row['Deuda Total Otras Deudas']) if row['Deuda Total Otras Deudas'] else 0,
                        "deuda_total": int(str(row['Deuda Total (Compromisos+Colegiaturas+Otras Deudas)']).replace('$', '').replace(',', '')) if row['Deuda Total (Compromisos+Colegiaturas+Otras Deudas)'] and str(row['Deuda Total (Compromisos+Colegiaturas+Otras Deudas)']) != '$0' else 0,
                    }

                    if self._estudiante_exists(cursor, rut_estudiante):
                        self._update_estudiante(cursor, rut_estudiante, datos_estudiante)
                        self._update_reporte_financiero(cursor, rut_estudiante, datos_reporte_financiero_estudiante)
                    else:
                        self._insert_estudiante(cursor, rut_estudiante, datos_estudiante)
                        self._insert_reporte_financiero(cursor, rut_estudiante, datos_reporte_financiero_estudiante)
                        
                except (ValueError, KeyError, TypeError) as e:
                    fila_num = index + 1
                    raise ValueError(f"Error en fila {fila_num} (índice {index}): {str(e)}\nDatos de la fila: {dict(row)}")

        finally:
            cursor.close()

    def _convert_periodo(self, periodo_str: str) -> str:
        periodo = re.search(self.patron_año, periodo_str)
        if periodo:
            año = periodo.group(1)
            if "PRIMAVERA" in periodo_str.upper():
                return f"PRIMAVERA {año}"
            elif "OTOÑO" in periodo_str.upper():
                return f"OTONO {año}"
