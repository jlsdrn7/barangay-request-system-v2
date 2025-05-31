# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
from glob import glob
import os

block_cipher = None

# Include ALL files in assets folder
asset_files = [(f, os.path.join("assets", os.path.basename(f))) for f in glob("assets/*")]

# Include database file
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BarangayRequestApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon='assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='BarangayRequestApp',
)
