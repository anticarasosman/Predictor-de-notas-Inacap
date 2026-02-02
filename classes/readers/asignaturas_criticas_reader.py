from operator import index
import pandas as pd
from classes.readers.reader import Reader


class AsignaturaCriticasReader(Reader):
    
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.df = pd.read_csv(self.file_path, delimiter=';', skiprows=5, encoding='utf-8')

    def _process_and_upsert(self):
        cursor = self.db_connection.cursor()
        
        try:
            for index, row in self.df.iterrows():
                codigo_asignatura = row['CODIGO ASIGNATURA']
                periodo = row['PERIODO']
                
                self._insert_semestre(cursor, periodo)

                datos_asignatura_semestre = {
                    "codigo_asignatura": codigo_asignatura,
                    "periodo_semestre": periodo,
                    "secciones": int(row["SECCIONES"]) if row["SECCIONES"] else None,
                    "alumnos": int(row["ALUMNOS"]) if row["ALUMNOS"] else None,
                    "alumnos_en_riesgo": int(row["ALUMNOS EN RIESGO"]) if row["ALUMNOS EN RIESGO"] else None,
                    "alumnos_ayudantia": int(row["ALUMNOS AYUDANTIA"]) if row["ALUMNOS AYUDANTIA"] else None,
                    "porcentaje_reprobacion_N1": float(row["PORCENTAJE REPROBACION N1"]) if row["PORCENTAJE REPROBACION N1"] else None,
                    "porcentaje_reprobacion_N2": float(row["PORCENTAJE REPROBACION N2"]) if row["PORCENTAJE REPROBACION N2"] else None,
                    "porcentaje_reprobacion_N3": float(row["PORCENTAJE REPROBACION N3"]) if row["PORCENTAJE REPROBACION N3"] else None,

                    "promedio_nota_uno": float(row["PROMEDIO NOTA UNO"]) if row["PROMEDIO NOTA UNO"] else None,
                    "promedio_nota_dos": float(row["PROMEDIO NOTA DOS"]) if row["PROMEDIO NOTA DOS"] else None,
                    "promedio_nota_tres": float(row["PROMEDIO NOTA TRES"]) if row["PROMEDIO NOTA TRES"] else None,

                    "ayudantia_virtual": True if row["AYUDANTIA VIRTUAL"] == "SI" else False,
                    "ayudantia_sede": True if row["AYUDANTIA SEDE"] == "SI" else False
                }
                
                datos_asignatura = {
                    'nombre': row['ASIGNATURA'],
                    "programa": row['PROGRAMA'],
                    "area": row['AREA'],
                    "COD_mencion": row['COD MENCION'],
                    "mencion": row['MENCION'].upper(),
                    "plan": row['PLAN'],
                    "modalidad": row['JORNADA'],
                    "nivel": int(row['NIVEL']) if row['NIVEL'] else None,
                    "prerequisito_semestre_siguiente": int(row['PREREQUISITO SEMESTRE SIGUIENTE']) if row['PREREQUISITO SEMESTRE SIGUIENTE'] else None,
                    "ultimo_nivel": int(row['ULTIMO NIVEL']) if row['ULTIMO NIVEL'] else None
                }
                
                if self._asignatura_exists(codigo_asignatura):
                    self._update_asignatura(cursor, codigo_asignatura, datos_asignatura)
                else:
                    self._insert_asignatura(cursor, codigo_asignatura, datos_asignatura)

                if self._asignatura_semestre_exists(cursor, codigo_asignatura, periodo):
                    self._update_asignatura_semestre(cursor, codigo_asignatura, periodo, datos_asignatura_semestre)
                else:
                    self._insert_asignatura_semestre(cursor, codigo_asignatura, periodo, datos_asignatura_semestre)
                    
        finally:
            cursor.close()