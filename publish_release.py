"""Idempotent GitHub CLI release publication; credentials stay in the environment."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
ASSETS = ('dev-forge.zip', 'DevForge.exe', 'dev-forge-windows-x64.zip', 'dev-forge-linux-x64.zip', 'dev-forge-linux-x64.tar.gz')

def release_notes(changelog, version):
    match = re.search(r'^## ' + re.escape(version) + r'\s.*?\n(.*?)(?=^## |\Z)', changelog, re.M | re.S)
    if not match:
        raise ValueError('Changelog sem a versao atual.')
    return match.group(1).strip() + '\n'

def publish(tag, directory, repository):
    metadata = json.loads((BASE / 'version.json').read_text(encoding='utf-8'))
    if tag != 'v' + metadata['version']:
        raise ValueError('Tag e version.json precisam coincidir.')
    directory = Path(directory).resolve()
    files = [directory / name for name in ASSETS]
    for path in files:
        if not path.is_file():
            raise ValueError('Asset faltando: ' + path.name)
    notes = directory / 'release-notes.md'
    notes.write_text(release_notes((BASE / 'CHANGELOG.md').read_text(encoding='utf-8'), metadata['version']), encoding='utf-8')
    checksums = directory / 'SHA256SUMS.txt'
    checksums.write_text(''.join(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + path.name + '\n' for path in files), encoding='utf-8')
    def gh(*args, check=True):
        return subprocess.run(['gh', *args, '--repo', repository], check=check)
    exists = gh('release', 'view', tag, check=False).returncode == 0
    if not exists:
        gh('release', 'create', tag, '--draft', '--title', 'Dev Forge ' + tag, '--notes-file', str(notes), '--verify-tag')
    gh('release', 'upload', tag, *[str(path) for path in files], str(checksums), '--clobber')
    gh('release', 'edit', tag, '--title', 'Dev Forge ' + tag, '--notes-file', str(notes), '--draft=false', '--prerelease=false', '--latest')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', required=True)
    parser.add_argument('--assets', required=True)
    parser.add_argument('--repo', required=True)
    args = parser.parse_args()
    publish(args.tag, args.assets, args.repo)
