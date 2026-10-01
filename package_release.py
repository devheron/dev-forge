"""Build an allowlisted source release without local settings or logs."""
import json
import zipfile
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
FILES = ('app.py', 'desktop_entry.py', 'ui.py', 'runtime.py', 'shortcuts.py', 'catalog.py', 'engine.py', 'updater.py', 'version.json', 'README.md', 'CHANGELOG.md', 'VALIDATION.md', 'LICENSE', 'start-windows.cmd', 'start-linux.sh', 'package_release.py', 'build_desktop.py', 'publish_release.py', 'prepare_release.py', 'requirements-build.txt')

def build(destination):
    metadata = json.loads((BASE / 'version.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            archive.write(BASE / name, f'dev-forge/{name}')
        for name in ('tests', '.github', 'assets'):
            for path in sorted((BASE / name).rglob('*')):
                if path.is_file() and '__pycache__' not in path.parts:
                    archive.write(path, 'dev-forge/' + path.relative_to(BASE).as_posix())
        archive.write(BASE / '.gitignore', 'dev-forge/.gitignore')
    return metadata['version']

if __name__ == '__main__':
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else 'dev-forge.zip').resolve()
    print(f'Release {build(destination)}: {destination.name}')
