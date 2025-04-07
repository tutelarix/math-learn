import random
from random import randint

from rich.console import Console

from common.general.logger import logger


def get_mult_table_operation(cache_learned, min_num, max_num):
    logger.debug(len(cache_learned))
    logger.debug(cache_learned)

    full_max_num = 10
    if not len(cache_learned) == (max_num - min_num + 1) * (full_max_num - min_num + 1):
        current = -1
        while current in cache_learned or current == -1:
            first = randint(min_num, max_num)
            second = randint(min_num, full_max_num)
            current = (first, second)
        return current
    return None


def multi_table(cache, max_num):
    console = Console(color_system="windows")
    console.clear()
    console.print(f"Перевіряємо табличку множення до цифри {max_num}")
    console.print("Нажми 'q', щоб повернутися назад в меню")

    read_line = ""
    num_learned_samples = 0
    while read_line.lower() not in ["q", "й"]:
        console.print("---------")
        values = get_mult_table_operation(cache["learned"], 0, max_num)

        if values is None:
            console.print(f"Оуоу. Здається ти все вивчив до цифри {max_num}. Ти супер крутий.")
            break

        shuf_values = list(values)
        random.shuffle(shuf_values)
        read_line = console.input(f"{shuf_values[0]} * {shuf_values[1]} = ")
        if read_line.isdigit():
            multi_result = int(read_line)
            if shuf_values[0] * shuf_values[1] == multi_result:
                num_learned_samples += 1
                console.print(f"Правильно. Ура. Ти повторив {num_learned_samples} прикладів.")

                _cache_correct(cache, values)
            else:
                console.print(
                    f"Не правильно. {shuf_values[0]} * {shuf_values[1]} = {shuf_values[0] * shuf_values[1]}"
                )
                _cache_incorrect(cache, values)

        logger.debug(f"Cache: {cache}")

    console.print("Гарно попрацював.")


def _cache_correct(cache, values):
    if values in cache["learning"]:
        cache["learning"][values] -= 1
        if cache["learning"][values] == 0:
            del cache["learning"][values]
    else:
        cache["learned"].append(values)


def _cache_incorrect(cache, values):
    if values in cache["learning"]:
        cache["learning"][values] += 1
    else:
        cache["learning"][values] = 1


def division_multi_table(cache, max_num):
    console = Console(color_system="windows")
    console.clear()
    console.print(f"Перевіряємо ділення в табличці множення до цифри {max_num}")
    console.print("Нажми 'q', щоб повернутися назад в меню")

    num_learned_samples = 0
    read_line = ""
    while read_line.lower() not in ["q", "й"]:
        console.print("---------")
        values = get_mult_table_operation(cache["learned"], 1, max_num)

        if values is None:
            console.print(f"Оуоу. Здається ти все вивчив до цифри {max_num}. Ти супер крутий.")
            break

        shuf_values = list(values)
        random.shuffle(shuf_values)
        read_line = console.input(f"{shuf_values[0] * shuf_values[1]} / {shuf_values[0]} = ")
        if read_line.isdigit():
            div_value = int(read_line)
            if shuf_values[1] == div_value:
                num_learned_samples += 1
                console.print(f"Правильно. Ура. Ти повторив {num_learned_samples} прикладів.")

                _cache_correct(cache, values)
            else:
                console.print(
                    f"Не правильно. {shuf_values[0] * shuf_values[1]} / {shuf_values[0]} = {shuf_values[1]}"
                )
                _cache_incorrect(cache, values)

        logger.debug(f"Cache: {cache}")

    console.print("Гарно попрацював.")
