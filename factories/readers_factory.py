from classes.readers.excel_reader.asignaturas_criticas_reader import AsignaturaCriticasReader
from classes.readers.excel_reader.reporte_morosidad_reader import ReporteMorosidadReader
from classes.readers.excel_reader.seguimiento_de_alumnos_reader import SeguimientoDeAlumnosReader
from classes.readers.excel_reader.situacion_academica_reader import SituacionAcademicaReader
from classes.readers.pdf_reader.pdf_reader import PDFReader
from classes.readers.pdf_reader.certificado_anual_reader import CertificadoAnualReader
from classes.readers.pdf_reader.certificado_de_concentracion_reader import CertificadoDeConcentracionReader
from pdfminer.high_level import extract_text


class ReadersFactory:
    """Factory para crear instancias de readers según el tipo de archivo"""
    
    @staticmethod
    def create_reader(file_type: str, file_path: str, db_connection):
        # Para PDFs, detectar automáticamente el tipo
        if file_type == 'certificado_pdf':
            return ReadersFactory._create_pdf_reader(file_path, db_connection)
        
        # Readers CSV
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
    def _create_pdf_reader(file_path: str, db_connection):
        try:
            # Extraer texto del PDF
            texto = extract_text(file_path)
            texto_upper = texto.upper()
            
            # Identificar tipo de certificado
            if "ANUAL" in texto_upper:
                return CertificadoAnualReader(file_path, db_connection)
            elif "CONCENTRACION" in texto_upper or "CONCENTRACIÓN" in texto_upper:
                return CertificadoDeConcentracionReader(file_path, db_connection)
            else:
                raise ValueError(f"Tipo de certificado PDF no reconocido en: {file_path}")
        except Exception as e:
            raise ValueError(f"Error al identificar certificado PDF: {str(e)}")
    
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
            },
            'certificado_pdf': {
                'name': 'Certificados Enseñanza Media (PDF)',
                'extensions': [('.pdf', 'Archivos PDF (*.pdf)')]
            }
        }
