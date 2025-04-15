import pickle
from enum import IntEnum, auto
from pathlib import Path

from common.general.logger import logger


class DatabaseID(IntEnum):
    """
    Database IDs
    """

    MultiplicationTable = auto()
    AdditionSubtraction = auto()


class Database:
    """
    Implementation of database
    """

    def __init__(self, folder_path: Path):
        """
        :param folder_path: path to folder with database
        """
        self._db_file_path = folder_path.joinpath("cache.dat")
        self._db: dict = self._get_init_db()

    @staticmethod
    def _get_init_db():
        return {
            DatabaseID.MultiplicationTable: {},
            DatabaseID.AdditionSubtraction: {},
        }

    def load_db(self, is_clear_db=False):
        """
        Load database. If database isn't created, it will create it.
        :param is_clear_db: where to clear database and start from scratch
        """
        if is_clear_db:
            logger.debug("Clear db file")
            self._db_file_path.unlink(missing_ok=True)
            self._db = self._get_init_db()

        if self._db_file_path.exists():
            with open(self._db_file_path, "rb") as cache_file:
                self._db = pickle.load(cache_file)

        logger.debug(f"Database: {self._db}")

    def save_db(self):
        """
        Save database
        :return:
        """
        logger.debug(f"Cache: {self._db}")

        with open(self._db_file_path, "wb") as cache_file:
            pickle.dump(self._db, cache_file)

    def get_data(self, db_id: DatabaseID):
        """
        Get database data by ID
        :param db_id: id
        :return: data
        """
        return self._db[db_id]
