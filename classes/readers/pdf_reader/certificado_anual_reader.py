import re
from classes.readers.pdf_reader.pdf_reader import PDFReader


class CertificadoAnualReader(PDFReader):
    def __init__(self, file_path: str, db_connection):
        super().__init__(file_path, db_connection)

        self.nombre_estudiante = ""
        self.rut_estudiante = ""
        self.asignaturas = []
        self.calificaciones = []

        self.categorias = {
            "Lenguaje": [
                "Lengua Castellana Y Comunicación",
                "Lengua Y Literatura",
                "Lengua y Comunicación",
                "Castellano",
            ],
            "Matematica": ["Educación Matemática", "Matemática"],
            "Ingles": [
                "Idioma Extranjero: Inglés",
                "Idioma Extranjero (inglés)",
                "Idioma Extranjero",
                "Inglés",
            ],
        }

    def _process_and_upsert(self, progress_callback=None):
        text = self.extract_text()
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        capturando_calificaciones = False

        for i, line in enumerate(lines):
            next_line = lines[i + 1] if i + 1 < len(lines) else ""

            if "don(ña)" in line:
                nombre_base = re.search(r"don\(ña\)\s+([A-Za-zÁÉÍÓÚáéíóúÑñ\s]+)", line)
                if nombre_base:
                    self.nombre_estudiante = nombre_base.group(1).strip()
                    apellido_match = re.search(r"^[A-ZÁÉÍÓÚÜÑ]+(?:\s+[A-ZÁÉÍÓÚÜÑ]+)*", next_line)
                    if apellido_match:
                        self.nombre_estudiante += " " + apellido_match.group(0).strip()

            if "RUN" in line:
                rut_match = re.search(r"RUN[:\s]+([\d\.]+-[\dkK])", line)
                if rut_match:
                    self.rut_estudiante = self._normalize_rut(rut_match.group(1))

            if capturando_calificaciones:
                if not line:
                    continue
                numeros = re.findall(r"\d\.\d", line)
                if numeros:
                    self.calificaciones.extend(numeros)
                elif re.search(r"^\w+,\w+$", line):
                    continue
                else:
                    self.asignaturas.append(line)

            if "Asignatura" in line:
                capturando_calificaciones = True

        self.asignaturas = self.asignaturas[: len(self.calificaciones)]

        notas_por_categoria = {"Matematica": [], "Lenguaje": [], "Ingles": []}
        for asignatura, calificacion in zip(self.asignaturas, self.calificaciones):
            nota = self._safe_float(calificacion)
            categoria = self._categorizar_asignatura(asignatura)
            if categoria and nota is not None:
                notas_por_categoria[categoria].append(nota)

        promedio_mate = self._promedio(notas_por_categoria["Matematica"])
        promedio_leng = self._promedio(notas_por_categoria["Lenguaje"])
        promedio_ing = self._promedio(notas_por_categoria["Ingles"])

        if not self.rut_estudiante:
            raise ValueError("No se pudo detectar el RUT en el certificado anual")

        datos_estudiante = {
            "rut": self.rut_estudiante,
            "nombre": self.nombre_estudiante or None,
            "promedio_media_matematica": promedio_mate,
            "promedio_media_lenguaje": promedio_leng,
            "promedio_media_ingles": promedio_ing,
        }

        cursor = self.db_connection.cursor()
        try:
            if self._estudiante_exists(cursor, self.rut_estudiante):
                self._update_estudiante(cursor, self.rut_estudiante, datos_estudiante)
            else:
                self._insert_estudiante(cursor, self.rut_estudiante, datos_estudiante)

            if progress_callback:
                progress_callback(1)
        finally:
            cursor.close()

    def _categorizar_asignatura(self, asignatura: str):
        if not asignatura:
            return None
        asignatura_norm = asignatura.strip().lower()
        for categoria, nombres in self.categorias.items():
            for nombre in nombres:
                if nombre.lower() in asignatura_norm:
                    return categoria
        return None

    def _safe_float(self, value: str):
        try:
            return float(str(value).strip())
        except (ValueError, TypeError):
            return None

    def _promedio(self, valores):
        if not valores:
            return None
        return round(sum(valores) / len(valores), 1)