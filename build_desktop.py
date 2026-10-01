"""Build native x64 portable downloads on each target operating system."""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent

def build(output, console=False, work_root=None, build_only=False):
    if platform.machine().lower() not in ('amd64','x86_64'):
        raise RuntimeError('Builds desta release exigem arquitetura x64.')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    kind = 'windows' if os.name == 'nt' else 'linux'
    executable_name = 'DevForge.exe' if kind == 'windows' else 'DevForge'
    metadata = json.loads((BASE / 'version.json').read_text(encoding='utf-8'))
    if work_root is not None:
        work_root = Path(work_root).resolve()
        work_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='dev-forge-build-', dir=work_root, ignore_cleanup_errors=True) as temp:
        temp = Path(temp)
        command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onefile', '--console' if console else '--windowed', '--name', 'DevForge', '--distpath', str(temp / 'dist'), '--workpath', str(temp / 'work'), '--specpath', str(temp), '--paths', str(BASE)]
        for name in ('version.json', 'CHANGELOG.md', 'assets'):
            command += ['--add-data', str(BASE / name) + os.pathsep + ('.' if name != 'assets' else 'assets')]
        if kind == 'windows':
            command += ['--icon', str(BASE / 'assets' / 'dev-forge.ico')]
            components = tuple(int(n) for n in metadata['version'].split('.')) + (0,)
            resource = "VSVersionInfo(ffi=FixedFileInfo(filevers=" + repr(components) + ",prodvers=" + repr(components) + ",mask=0x3f,flags=0x0,OS=0x40004,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','Dev Forge'),StringStruct('FileDescription','Dev Forge'),StringStruct('FileVersion','" + metadata['version'] + "'),StringStruct('ProductName','Dev Forge'),StringStruct('ProductVersion','" + metadata['version'] + "')])]),VarFileInfo([VarStruct('Translation',[1033,1200])])])"
            version_file = temp / 'version-resource.txt'
            version_file.write_text(resource, encoding='utf-8')
            command += ['--version-file', str(version_file)]
        command.append(str(BASE / 'desktop_entry.py'))
        build_environment = dict(os.environ, PYINSTALLER_CONFIG_DIR=str(temp / 'cache'), PYTHONUSERBASE=str(temp / 'user-site'), PYTHONNOUSERSITE='1')
        subprocess.run(command, check=True, cwd=str(BASE), env=build_environment)
        binary = temp / 'dist' / executable_name
        if not binary.exists():
            raise RuntimeError('Executavel nao foi gerado.')
        if not build_only:
            # Confirm bundled Tcl/Tk, metadata, icon and application imports work.
            check_path = temp / 'smoke.json'
            smoke = [str(binary), '--self-test', str(check_path)]
            if kind == 'linux' and not os.environ.get('DISPLAY'):
                smoke = ['xvfb-run', '-a'] + smoke
            smoke_environment = dict(os.environ, TEMP=str(temp), TMP=str(temp), TMPDIR=str(temp))
            process = subprocess.Popen(smoke, cwd=str(temp), env=smoke_environment)
            try:
                return_code = process.wait(timeout=60)
            except subprocess.TimeoutExpired:
                if os.name == 'nt':
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],check=False,capture_output=True)
                else:
                    process.kill()
                process.wait()
                raise RuntimeError('Teste do executavel nao concluiu em 60 segundos.')
            if return_code != 0:
                detail = check_path.read_text(encoding='utf-8') if check_path.exists() else 'Sem diagnostico de inicializacao.'
                raise RuntimeError('Teste do executavel falhou: ' + detail)
            result = json.loads(check_path.read_text(encoding='utf-8'))
            if not result['ok'] or not result['packaged'] or result['version'] != metadata['version']:
                raise RuntimeError('Teste do executavel falhou.')
        staging = temp / 'dev-forge'
        staging.mkdir()
        shutil.copy2(binary, staging / executable_name)
        for name in ('version.json', 'CHANGELOG.md', 'README.md', 'LICENSE'):
            shutil.copy2(BASE / name, staging / name)
        (staging / 'assets').mkdir()
        for name in ('dev-forge.png', 'dev-forge.ico', 'interface.svg'):
            shutil.copy2(BASE / 'assets' / name, staging / 'assets' / name)
        archive_path = output / f'dev-forge-{kind}-x64.zip'
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(staging.rglob('*')):
                if file.is_file():
                    archive.write(file, 'dev-forge/' + file.relative_to(staging).as_posix())
        if kind == 'windows':
            shutil.copy2(binary, output / 'DevForge.exe')
        else:
            with tarfile.open(output / 'dev-forge-linux-x64.tar.gz', 'w:gz') as archive:
                archive.add(staging, arcname='dev-forge')
    print(f'Build {kind} {metadata["version"]}: ' + ('arquivos gerados; teste de inicializacao nao executado.' if build_only else 'executavel e pacote verificados.'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='dist')
    parser.add_argument('--debug-console',action='store_true')
    parser.add_argument('--work-root')
    parser.add_argument('--build-only',action='store_true',help='Generate artifacts without claiming startup validation; CI does not use this option.')
    args = parser.parse_args()
    build(args.output,args.debug_console,args.work_root,args.build_only)
