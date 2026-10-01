import io
import json
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import updater
from package_release import build

class UpdateTests(unittest.TestCase):
    def test_version_order(self):
        self.assertGreater(updater.version_tuple('v0.10.0'), updater.version_tuple('0.2.0'))
        for value in ('v1', '1.0.0-beta', '../evil'):
            with self.assertRaises(ValueError):
                updater.version_tuple(value)

    def test_repository_validation(self):
        self.assertEqual(updater.validate_repository('devheron/dev-forge'), 'devheron/dev-forge')
        for value in ('../repo', 'owner/../repo', 'https://evil.test', 'a/..'):
            with self.assertRaises(ValueError):
                updater.validate_repository(value)

    def release_data(self, version='v0.3.0'):
        return json.dumps({'tag_name': version, 'assets': [{'name': 'dev-forge.zip', 'browser_download_url': 'https://github.com/devheron/dev-forge/releases/download/v0.3.0/dev-forge.zip', 'digest': 'sha256:' + 'a' * 64}]}).encode()

    def test_new_version_and_current(self):
        with patch.object(updater, 'fetch', return_value=self.release_data()):
            release = updater.check_release('devheron/dev-forge', current='0.2.0')
            self.assertEqual(release['version'], '0.3.0')
            self.assertIn('digest', release)
        with patch.object(updater, 'fetch', return_value=self.release_data('v0.2.0')):
            self.assertIsNone(updater.check_release('devheron/dev-forge', current='0.2.0'))

    def test_missing_digest_disables_download(self):
        data = json.loads(self.release_data())
        data['assets'][0].pop('digest')
        with patch.object(updater, 'fetch', return_value=json.dumps(data).encode()):
            self.assertNotIn('url', updater.check_release('devheron/dev-forge', current='0.2.0'))

    def test_integrity_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(updater, 'fetch', return_value=b'tampered'):
                with self.assertRaises(ValueError):
                    updater.download_update({'url': 'https://github.com', 'digest': '0' * 64, 'version': '0.3.0'}, directory)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_zip_traversal_rejected(self):
        for name in ('dev-forge/../../outside.py', '/outside.py', 'dev-forge/..\\outside.py', 'dev-forge/C:evil.py'):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as archive:
                archive.writestr(name, 'bad')
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(ValueError):
                    updater.extract_verified(buffer.getvalue(), Path(directory), '0.2.0')
                self.assertEqual(list(Path(directory).iterdir()), [])

    def test_real_package_and_preservation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'dev-forge.zip'
            build(path)
            data = path.read_bytes()
            with zipfile.ZipFile(path) as archive:
                self.assertNotIn('dev-forge/settings.local.json', archive.namelist())
                self.assertFalse(any(n.endswith('.log') for n in archive.namelist()))
            with patch.object(updater, 'fetch', return_value=data):
                extracted = updater.download_update({'url': 'https://github.com', 'digest': hashlib.sha256(data).hexdigest(), 'version': updater.METADATA['version']}, directory)
            self.assertTrue((extracted / 'app.py').exists())
            self.assertTrue(path.exists())
            with self.assertRaises(ValueError):
                updater.extract_verified(data, Path(directory) / 'other', '9.9.9')

if __name__ == '__main__':
    unittest.main()
