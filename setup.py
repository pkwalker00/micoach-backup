from distutils.core import setup
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func) 
    
setup (name='micoach-backup', 
            version='1.0', 
            description='Simple Utility to backup miCoach Workouts', 
            author='Patrick Walker', 
            url='https://github.com/pkwalker00/micoach-backup', 
            license='BSD',  
            scripts=['micoach-backup.py'], 
            packages=['libmicoach'], 
            requires=['lxml(>=3.0)', 'pygobject'])
