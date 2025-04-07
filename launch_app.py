import logging
import pickle
from enum import IntEnum
from pathlib import Path

import click
from beaupy import select
from rich.console import Console

from common.general.logger import logger
from math_testing_ops import multi_table, division_multi_table


class MainOptions(IntEnum):
    Multiplication = 0
    Deletion = 1
    ClearDatabase = 2


def _load_cache(cache_file_path, is_clear_db=False):
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
    logger.debug(f"Cache: {cache}")

    with open(cache_file_path, "wb") as cache_file:
        pickle.dump(cache, cache_file)


def launch_app(is_clear_db=False):
    """
    Launch application
    :param is_clear_db: clear database file
    """
    max_num = 5

    console = Console(color_system="windows")
    console.clear()
    console.print("Привіт Вовчик! Давай потренуємо математику.")

    cache_file_path = Path(__file__).parent.joinpath("cache.dat")
    cache = _load_cache(cache_file_path, is_clear_db)

    op_index = -1
    ops = ["Табличка множення", "Ділення", "Вихід"]
    while op_index != len(ops) - 1:
        console.print("Вибери з опцій нижче, що хочеш потренувати.")
        operation = select(ops, cursor="🢧", cursor_style="cyan")
        console.clear()
        console.print(f"Ти вибрав: {operation}.")

        op_index = ops.index(operation)
        if op_index == MainOptions.Multiplication:
            multi_table(cache["multi_table_multi"], max_num)
            _save_cache(cache_file_path, cache)
        elif op_index == MainOptions.Deletion:
            division_multi_table(cache["multi_table_div"], max_num)
            _save_cache(cache_file_path, cache)

        console.print("")

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
