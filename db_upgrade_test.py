"""
Testing database upgrade script
"""
import unittest
import os
from db_upgrade import UpgradeScript


class UpgradeScriptTest(unittest.TestCase):
    """Class to test Upgrade Script."""

    initial_current_version = 0
    filenames = os.listdir("test_db_scripts")

    def setUp(self):
        """Setting up a new object to be tested."""
        self.script = UpgradeScript()
        self.initial_current_version = self.script.read_current_version()

    def tearDown(self):
        self.script.write_current_version(self.initial_current_version)

    def test_current_version(self):
        """Testing current version."""

        current_version = self.script.read_current_version()
        self.assertIsNotNone(current_version)

        current_version = 10
        self.script.write_current_version(current_version)

        current_version = self.script.read_current_version()
        self.assertEqual(current_version, 10)

    def test_get_scripts_versions(self):
        """Testing getting newer scripts."""

        scripts_versions = self.script.get_scripts_versions(self.filenames)
        self.assertEqual(len(scripts_versions), 4)
        self.assertEqual(scripts_versions, [27, 45, 99, 134])

    def test_get_newer_scripts(self):
        """Testing getting newer scripts."""

        scripts_versions = self.script.get_scripts_versions(self.filenames)

        newer_scripts = self.script.get_newer_scripts(
            self.filenames, scripts_versions, 0)
        self.assertEqual(len(newer_scripts), 4)

        newer_scripts = self.script.get_newer_scripts(
            self.filenames, scripts_versions, 28)
        self.assertEqual(len(newer_scripts), 3)

        newer_scripts = self.script.get_newer_scripts(
            self.filenames, scripts_versions, 46)
        self.assertEqual(len(newer_scripts), 2)

        newer_scripts = self.script.get_newer_scripts(
            self.filenames, scripts_versions, 100)
        self.assertEqual(len(newer_scripts), 1)


def main():
    """Main method to call all tests."""
    unittest.main()

if __name__ == '__main__':
    main()
