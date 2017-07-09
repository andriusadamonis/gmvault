# -*- mode: python -*-

block_cipher = None


a = Analysis(['../../src/gmv_runner.py'],
             pathex=['/home/gmv/Dev/gmvault'],
             binaries=None,
             datas=[('../../src/gmv/cacerts/cacert.pem', 'gmv/cacerts')], #use data to add cacerts.pem in data part
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gmvault',
          debug=False,
          strip=False,
          upx=True,
          console=True)
