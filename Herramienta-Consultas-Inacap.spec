# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import pathlib
import subprocess
import sys

# Encontrar la instalación real de Python (no el venv)
try:
    result = subprocess.run(
        [sys.executable, '-c', 'import sys; print(sys.base_prefix)'],
        capture_output=True,
        text=True
    )
    python_real = pathlib.Path(result.stdout.strip())
except:
    python_real = pathlib.Path("C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.13_3.13.3312.0_x64__qbz5n2kfra8p0")

tcl_root = python_real / 'tcl'

print(f"[DEBUG SPEC] Python real: {python_real}")
print(f"[DEBUG SPEC] TCL exists: {tcl_root.exists()}")

# Preparar datos - incluir la carpeta tcl COMPLETA (contiene tcl + tk)
tcl_datas = []

if tcl_root.exists():
    # Copiar el contenido de la carpeta tcl directamente a _internal
    # Esto pone tcl8.6, tk8.6, etc. directamente en _internal, no en _internal/tcl
    for item in tcl_root.iterdir():
        if item.is_dir():
            tcl_datas.append((str(item), item.name))
            print(f"[DEBUG SPEC] [OK] Agregando {item.name}")
    print(f"[DEBUG SPEC] [OK] Copiando contenido de TCL completo")

# Agregar datos de MySQL connector (archivos de error/localización)
mysql_datas = []
try:
    mysql_files = collect_data_files('mysql.connector')
    if mysql_files:
        mysql_datas.extend(mysql_files)
        print(f"[DEBUG SPEC] [OK] Agregados datos de mysql.connector: {len(mysql_files)} items")
except Exception as e:
    print(f"[DEBUG SPEC] [WARN] Error recopilando mysql.connector: {e}")

# Agregar explícitamente la carpeta locales de mysql.connector
try:
    import mysql.connector as _mysql_connector
    mysql_path = pathlib.Path(_mysql_connector.__file__).parent
    mysql_locales = mysql_path / 'locales'
    if mysql_locales.exists():
        mysql_datas.append((str(mysql_locales), 'mysql/connector/locales'))
        print(f"[DEBUG SPEC] [OK] Agregada carpeta locales: {mysql_locales}")
    else:
        print(f"[DEBUG SPEC] [WARN] Carpeta locales no encontrada: {mysql_locales}")
except Exception as e:
    print(f"[DEBUG SPEC] [WARN] Error agregando locales: {e}")

# Combinar todos los datos
all_datas = tcl_datas + mysql_datas

# Recopilar binarios de Tkinter
tcl_binaries = collect_dynamic_libs('tkinter')

print(f"[DEBUG SPEC] Total TCL datas: {len(tcl_datas)}")
print(f"[DEBUG SPEC] Total MySQL datas: {len(mysql_datas)}")
print(f"[DEBUG SPEC] Total combinado: {len(all_datas)}")
print(f"[DEBUG SPEC] Total binaries: {len(tcl_binaries)}")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=tcl_binaries,
    datas=all_datas,
    hiddenimports=[
        'database', 
        'frontend', 'classes', 
        'utils', 
        'factories', 
        'openpyxl', 
        'mysql.connector', 
        'mysql.connector.locales',
        'mysql.connector.locales.eng',  # Localización en inglés
        'mysql.connector.errors',
        'pandas',
        'setup_tkinter',
    ],
    hookspath=['.'],  # Usar hooks personalizados de esta carpeta
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Herramienta-Consultas-Inacap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # CON CONSOLA - para debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Herramienta-Consultas-Inacap',
)
