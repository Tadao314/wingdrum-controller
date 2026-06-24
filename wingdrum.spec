# -*- mode: python ; coding: utf-8 -*-
# WingDrum Controller — PyInstaller spec
# Windows / macOS 両対応

import sys
from pathlib import Path

block_cipher = None

# 同梱するデータファイル（exe内に埋め込む）
added_files = [
    ('index.html', '.'),
    ('wd_bk.png',  '.'),
    ('wd_wh.png',  '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'serial',
        'serial.tools',
        'serial.tools.list_ports',
        'webview',
        'webview.platforms',
        # Windows用
        'webview.platforms.winforms',
        'webview.platforms.mshtml',
        'webview.platforms.edgechromium',
        # Mac用
        'webview.platforms.cocoa',
        # Linux用（念のため）
        'webview.platforms.gtk',
        'webview.platforms.qt',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WingDrumController',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # コンソールウィンドウを出さない
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='wingdrum.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WingDrumController',
)

# macOS用 .app バンドル
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='WingDrumController.app',
        bundle_identifier='com.phonicbloom.wingdrum-controller',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '1.0.0',
        },
    )
