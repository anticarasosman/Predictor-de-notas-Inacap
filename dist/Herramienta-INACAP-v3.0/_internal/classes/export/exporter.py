import pandas as pd
from openpyxl import Workbook
from factories.sheets_factory import SheetsFactory
import os
import subprocess
from datetime import datetime
from pathlib import Path

class Exporter:

    def __init__(self, db_connection, sheet_selection: dict, custom_sheet_selection: dict):
        self.db_connection = db_connection
        self.sheet_factory = SheetsFactory()
        self.sheet_selection = sheet_selection
        self.custom_sheet_selection = custom_sheet_selection
    
    def export_student_by_rut(self, rut: str, output_dir: Path) -> str:
        student_data = self._get_student_data(rut)
        
        if not student_data:
            raise ValueError(f"Estudiante con RUT {rut} no encontrado en la base de datos")
        
        file_path = self._create_excel(student_data, output_dir, rut)
        
        return file_path
    
    def _get_student_data(self, rut: str) -> dict:
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # 1. Datos generales del estudiante
            query = "SELECT * FROM Estudiante WHERE rut = %s"
            cursor.execute(query, (rut,))
            student = cursor.fetchone()

            if not student:
                return None
            
            # 2. Semestres del estudiante
            query = """
                SELECT * FROM Estudiante_Semestre
                WHERE rut_estudiante = %s
                ORDER BY periodo_semestre DESC
            """
            cursor.execute(query, (rut,))
            semesters = cursor.fetchall()

            # 3. Cursos por semestre
            semesters_with_subjects = []
            for semester in semesters:
                query = """
                    SELECT * FROM Estudiante_Asignatura
                    WHERE rut_estudiante = %s AND periodo_semestre = %s
                    ORDER BY codigo_asignatura
                """
                cursor.execute(query, (rut, semester['periodo_semestre']))
                subjects = cursor.fetchall()
                semesters_with_subjects.append({
                    'semester': semester,
                    'subjects': subjects
                })

            # 4. Informacion financiera
            query = "SELECT * FROM Reporte_financiero_estudiante WHERE rut_estudiante = %s"
            cursor.execute(query, (rut,))
            financial_info = cursor.fetchone()

            return {
                "student": student,
                "semesters": semesters_with_subjects,
                "financial_info": financial_info
            }
        
        finally:
            cursor.close()
    
    def _create_excel(self, student_data: dict, output_dir: Path, rut: str) -> str:
        wb = Workbook()
        wb.remove(wb.active)

        # Pasar db_connection a la factory
        sheets = self.sheet_factory.create_sheets(wb, student_data, self.sheet_selection, self.custom_sheet_selection, self.db_connection)
        
        for sheet in sheets.values():
            if sheet:
                # Pasar db_connection al método add_sheet si es necesario
                if hasattr(sheet, 'db_connection'):
                    sheet.add_sheet(wb, student_data, self.db_connection)
                else:
                    sheet.add_sheet(wb, student_data)
        
        # Guardar archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Estudiante_{rut}_{timestamp}.xlsx"
        file_path = output_dir / filename
        wb.save(file_path)
        subprocess.Popen(f'explorer /select,"{file_path}"')
        return str(file_path)