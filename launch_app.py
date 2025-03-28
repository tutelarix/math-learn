import pickle
from enum import IntEnum
from pathlib import Path

from beaupy import select
from rich.console import Console

from common.general.logger import logger
from math_testing_ops import multiplication_table


class MainOptions(IntEnum):
    Multiplication = 0
    Deletion = 1
    ClearDatabase = 2


def _load_cache(cache_file_path, is_debug):
    if cache_file_path.exists():
        with open(cache_file_path, "rb") as cache_file:
            cache = pickle.load(cache_file)
    else:
        cache = {"multi_table": {"learned": [], "learning": {}}}

    if is_debug:
        logger.debug(f"Cache: {cache}")

    return cache


def _save_cache(cache_file_path, cache, is_debug):
    if is_debug:
        logger.debug(f"Cache: {cache}")

    with open(cache_file_path, "wb") as cache_file:
        pickle.dump(cache, cache_file)


def launch_app(cache_file_path, is_debug=False):
    max_num = 5

    console = Console(color_system="windows")
    console.clear()
    console.print("Привіт Вовчик! Давай потренуємо математику.")

    cache = _load_cache(cache_file_path, is_debug)

    op_index = -1
    ops = ["Табличка множення", "Ділення", "Стерти історію", "Вихід"]
    while op_index != len(ops) - 1:
        console.print("Вибери з опцій нижче, що хочеш потренувати.")
        operation = select(ops, cursor="🢧", cursor_style="cyan")
        console.clear()
        console.print(f"Ти вибрав: {operation}.")

        op_index = ops.index(operation)
        if op_index == MainOptions.Multiplication:
            multiplication_table(cache["multi_table"], max_num, is_debug)
            _save_cache(cache_file_path, cache, is_debug)
        elif op_index == MainOptions.Deletion:
            console.print("Ділення не реалізовано")
        elif op_index == MainOptions.ClearDatabase:
            cache_file_path.unlink(missing_ok=True)
            console.print("Історія минулих тестувань стерта")

        console.print("")

    _save_cache(cache_file_path, cache, is_debug)


def main():
    is_debug = True
    cache_file_path = Path(__file__).parent.joinpath("cache.dat")

    launch_app(cache_file_path, is_debug)


if __name__ == "__main__":
    main()
