"""Create a user-requested launcher, without requiring administrator access."""
import os
import subprocess
from pathlib import Path
from runtime import current_launch_command, RESOURCES, data_directory

def powershell_literal(value):
    return "'" + str(value).replace("'", "''") + "'"

def desktop_argument(value):
    value = str(value)
    if '\n' in value or '\r' in value:
        raise ValueError('Caminho invalido para atalho.')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$') + '"'

def create_shortcut():
    command = current_launch_command()
    icon = data_directory() / 'dev-forge.ico'
    icon.parent.mkdir(parents=True, exist_ok=True)
    if os.name == 'nt':
        icon.write_bytes((RESOURCES / 'assets' / 'dev-forge.ico').read_bytes())
        arguments = ' '.join('"' + arg + '"' for arg in command[1:])
        script = "$ErrorActionPreference='Stop'; $shell=New-Object -ComObject WScript.Shell; $path=Join-Path $shell.SpecialFolders.Item('Desktop') 'Dev Forge.lnk'; $shortcut=$shell.CreateShortcut($path); "
        script += '$shortcut.TargetPath=' + powershell_literal(command[0]) + '; '
        script += '$shortcut.Arguments=' + powershell_literal(arguments) + '; '
        script += '$shortcut.WorkingDirectory=' + powershell_literal(Path(command[0]).parent) + '; '
        script += '$shortcut.IconLocation=' + powershell_literal(str(icon) + ',0') + '; $shortcut.Save()'
        subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],check=True,capture_output=True)
    else:
        png = data_directory() / 'dev-forge.png'
        png.write_bytes((RESOURCES / 'assets' / 'dev-forge.png').read_bytes())
        applications = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')) / 'applications'
        applications.mkdir(parents=True, exist_ok=True)
        content = '[Desktop Entry]\nType=Application\nName=Dev Forge\nComment=Prepare seu ambiente de desenvolvimento\nTerminal=false\nCategories=Development;Utility;\n'
        content += 'Exec=' + ' '.join(desktop_argument(arg) for arg in command) + '\nIcon=' + str(png) + '\n'
        (applications / 'dev-forge.desktop').write_text(content,encoding='utf-8')
