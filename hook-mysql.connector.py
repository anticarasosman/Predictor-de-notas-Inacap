# PyInstaller hook para mysql.connector
# Incluye los archivos de locales necesarios para evitar "No localization support for language 'eng'"

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Recolectar todos los archivos de datos de mysql.connector, incluyendo locales/
datas = collect_data_files('mysql.connector', include_py_files=True)

# Asegurar que todos los submódulos de locales estén incluidos
hiddenimports = collect_submodules('mysql.connector.locales')
