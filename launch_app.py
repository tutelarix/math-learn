import logging
import pickle
from enum import IntEnum
from pathlib import Path

import click
from beaupy import select

from common.application import Application
from common.communication_interface import CommunicationInterface
from common.general.logger import logger
from math_ops.math_testing_ops import multi_table, division_multi_table


class MainOptions(IntEnum):
    Multiplication = 0
    Deletion = 1


def _load_cache(cache_file_path, is_clear_db=False):
    """
    Load cache
    :param cache_file_path: path to cache file
    :param is_clear_db: where to remove the file and start from scratch
    :return: cache data
    """
    if is_clear_db:
        logger.debug("Clear db file")
        cache_file_path.unlink(missing_ok=True)

    if cache_file_path.exists():
        with open(cache_file_path, "rb") as cache_file:
            cache = pickle.load(cache_file)
    else:
        cache = {
            "multi_table_multi": {"learned": [], "learning": {}},
            "multi_table_div": {"learned": [], "learning": {}},
        }

    logger.debug(f"Cache: {cache}")
    return cache


def _save_cache(cache_file_path, cache):
    """
    Save cache to file
    :param cache_file_path: path to cache file
    :param cache: cache data
    """
    logger.debug(f"Cache: {cache}")

    with open(cache_file_path, "wb") as cache_file:
        pickle.dump(cache, cache_file)


def launch_app(is_clear_db=False):
    """
    Launch application
    :param is_clear_db: clear database file
    """
    app = Application(com_interface_type=CommunicationInterface.Console)
    com_interface = app.get_com_interface()

    com_interface.clear()
    com_interface.dialog("Привіт Вовчик! Давай потренуємо математику.")

    cache_file_path = Path(__file__).parent.joinpath("cache.dat")
    cache = _load_cache(cache_file_path, is_clear_db)

    op_index = -1
    ops = ["Табличка множення", "Ділення", "Вихід"]
    while op_index != len(ops) - 1:
        com_interface.dialog("Вибери з опцій нижче, що хочеш потренувати.")
        operation = select(ops, cursor="🢧", cursor_style="cyan")
        com_interface.clear()
        com_interface.dialog(f"Ти вибрав: {operation}.")

        op_index = ops.index(operation)
        if op_index == MainOptions.Multiplication:
            multi_table(app, cache["multi_table_multi"])
            _save_cache(cache_file_path, cache)
        elif op_index == MainOptions.Deletion:
            division_multi_table(app, cache["multi_table_div"])
            _save_cache(cache_file_path, cache)

        com_interface.dialog("")

    _save_cache(cache_file_path, cache)


@click.command()
@click.option("--verbose", "-V", is_flag=True, help="Print debug output.")
@click.option("--clear-db", is_flag=True, help="Clear database")
def main(verbose=False, clear_db=False):
    print(verbose)

    if not verbose:
        logger.level = logging.CRITICAL

    launch_app(is_clear_db=clear_db)


if __name__ == "__main__":
    main()
