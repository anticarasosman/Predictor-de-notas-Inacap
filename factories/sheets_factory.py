from classes.sheets.custom_sheet import CustomSheet
from classes.sheets.general_info_sheet import GeneralInfoSheet
from classes.sheets.academic_info_sheet import AcademicInfoSheet
from classes.sheets.financial_info_sheet import FinancialInfoSheet
from utils.custom_sheet_manager import load_custom_sheet_config

class SheetsFactory():
    
    def create_sheets(self, workbook, student_data: dict, sheet_selection: dict, custom_sheet_selection: dict, db_connection=None) -> dict:
        
        sheets = {
            "general_info": GeneralInfoSheet() if sheet_selection.get('general') else None,
            "academic_info": AcademicInfoSheet() if sheet_selection.get('academic') else None,
            "financial_info": FinancialInfoSheet() if sheet_selection.get('financial') else None
        }

        for sheet_name, is_selected in custom_sheet_selection.items():
            if is_selected:
                config = load_custom_sheet_config(sheet_name)
                # Crear CustomSheet y guardar referencia a db_connection
                custom_sheet = CustomSheet(config)
                custom_sheet.db_connection = db_connection
                sheets[sheet_name] = custom_sheet

        return sheets