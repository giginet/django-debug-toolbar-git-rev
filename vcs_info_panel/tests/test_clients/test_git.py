import subprocess
import pytz
from unittest.mock import patch

import datetime
from django.test import TestCase

from vcs_info_panel.clients.git import GitClient


def without_git_repository(*commands):
    def decorator(func):
        def inner(*args, **kwargs):
            with patch('subprocess.check_output') as _check_output:
                _check_output.side_effect = subprocess.CalledProcessError(128,
                                                                          commands,
                                                                          'fatal: Not a git repository (or any of the parent directories): .git')
                return func(*args, **kwargs)
        return inner
    return decorator


class GitClientTestCase(TestCase):
    def setUp(self):
        self.client = GitClient()

    def _test_called_check_output(self, commands):
        with patch('subprocess.check_output') as _check_output:
            _check_output.assert_called_with(commands)

    def test_base_command(self):
        self.assertEqual(self.client.base_command, 'git')

    def test_is_repository_with_repository(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'true'
            self.assertEqual(self.client.is_repository(), True)
            _check_output.assert_called_once_with(['git', 'rev-parse', '--is-inside-work-tree'])

    @without_git_repository('git', 'rev-parse', '--is-inside-work-tree')
    def test_is_repository_without_repository(self):
        self.assertEqual(self.client.is_repository(), False)

    def test_get_short_hash(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'3218766'
            self.assertEqual(self.client.get_short_hash(), '3218766')
            _check_output.assert_called_once_with(['git', 'rev-parse', 'HEAD'])

    @without_git_repository('git', 'rev-parse', 'HEAD')
    def test_get_short_hash_without_repository(self):
        self.assertEqual(self.client.get_short_hash(), None)

    def test_get_short_hash(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'3218766'
            self.assertEqual(self.client.get_short_hash(), '3218766')
            _check_output.assert_called_once_with(['git', 'rev-parse', '--short', 'HEAD'])

    @without_git_repository('git', 'rev-parse', '--short', 'HEAD')
    def test_get_short_hash_without_repository(self):
        self.assertEqual(self.client.get_short_hash(), None)

    def test_get_current_branch_name(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'master'
            self.assertEqual(self.client.get_current_branch_name(), 'master')
            _check_output.assert_called_once_with(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

    @without_git_repository('git', 'rev-parse', '--abbrev-ref', 'HEAD')
    def test_get_hash_without_repository(self):
        self.assertEqual(self.client.get_current_branch_name(), None)

    def test_get_author_name(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'giginet'
            self.assertEqual(self.client.get_author_name(), 'giginet')
            _check_output.assert_called_once_with(['git', 'show', '--format=%an', 'HEAD'])

    @without_git_repository('git', 'show', '--format=%an', 'HEAD')
    def test_get_author_email_without_repository(self):
        self.assertEqual(self.client.get_author_email(), None)

    def test_get_author_email(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'giginet@kawaz.org'
            self.assertEqual(self.client.get_author_email(), 'giginet@kawaz.org')
            _check_output.assert_called_once_with(['git', 'show', '--format=%ae', 'HEAD'])

    @without_git_repository('git', 'show', '--format=%ae', 'HEAD')
    def test_get_author_email_without_repository(self):
        self.assertEqual(self.client.get_author_email(), None)

    def test_get_committer_name(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'giginet'
            self.assertEqual(self.client.get_committer_name(), 'giginet')
            _check_output.assert_called_once_with(['git', 'show', '--format=%cn', 'HEAD'])

    @without_git_repository('git', 'show', '--format=%cn', 'HEAD')
    def test_get_committer_email_without_repository(self):
        self.assertEqual(self.client.get_committer_email(), None)

    def test_get_committer_email(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'giginet@kawaz.org'
            self.assertEqual(self.client.get_committer_email(), 'giginet@kawaz.org')
            _check_output.assert_called_once_with(['git', 'show', '--format=%ce', 'HEAD'])

    @without_git_repository('git', 'show', '--format=%ce', 'HEAD')
    def test_get_committer_email_without_repository(self):
        self.assertEqual(self.client.get_committer_email(), None)

    def test_get_date(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'2015-12-04 20:29:10 +0900'
            jst = pytz.timezone('Asia/Tokyo')
            self.assertEqual(self.client.get_date(), datetime.datetime(2015, 12, 4, 20, 29, 10, tzinfo=jst))
            _check_output.assert_called_once_with(['git', 'show', '--format=%ci', 'HEAD'])

    @without_git_repository('git', 'show', '--format=%ci', 'HEAD')
    def test_get_date_without_repository(self):
        self.assertEqual(self.client.get_date(), None)

    def test_get_message(self):
        with patch('subprocess.check_output') as _check_output:
            _check_output.return_value = b'Fix issue'
            self.assertEqual(self.client.get_message(), 'Fix issue')
            _check_output.assert_called_once_with(['git', 'show', '--format=%b', 'HEAD'])

    @without_git_repository('git', 'show', '--format=%b', 'HEAD')
    def test_get_message_without_repository(self):
        self.assertEqual(self.client.get_message(), None)