import pandas as pd
from classes.readers.reader import Reader


class SituacionAcademicaReader(Reader):
    
    def _load_file(self) -> pd.DataFrame:
        """Carga archivo de Situación Académica"""
        pass
    
    def _clean_data(self) -> pd.DataFrame:
        """Limpia datos de Situación Académica"""
        pass
    
    def _process_and_upsert(self):
        """Procesa y hace UPSERT de Situación Académica"""
        pass
    
    # ========== MÉTODOS ESPECÍFICOS DE ESTE READER ==========
    
    def _combine_rut(self, rut: str, dv: str) -> str:
        """Combina RUT y DV"""
        pass
    
    def _convert_periodo(self, periodo_str: str) -> str:
        """Convierte formato de período"""
        pass
    
    def _extract_student_info(self, row) -> dict:
        """Extrae información del estudiante"""
        pass
