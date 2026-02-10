"""
Hook personalizado de PyInstaller para mysql.connector
Asegura que se incluyan correctamente los archivos de localización y datos
"""

from PyInstaller.utils.hooks import collect_data_files, get_module_file_attribute
import os

# Recopilar datos completos de mysql.connector
datas = collect_data_files('mysql.connector')

# Asegurar que se incluyen las localizaciones
locales_dir = os.path.join(get_module_file_attribute('mysql.connector'), 'locales')
if os.path.exists(locales_dir):
    datas.append((locales_dir, 'mysql/connector/locales'))

hiddenimports = ['mysql.connector.locales.eng', 'mysql.connector.errors']
