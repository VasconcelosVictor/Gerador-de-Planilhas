# Gerador de planilhas
#
# By: Victor Vasconcelos
#
import cx_Freeze

executables = [cx_Freeze.Executable('model/main.py',base ='Win32GUI',targetName = 'gerador.exe', icon= 'Ui/pasta-.icon.ico')]

cx_Freeze.setup(
    name="gerarPlanilhas",
    options={'build_exe': {'packages': [ 'PyQt5', 'psycopg2' ],
                           'include_files': ['model', 'UI']}},

    executables=executables

)


