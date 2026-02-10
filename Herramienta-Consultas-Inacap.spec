# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs


tcl_datas = collect_data_files('tkinter')
tcl_datas += collect_data_files('tcl')
tcl_datas += collect_data_files('tk')
tcl_binaries = collect_dynamic_libs('tkinter')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=tcl_binaries,
    datas=tcl_datas,
    hiddenimports=['database', 'frontend', 'classes', 'utils', 'factories', 'openpyxl', 'mysql.connector', 'pandas'],
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
    console=False,
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
