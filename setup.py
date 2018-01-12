from cx_Freeze import setup, Executable
import sys
import os

os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\Python\\Python35-32\\tcl\\tk8.6"

build_exe_options = {
	'excludes': ["pandas", 'PyQt5', 'scipy'],
	"packages": ["numpy", "matplotlib", 'tkinter'],
	"include_files": ["tcl86t.dll", "tk86t.dll"]
	}

base = 'Console'
if sys.platform == 'win32':
  base = 'Win32GUI'

setup(name='n-queen-GA-applied',
    version='1.0',
    description='creator: amidmajd@gmail.com',
    options = {"build_exe": build_exe_options},
    executables = [Executable('main.py', base=base)])
