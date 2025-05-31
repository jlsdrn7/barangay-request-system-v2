# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
import os
from glob import glob

block_cipher = None

# Collect every file inside assets folder (PNG, ICO, JPG, etc.)
asset_files = []
for filepath in glob("assets/*"):
    asset_files.append((filepath, os.path.join("assets", os.path.basename(filepath))))

# Add the database
asset_files.append(("barangay.db", "barangay.db"))

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
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BarangayRequestApp',
)