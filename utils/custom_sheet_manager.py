import os
import json

def save_custom_sheet_data(name, config):
    """
    Guarda la configuración de una sheet personalizada en JSON
    
    Args:
        name: Nombre de la sheet (se usará para el nombre del archivo)
        config: Dict con estructura {'name': 'Mi Sheet', 'tables': [...]}
    """
    # Crear carpeta si no existe
    os.makedirs("personalized_sheets", exist_ok=True)
    
    # Generar nombre del archivo (nombre_sheet.json)
    filename = f"personalized_sheets/{name}.json"
    
    # Guardar JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def load_custom_sheet_config(filename):
    """
    Carga la configuración de una sheet personalizada desde JSON
    
    Args:
        filename: Nombre del archivo (sin .json)
        
    Returns:
        dict: Configuración de la sheet
    """
    filepath = f"personalized_sheets/{filename}.json"
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    return config

def list_custom_sheets():
    """
    Retorna lista de nombres de sheets personalizadas disponibles
    
    Returns:
        list: ['mi_sheet', 'otra_sheet', ...]
    """
    sheets_dir = "personalized_sheets"
    
    # Crear carpeta si no existe
    os.makedirs(sheets_dir, exist_ok=True)
    
    # Obtener archivos .json
    sheets = []
    for filename in os.listdir(sheets_dir):
        if filename.endswith(".json"):
            # Remover extensión .json
            sheet_name = filename[:-5]
            sheets.append(sheet_name)
    
    return sorted(sheets)

def delete_custom_sheet(name):
    """
    Elimina una sheet personalizada
    
    Args:
        name: Nombre de la sheet a eliminar
        
    Returns:
        bool: True si se eliminó, False si no existe
    """
    filepath = f"personalized_sheets/{name}.json"
    
    if not os.path.exists(filepath):
        return False
    
    os.remove(filepath)
    return True