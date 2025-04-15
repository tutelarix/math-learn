import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from common.Database import Database, DatabaseID


class TestDatabase(unittest.TestCase):
    def test_database_save_load(self):
        # pylint: disable=protected-access
        with TemporaryDirectory() as temp_dir:
            db = Database(Path(temp_dir))

            # No file on start
            self.assertFalse(db._db_file_path.exists())

            # No file after load, because it's new db
            db.load_db()
            self.assertFalse(db._db_file_path.exists())

            # After save, file exists
            db.save_db()
            self.assertTrue(db._db_file_path.exists())

            # After load, file exists
            db.load_db()
            self.assertTrue(db._db_file_path.exists())

            # No file after clear db
            db.load_db(is_clear_db=True)
            self.assertFalse(db._db_file_path.exists())

    def test_get_data(self):
        with TemporaryDirectory() as temp_dir:
            # Save changes to db
            db = Database(Path(temp_dir))
            multi_table_data = db.get_data(DatabaseID.MultiplicationTable)
            self.assertFalse(db.get_data(DatabaseID.MultiplicationTable))
            multi_table_data["learned"] = 5
            db.save_db()

            # Load changes and check
            db = Database(Path(temp_dir))
            self.assertFalse(db.get_data(DatabaseID.MultiplicationTable))
            db.load_db()
            self.assertEqual(db.get_data(DatabaseID.MultiplicationTable)["learned"], 5)

            # Load db, but clear it
            db.load_db(is_clear_db=True)
            self.assertFalse(db.get_data(DatabaseID.MultiplicationTable))


if __name__ == "__main__":
    unittest.main()
