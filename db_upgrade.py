"""
Script to upgrade database.
"""
import pickle
import os


CURRENT_VERSION_FILENAME = "current_db_version"
DB_SCRIPTS_FOLDER = "db_scripts"


class UpgradeScript(object):
    """Class to do the database upgrade using scripts."""

    @staticmethod
    def read_current_version():
        """Read the database version from file."""

        try:
            version_file = open(CURRENT_VERSION_FILENAME, "rb")
        except IOError:
            # Writing current version "db" registry if not found
            UpgradeScript.write_current_version(0)
            return 0

        with version_file:
            return pickle.load(version_file)

    @staticmethod
    def write_current_version(version):
        """Write the new database version to file."""

        with open(CURRENT_VERSION_FILENAME, "wb") as version_file:
            pickle.dump(version, version_file)

    @staticmethod
    def get_scripts_versions(filenames):
        """Get all scripts versions from the scripts folder."""

        # Filtering filenames
        filenames = [filename for filename in filenames
                     if any(map(str.isdigit, filename))]

        # List comprehension to get all digits from each filename
        return [int(filter(str.isdigit, filename)) for filename in filenames]

    @staticmethod
    def get_newer_scripts(filenames, scripts_versions, current_version):
        """Upgrade the database with newer scripts."""

        # List comprehension to get all script versions newer than current
        versions_to_run = [v for v in scripts_versions if v > current_version]

        # List comprehension to get all scripts that belong to runable versions
        db_scripts_to_run = [
            sql for sql in filenames if
            int(filter(str.isdigit, sql)) in versions_to_run
        ]

        return db_scripts_to_run

    @staticmethod
    def run():
        """Main code to upgrade database if new scripts in scripts folder."""

        try:
            filenames = os.listdir(DB_SCRIPTS_FOLDER)
        except OSError:
            print "Scripts folder not found: " + DB_SCRIPTS_FOLDER
            exit(1)

        scripts_versions = UpgradeScript.get_scripts_versions(filenames)

        if len(scripts_versions) == 0:
            print "There are no proper db scripts to run."
            exit(1)

        max_version = max(scripts_versions)

        current_version = UpgradeScript.read_current_version()

        # If old database, run newer scripts and update current version
        if current_version < max_version:
            newer_scripts = UpgradeScript.get_newer_scripts(
                filenames,
                scripts_versions,
                current_version
            )
            UpgradeScript.write_current_version(max_version)
            print "The database was upgraded to version " + str(max_version)
            print "These are the executed scripts:"
            for script in newer_scripts:
                print script
        else:
            print "There are no upgrades to make to the database."


if __name__ == "__main__":
    UpgradeScript().run()
