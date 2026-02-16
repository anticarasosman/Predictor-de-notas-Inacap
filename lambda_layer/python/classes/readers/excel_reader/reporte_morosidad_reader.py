import pandas as pd
from classes.readers.reader import Reader
import re
from datetime import datetime

class ReporteMorosidadReader(Reader):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.patron_año = r'(\d{4})'
        self.df = pd.read_csv(self.file_path, delimiter=',', skiprows=0, encoding='utf-8')
        # Limpiar nombres de columnas (eliminar espacios)
        self.df.columns = self.df.columns.str.strip()
        # Métricas de morosidad
        self.metricas_morosidad = {}

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
                    
                    # Convertir compromisos a int
                    monto_compromiso_matricula = int(str(row['Monto Compromiso Matricula']).replace('$', '').replace(',', '')) if row['Monto Compromiso Matricula'] and str(row['Monto Compromiso Matricula']) != '$0' else 0
                    monto_compromiso_colegiaturas = int(str(row['Monto Compromisos Colegiaturas']).replace('$', '').replace(',', '')) if row['Monto Compromisos Colegiaturas'] and str(row['Monto Compromisos Colegiaturas']) != '$0' else 0
                    
                    datos_reporte_financiero_estudiante = {
                        "rut_estudiante": rut_estudiante,
                        "cantidad_cuotas_pendientes_matriculas": int(row['Cantidad Cuotas Pendientes Matricula']) if row['Cantidad Cuotas Pendientes Matricula'] else 0,
                        "cantidad_cuotas_pendientes_colegiaturas": int(row['Cantidad Cuotas Pendientes Colegiaturas']) if row['Cantidad Cuotas Pendientes Colegiaturas'] else 0,
                        "deuda_matriculas": int(str(row['Deuda Matriculas']).replace('$', '').replace(',', '')) if row['Deuda Matriculas'] and str(row['Deuda Matriculas']) != '$0' else 0,
                        "deuda_colegiaturas": int(str(row['Deuda Colegiaturas']).replace('$', '').replace(',', '')) if row['Deuda Colegiaturas'] and str(row['Deuda Colegiaturas']) != '$0' else 0,
                        "otras_deudas": int(row['Deuda Total Otras Deudas']) if row['Deuda Total Otras Deudas'] else 0,
                        "deuda_total": int(str(row['Deuda Total (Compromisos+Colegiaturas+Otras Deudas)']).replace('$', '').replace(',', '')) if row['Deuda Total (Compromisos+Colegiaturas+Otras Deudas)'] and str(row['Deuda Total (Compromisos+Colegiaturas+Otras Deudas)']) != '$0' else 0,
                        "monto_compromiso_matricula": monto_compromiso_matricula,
                        "monto_compromiso_colegiaturas": monto_compromiso_colegiaturas,
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
            
            # Después de procesar todos los registros, calcular y guardar métricas de morosidad
            self._calculate_and_insert_morosidad_summary(cursor)

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

    def _calculate_and_insert_morosidad_summary(self, cursor):
        """
        Calcula métricas resumidas de morosidad y las inserta en la tabla Resumen_reporte_morosidad
        """
        try:
            # Convertir Total Saldo a numérico para cálculos
            self.df['Total_Saldo_num'] = self.df['Total Saldo'].apply(
                lambda x: int(str(x).replace('$', '').replace(',', '')) if x and str(x) != '$0' else 0
            )
            
            # Convertir compromisos a numéricos
            self.df['Monto_Compromiso_Matricula_num'] = self.df['Monto Compromiso Matricula'].apply(
                lambda x: int(str(x).replace('$', '').replace(',', '')) if x and str(x) != '$0' else 0
            )
            
            self.df['Monto_Compromiso_Colegiaturas_num'] = self.df['Monto Compromisos Colegiaturas'].apply(
                lambda x: int(str(x).replace('$', '').replace(',', '')) if x and str(x) != '$0' else 0
            )
            
            # Convertir cuotas Colegiaturas a numérico para promedio
            self.df['Cuotas_Colegiaturas_num'] = pd.to_numeric(self.df['Cantidad Cuotas Pendientes Colegiaturas'], errors='coerce').fillna(0).astype(int)
            
            # Calcular métricas
            numero_estudiantes_total = int(len(self.df))
            numero_estudiantes_con_deuda = int((self.df['Total_Saldo_num'] > 0).sum())
            porcentaje_con_deuda = float((numero_estudiantes_con_deuda / numero_estudiantes_total * 100) if numero_estudiantes_total > 0 else 0)
            
            monto_total_adeudado = int(self.df['Total_Saldo_num'].sum())
            monto_total_compromisos = int(self.df['Monto_Compromiso_Matricula_num'].sum() + self.df['Monto_Compromiso_Colegiaturas_num'].sum())
            
            # Promedio de cuotas pendientes (solo mayores que 0)
            cuotas_mayores_cero = self.df[self.df['Cuotas_Colegiaturas_num'] > 0]['Cuotas_Colegiaturas_num']
            promedio_cuotas = float(cuotas_mayores_cero.mean()) if len(cuotas_mayores_cero) > 0 else 0.0
            
            # Porcentaje de morosidad
            porcentaje_morosidad = float((monto_total_adeudado / monto_total_compromisos * 100) if monto_total_compromisos > 0 else 0)
            
            # Fecha de actualización (hoy)
            fecha_actualizacion = datetime.now().date()
            
            # Guardar métricas en la tabla
            query = """
                INSERT INTO Resumen_reporte_morosidad 
                (fecha_actualizacion, numero_estudiantes_total, numero_estudiantes_con_deuda, 
                 porcentaje_estudiantes_con_deuda, monto_total_adeudado, monto_total_compromisos,
                 promedio_cuotas_pendientes, porcentaje_morosidad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                numero_estudiantes_total = VALUES(numero_estudiantes_total),
                numero_estudiantes_con_deuda = VALUES(numero_estudiantes_con_deuda),
                porcentaje_estudiantes_con_deuda = VALUES(porcentaje_estudiantes_con_deuda),
                monto_total_adeudado = VALUES(monto_total_adeudado),
                monto_total_compromisos = VALUES(monto_total_compromisos),
                promedio_cuotas_pendientes = VALUES(promedio_cuotas_pendientes),
                porcentaje_morosidad = VALUES(porcentaje_morosidad),
                fecha_generacion = CURRENT_TIMESTAMP
            """
            
            cursor.execute(query, (
                fecha_actualizacion,
                numero_estudiantes_total,
                numero_estudiantes_con_deuda,
                round(porcentaje_con_deuda, 2),
                monto_total_adeudado,
                monto_total_compromisos,
                round(promedio_cuotas, 2),
                round(porcentaje_morosidad, 2)
            ))
            
            self.db_connection.connection.commit()
            
            # Guardar métricas para acceso posterior
            self.metricas_morosidad = {
                'fecha_actualizacion': fecha_actualizacion,
                'numero_estudiantes_total': int(numero_estudiantes_total),
                'numero_estudiantes_con_deuda': int(numero_estudiantes_con_deuda),
                'porcentaje_estudiantes_con_deuda': float(round(porcentaje_con_deuda, 2)),
                'monto_total_adeudado': int(monto_total_adeudado),
                'monto_total_compromisos': int(monto_total_compromisos),
                'promedio_cuotas_pendientes': float(round(promedio_cuotas, 2)),
                'porcentaje_morosidad': float(round(porcentaje_morosidad, 2))
            }
            
        except Exception as e:
            print(f"✗ Error al calcular resumen de morosidad: {str(e)}")
            raise
