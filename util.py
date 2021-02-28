import os
import sys


def resource_path(relative_path):
    """ Get absolute path to editable file in the same folder with the project or exe,
        works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
