import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import publish_release
import updater
from runtime import updated_launch_command

class PublicationTests(unittest.TestCase):
    def fake_assets(self, directory):
        for name in publish_release.ASSETS:
            (Path(directory) / name).write_bytes(b'fixture')

    def test_existing_release_uploads_without_recreating(self):
        with tempfile.TemporaryDirectory() as directory:
            self.fake_assets(directory)
            with patch.object(publish_release.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as run:
                publish_release.publish('v' + updater.METADATA['version'], directory, 'devheron/dev-forge')
            commands = [call.args[0] for call in run.call_args_list]
            self.assertFalse(any(command[1:3] == ['release','create'] for command in commands))
            self.assertTrue(any('--clobber' in command for command in commands))
            self.assertIn('--draft=false', commands[-1])

    def test_new_release_stays_draft_until_assets_uploaded(self):
        with tempfile.TemporaryDirectory() as directory:
            self.fake_assets(directory)
            results = [subprocess.CompletedProcess([], 1), *[subprocess.CompletedProcess([], 0)] * 3]
            with patch.object(publish_release.subprocess, 'run', side_effect=results) as run:
                publish_release.publish('v' + updater.METADATA['version'], directory, 'devheron/dev-forge')
            commands = [call.args[0] for call in run.call_args_list]
            self.assertIn('--draft', commands[1])
            self.assertEqual(commands[2][1:3], ['release','upload'])
            self.assertIn('--latest', commands[3])

    def test_failed_upload_does_not_publish_draft(self):
        with tempfile.TemporaryDirectory() as directory:
            self.fake_assets(directory)
            with patch.object(publish_release.subprocess, 'run', side_effect=[subprocess.CompletedProcess([],1),subprocess.CompletedProcess([],0),subprocess.CalledProcessError(1,['gh'])]) as run:
                with self.assertRaises(subprocess.CalledProcessError):
                    publish_release.publish('v' + updater.METADATA['version'], directory, 'devheron/dev-forge')
            self.assertEqual(run.call_count, 3)

    def test_mismatch_stops_before_github(self):
        with patch.object(publish_release.subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                publish_release.publish('v0.0.1','missing','devheron/dev-forge')
            run.assert_not_called()

    def test_native_package_selection(self):
        release = {'tag_name':'v9.0.0','assets':[]}
        for kind,name in updater.ASSETS.items():
            release['assets'].append({'name':name,'digest':'sha256:'+'a'*64,'browser_download_url':'https://github.com/devheron/dev-forge/releases/download/v9.0.0/'+name})
        with patch.object(updater,'fetch',return_value=json.dumps(release).encode()):
            for kind,name in updater.ASSETS.items():
                result=updater.check_release('devheron/dev-forge',kind=kind)
                self.assertEqual(result['asset'],name)
                self.assertIn('digest',result)
        self.assertEqual(updated_launch_command(Path('test'), 'windows'), [str(Path('test/DevForge.exe'))])

if __name__ == '__main__':
    unittest.main()
