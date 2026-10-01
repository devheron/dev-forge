"""Opt-in public GitHub release checks and verified side-by-side updates."""
import hashlib
import io
import json
import re
import stat
import tempfile
import zipfile
import os
import sys
import platform
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from runtime import RESOURCES, data_directory, is_packaged

BASE = RESOURCES
METADATA = json.loads((BASE / 'version.json').read_text(encoding='utf-8'))
MAX_DOWNLOAD = 256 * 1024 * 1024
MAX_EXTRACTED = 512 * 1024 * 1024

def distribution_kind():
    if not is_packaged():
        return 'source'
    if platform.machine().lower() not in ('amd64', 'x86_64'):
        raise ValueError('Atualizacao automatica disponivel apenas para x64.')
    return 'windows' if os.name == 'nt' else 'linux'

ASSETS = {'source': 'dev-forge.zip', 'windows': 'dev-forge-windows-x64.zip', 'linux': 'dev-forge-linux-x64.zip'}

def version_tuple(value):
    if not isinstance(value, str) or not re.fullmatch(r'v?\d+\.\d+\.\d+', value):
        raise ValueError('Versao de release invalida.')
    return tuple(int(x) for x in value.removeprefix('v').split('.'))

def validate_repository(repository):
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9_.-]{1,100}', repository) or repository.split('/')[1] in {'.', '..'}:
        raise ValueError('Use o formato usuario/repositorio.')
    return repository

def fetch(url, limit):
    request = Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'Dev-Forge-Updater'})
    with urlopen(request, timeout=20) as response:
        if urlparse(response.url).scheme != 'https':
            raise ValueError('Download sem HTTPS recusado.')
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError('Resposta excede o limite permitido.')
    return data

def check_release(repository, current=METADATA['version'], kind=None):
    repository = validate_repository(repository)
    release = json.loads(fetch(f'https://api.github.com/repos/{repository}/releases/latest', 1024 * 1024))
    if release.get('draft') or release.get('prerelease'):
        raise ValueError('Release nao estavel.')
    latest = release['tag_name']
    if version_tuple(latest) <= version_tuple(current):
        return None
    kind = kind or distribution_kind()
    name = ASSETS[kind]
    asset = next((a for a in release.get('assets', []) if a.get('name') == name), None)
    result = {'version': latest.removeprefix('v'), 'date': release.get('published_at', '')[:10], 'notes': str(release.get('body') or 'Sem notas publicadas.')[:20000], 'repository': repository, 'kind': kind, 'asset': name}
    # Asset digests are supplied by GitHub. Source-code archives are not used.
    if asset and re.fullmatch(r'sha256:[0-9a-f]{64}', asset.get('digest') or ''):
        url = asset['browser_download_url']
        if not url.startswith(f'https://github.com/{repository}/releases/download/'):
            raise ValueError('Origem do pacote invalida.')
        result.update(url=url, digest=asset['digest'][7:])
    return result

def extract_verified(data, destination, expected_version, kind='source'):
    """Validate every entry before extracting anything; never trust ZIP paths."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if len(entries) > 300 or sum(e.file_size for e in entries) > MAX_EXTRACTED:
            raise ValueError('Pacote excede os limites.')
        names = set()
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if ('\\' in entry.filename or ':' in entry.filename or path.is_absolute()
                    or '..' in path.parts or not path.parts or path.parts[0] != 'dev-forge'
                    or stat.S_ISLNK(entry.external_attr >> 16)):
                raise ValueError('Caminho inseguro no pacote.')
            normalized = str(path).casefold()
            if normalized in names:
                raise ValueError('Arquivo duplicado no pacote.')
            names.add(normalized)
        metadata = json.loads(archive.read('dev-forge/version.json'))
        if version_tuple(metadata['version']) != version_tuple(expected_version):
            raise ValueError('Versao do pacote difere da release.')
        requirements = {'source': ('app.py', 'ui.py', 'updater.py', 'engine.py', 'catalog.py', 'runtime.py'), 'windows': ('DevForge.exe',), 'linux': ('DevForge',)}
        for required in requirements[kind]:
            if f'dev-forge/{required}' not in archive.namelist():
                raise ValueError('Pacote incompleto.')
        archive.extractall(destination)
        if kind == 'linux':
            (destination / 'dev-forge' / 'DevForge').chmod(0o755)
    return destination / 'dev-forge'

def download_update(release, directory):
    if 'url' not in release or 'digest' not in release:
        raise ValueError('Release sem pacote verificado.')
    data = fetch(release['url'], MAX_DOWNLOAD)
    if hashlib.sha256(data).hexdigest() != release['digest']:
        raise ValueError('Integridade do download nao confirmada.')
    destination = Path(tempfile.mkdtemp(prefix='release-', dir=directory))
    return extract_verified(data, destination, release['version'], release.get('kind', 'source'))

def load_settings():
    try:
        return json.loads((data_directory() / 'settings.local.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {'repository': METADATA.get('repository', ''), 'check_on_start': False}

def save_settings(settings):
    if settings['repository']:
        validate_repository(settings['repository'])
    directory = data_directory()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / 'settings.local.json'
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(settings, indent=2), encoding='utf-8')
    temporary.replace(path)
