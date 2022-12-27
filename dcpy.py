"""
Contains the python functions that I use a lot in general
"""

import os


def clear():
    """Clears the screen of the terminal"""
    clear_command = "clear"
    if os.name == "nt":
        clear_command = "cls"
    os.system(clear_command)
