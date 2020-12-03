# -*- mode: python ; coding: utf-8 -*-
import os
block_cipher = None

from autoUpdate import APP_NAME


def get_resources():
    data_files = []

    data_files.append((os.path.join('smartbond_tool','smartbond_tool','flash_database.json'),os.path.join('smartbond_tool','smartbond_tool')))
    for r, d, f in os.walk(os.path.join('assets')):
        for file in f:
            data_files.append((os.path.join(r, file),r))

    for r, d, f in os.walk(os.path.join('frontend','dist','frontend')):
        for file in f:
            data_files.append((os.path.join(r, file),r))

    for r, d, f in os.walk(os.path.join('smartbond_tool','lib')):
        for file in f:
            data_files.append((os.path.join(r, file),'.'))

    return(data_files)

a = Analysis(['main.py'],
             pathex=['.',os.path.join('smartbond_tool','smartbond_tool')],
             binaries=[],
             datas=get_resources(),
             hiddenimports=['engineio.async_drivers.threading'],
             hookspath=['.venv/lib/python3.7/site-packages/pyupdater/hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if os.name in 'nt':
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            [],
            name=APP_NAME,
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
                console=False , icon=os.path.join('assets','link.ico'))
else:
    exe = EXE(pyz,
            a.scripts,
                [],
                exclude_binaries=True,
                name=APP_NAME,
                debug=False,
                bootloader_ignore_signals=False,
                strip=False,
                upx=True,
                console=False )
    coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
                name='main')
    app = BUNDLE(coll,
                name='{}.app'.format(APP_NAME),
                icon='assets/link.icns',
                bundle_identifier='org.ezflash.{}'.format(APP_NAME))
