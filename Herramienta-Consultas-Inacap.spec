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

tcl_binaries = collect_dynamic_libs('tkinter')

print(f"[DEBUG SPEC] Total datas: {len(tcl_datas)}")
print(f"[DEBUG SPEC] Total binaries: {len(tcl_binaries)}")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=tcl_binaries,
    datas=tcl_datas,
    hiddenimports=[
        'database', 
        'frontend', 'classes', 
        'utils', 
        'factories', 
        'openpyxl', 
        'mysql.connector', 
        'pandas',
        'setup_tkinter',
    ],
    hookspath=[],
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
    console=False,  # Sin consola - TCL ya está incluido
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
