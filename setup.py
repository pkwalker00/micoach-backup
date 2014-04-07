from cx_Freeze import setup,  Executable

import requests.certs,  sys

buildOptions = dict(include_files = [(requests.certs.where(), 'cacert.pem')], packages = ['lxml._elementpath', 'inspect'], excludes = [])
base = 'win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('micoach-backup.py', base=base)
    ]

setup(name='miCoach Backup', 
            version = '2.0', 
            description = 'A small program for backing up your workouts', 
            options = dict(build_exe = buildOptions), 
            executables = executables)
