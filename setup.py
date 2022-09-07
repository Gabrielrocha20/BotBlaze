import sys
import os
from cx_Freeze import setup, Executable

files = ['icone.ico', 'interface.py', 'bot_blaze.py', 'banco_de_padroes.db', 'chromedriver.exe']

target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icone.ico"
)

setup(
    name="BotDoubleCoffe",
    version="1.0",
    description="Bot de resultados Double",
    author="GabrielRocha, ValberJesus, MarcosVinicius",
    options={'build_exe': {'include_files': files}},
    executables=[target]
)