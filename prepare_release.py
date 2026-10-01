"""Create the metadata version tag on main, or validate an existing tag."""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent

def prepare(reference):
    metadata = json.loads((BASE / 'version.json').read_text(encoding='utf-8'))
    version = metadata['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+',version):
        raise ValueError('Use uma versao estavel numerica, como 0.4.0.')
    tag = 'v' + version
    if reference not in ('main', tag):
        raise ValueError('Branch/tag nao corresponde a version.json.')
    def git(*args, check=True):
        return subprocess.run(['git', *args],cwd=BASE,check=check,text=True,capture_output=True)
    commit = git('rev-parse','HEAD').stdout.strip()
    existing = git('rev-list','-n','1',tag,check=False)
    if existing.returncode == 0:
        if existing.stdout.strip() != commit:
            raise ValueError('Esta versao ja aponta para outro commit. Aumente a versao antes de publicar.')
    elif reference == 'main':
        git('tag',tag,commit)
        git('push','origin','refs/tags/'+tag)
    else:
        raise ValueError('Tag informada nao existe.')
    return tag, commit

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref',required=True)
    args=parser.parse_args()
    tag,commit=prepare(args.ref)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a',encoding='utf-8') as output:
            output.write('tag='+tag+'\ncommit='+commit+'\n')
    print('Preparada release '+tag)
