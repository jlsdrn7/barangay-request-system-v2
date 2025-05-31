# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
from glob import glob
import os

block_cipher = None

# Collect all files inside the 'assets' folder (including .png and .ico)
asset_files = [(f, os.path.join("assets", os.path.basename(f))) for f in glob("assets/*")]
asset_files.append(('barangay.db', 'barangay.db'))

a = Analysis(
    ['app_entry.py'],
    pathex=[],
    binaries=[],
    datas=asset_files,
    hiddenimports=collect_submodules('ttkbootstrap'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BarangayRequestApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon='assets/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='BarangayRequestApp'
)
