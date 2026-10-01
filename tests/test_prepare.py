import subprocess
import unittest
from unittest.mock import patch
import prepare_release

class PrepareTests(unittest.TestCase):
    def test_main_creates_and_pushes_version_tag(self):
        responses = [subprocess.CompletedProcess([],0,'abc\n'), subprocess.CompletedProcess([],1,''), subprocess.CompletedProcess([],0,''), subprocess.CompletedProcess([],0,'')]
        with patch.object(prepare_release.subprocess,'run',side_effect=responses) as run:
            tag, commit = prepare_release.prepare('main')
        self.assertEqual(commit,'abc')
        self.assertEqual(run.call_args_list[-1].args[0],['git','push','origin','refs/tags/'+tag])

    def test_existing_same_commit_is_reusable(self):
        responses = [subprocess.CompletedProcess([],0,'abc\n'),subprocess.CompletedProcess([],0,'abc\n')]
        with patch.object(prepare_release.subprocess,'run',side_effect=responses) as run:
            prepare_release.prepare('main')
        self.assertEqual(run.call_count,2)

    def test_existing_other_commit_requires_new_version(self):
        responses = [subprocess.CompletedProcess([],0,'abc\n'),subprocess.CompletedProcess([],0,'old\n')]
        with patch.object(prepare_release.subprocess,'run',side_effect=responses) as run:
            with self.assertRaises(ValueError):
                prepare_release.prepare('main')
        self.assertEqual(run.call_count,2)
