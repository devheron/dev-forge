"""Resource, preferences and launch paths for source and packaged applications."""
import os
import sys
from pathlib import Path

RESOURCES = Path(__file__).resolve().parent

def is_packaged():
    return bool(getattr(sys, 'frozen', False))

def data_directory():
    if not is_packaged():
        return RESOURCES
    if os.name == 'nt':
        return Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'DevForge'
    return Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')) / 'dev-forge'

def update_directory():
    path = data_directory() / 'updates' if is_packaged() else RESOURCES.parent
    path.mkdir(parents=True, exist_ok=True)
    return path

def current_launch_command():
    if is_packaged():
        return [sys.executable]
    interpreter = Path(sys.executable)
    if os.name == 'nt' and interpreter.with_name('pythonw.exe').exists():
        interpreter = interpreter.with_name('pythonw.exe')
    return [str(interpreter), str(RESOURCES / 'app.py')]

def updated_launch_command(directory, kind):
    if kind == 'windows':
        return [str(directory / 'DevForge.exe')]
    if kind == 'linux':
        return [str(directory / 'DevForge')]
    if kind == 'source' and not is_packaged():
        return [sys.executable, str(directory / 'app.py')]
    raise ValueError('Formato de atualizacao incompativel.')
