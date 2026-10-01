import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import generate, resolve, notes
from catalog import CATALOG, PROFILES

class GenerationTests(unittest.TestCase):
    def test_dependency_order(self):
        keys = [i['key'] for i in resolve(['minikube', 'angular'])]
        self.assertLess(keys.index('docker'), keys.index('minikube'))
        self.assertLess(keys.index('node'), keys.index('angular'))

    def test_reject_unknown_input(self):
        with self.assertRaises(ValueError):
            generate(['git; rm -rf /'], 'linux')
        with self.assertRaises(ValueError):
            generate(['git'], 'macos')

    def test_manual_is_explicit(self):
        script, manual = generate(['gcloud', 'vscode'], 'linux')
        self.assertEqual({i['key'] for i in manual}, {'gcloud', 'vscode'})
        self.assertNotIn('apt-get install', script)

    def test_profiles_and_all_tools(self):
        for keys in [*PROFILES.values(), list(CATALOG)]:
            for platform in ('windows', 'linux'):
                script, _ = generate(keys, platform)
                self.assertTrue(script.endswith('\n'))
                self.assertNotIn('curl |', script)

    def test_failures_stop_execution(self):
        windows, _ = generate(['git', 'angular'], 'windows')
        linux, _ = generate(['git'], 'linux')
        self.assertIn('$LASTEXITCODE', windows)
        self.assertIn('finally { Stop-Transcript }', windows)
        self.assertIn('set -euo pipefail', linux)

    def test_post_install_instructions_are_in_exported_script(self):
        for platform in ('windows', 'linux'):
            script, _ = generate(['vscode', 'minikube', 'postgres'], platform)
            self.assertIn('minikube start --driver=docker', script)
            self.assertIn('psql --version', script)
            self.assertIn('Visual Studio Code', script)
        self.assertIn('menu Iniciar', notes(['vscode'], 'windows'))
        self.assertIn('instalacao oficial manual', notes(['vscode'], 'linux'))

    def test_rstudio_requires_r(self):
        keys = [i['key'] for i in resolve(['rstudio'])]
        self.assertLess(keys.index('r'), keys.index('rstudio'))

if __name__ == '__main__':
    unittest.main()
