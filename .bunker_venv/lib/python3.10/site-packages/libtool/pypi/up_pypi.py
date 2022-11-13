import os
from os import path
base_cmd_text = """
python setup.py sdist bdist_wheel
@echo off
pause

@echo on

twine upload {opp} dist/*
@echo off
echo Press any key for exit . . .
pause>nul
exit
"""


def up(folder="..", opp=""):
    folder = folder + "/"
    ################
    cmd_path = "up_pypi.cmd"
    cmd_path = path.dirname(__file__)+cmd_path
    with open(cmd_path, "w") as cmd_io:
        text = base_cmd_text.format(folder=folder, opp=opp)
        cmd_io.write(text)
    os.system("start " + cmd_path)
