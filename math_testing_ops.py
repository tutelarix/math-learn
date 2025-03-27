import pickle
from random import randint

from rich.console import Console

from common.general.logger import logger


def get_mult_table_operation(cache_learned, max_num, is_debug):
    if is_debug:
        logger.debug(cache_learned)
    if not len(cache_learned) == (max_num + 1) * (max_num + 1):
        current = -1
        while current in cache_learned or current == -1:
            first = randint(0, max_num)
            second = randint(0, max_num)
            current = (first, second)
        return current
    return None


def multiplication_table(cache_file_path, is_debug=False):
    max_num = 2

    console = Console(color_system="windows")
    console.clear()
    console.print("Перевіряємо табличку множення")
    console.print("Нажми 'q', щоб повернутися назад в меню")

    if cache_file_path.exists():
        with open(cache_file_path, "rb") as cache_file:
            cache = pickle.load(cache_file)
    else:
        cache = {"multi_table": {"learned": []}}
    read_line = ""
    while read_line.lower() not in ["q", "й"]:
        console.print("---------")
        values = get_mult_table_operation(cache["multi_table"]["learned"], max_num, is_debug)
        if values is None:
            console.print(f"Оуоу. Здається ти все вивчив до цифри {max_num}. Ти супер крутий.")
            break
        read_line = console.input(f"{values[0]} * {values[1]} = ")
        if read_line.isdigit():
            multi_result = int(read_line)
            if values[0] * values[1] == multi_result:
                console.print("Правильно. Ура.")
                cache["multi_table"]["learned"].append(values)
            else:
                console.print(f"Не правильно. {values[0]} * {values[1]} = {values[0] * values[1]}")

    with open(cache_file_path, "wb") as cache_file:
        pickle.dump(cache, cache_file)
    console.print("Гарно попрацював.")
