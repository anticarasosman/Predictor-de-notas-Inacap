from classes.readers.asignaturas_criticas_reader import AsignaturaCriticasReader
from classes.readers.reporte_morosidad_reader import ReporteMorosidadReader
from classes.readers.seguimiento_de_alumnos_reader import SeguimientoDeAlumnosReader
from classes.readers.situacion_academica_reader import SituacionAcademicaReader


class ReadersFactory:
    """Factory para crear instancias de readers según el tipo de archivo"""
    
    @staticmethod
    def create_reader(file_type: str, file_path: str, db_connection):
        """
        Crea una instancia del reader correspondiente
        
        Args:
            file_type: Tipo de archivo ('asignaturas_criticas', 'reporte_morosidad', etc.)
            file_path: Ruta del archivo
            db_connection: Conexión a la base de datos
            
        Returns:
            Instancia del reader correspondiente
            
        Raises:
            ValueError: Si el tipo de archivo no es válido
        """
        readers = {
            'asignaturas_criticas': AsignaturaCriticasReader,
            'reporte_morosidad': ReporteMorosidadReader,
            'seguimiento_alumnos': SeguimientoDeAlumnosReader,
            'situacion_academica': SituacionAcademicaReader,
        }
        
        if file_type not in readers:
            raise ValueError(f"Tipo de archivo no válido: {file_type}")
        
        reader_class = readers[file_type]
        return reader_class(file_path, db_connection)
    
    @staticmethod
    def get_file_types():
        """Retorna un diccionario con los tipos de archivo disponibles"""
        return {
            'asignaturas_criticas': {
                'name': 'Asignaturas Críticas',
                'extensions': [('.csv', 'Archivos CSV (*.csv)')]
            },
            'reporte_morosidad': {
                'name': 'Reporte Morosidad',
                'extensions': [('.csv', 'Archivos CSV (*.csv)')]
            },
            'seguimiento_alumnos': {
                'name': 'Seguimiento de Alumnos',
                'extensions': [('.csv', 'Archivos CSV (*.csv)')]
            },
            'situacion_academica': {
                'name': 'Situación Académica',
                'extensions': [('.csv', 'Archivos CSV (*.csv)')]
            }
        }
