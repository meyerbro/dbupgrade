# dbupgrade

Python Script to Upgrade a Database.

## Getting Started

First you need to create a folder called db_scripts and put all the db scripts you want there.

Then, just run python db_upgrade.py and it will generate a new current version to the database.

After that, at each run, it will go to this folder and check what to do, according to the correct behavior.

## Testing

To test, just run python db_upgrade_test.py.

## Travis CI

There's an integration with Travis CI, which will test the script every time someone creates a PR.
