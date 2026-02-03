from pdfminer.high_level import extract_text
from classes.readers.reader import Reader


class PDFReader(Reader):
    def __init__(self, file_path, db_connection):
        super().__init__(file_path, db_connection)

    def get_total_rows(self) -> int:
        """Retorna 1 porque cada PDF contiene un estudiante"""
        return 1

    def extract_text(self) -> str:
        return extract_text(self.file_path)

    def _identify_certificate_type(self, text: str) -> str:
        text_upper = text.upper()
        if "CERTIFICADO ANUAL DE ESTUDIOS" in text_upper:
            return "anual"
        if "CERTIFICADO DE CONCENTRACION DE NOTAS" in text_upper:
            return "concentracion"
        return "desconocido"

    def _normalize_rut(self, rut: str) -> str:
        if not rut:
            return rut
        return rut.replace(".", "").strip()

    def _process_and_upsert(self, progress_callback=None):
        raise NotImplementedError("Debe implementar _process_and_upsert en el reader específico")