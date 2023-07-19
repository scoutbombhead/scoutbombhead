# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['updater_main.py'],
             pathex=['/home/sa/repo/updater_gui_ver3'],
             binaries=[],
             datas=[('./updater.ui', '.'),('./help_dialog.ui', '.'),('./settings_dialog.ui', '.'),('./Chord2.wav', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='updater_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
          
          
          
