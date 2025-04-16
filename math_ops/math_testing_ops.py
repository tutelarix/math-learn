import random
from random import randint

from common.general.logger import logger


def get_mult_table_operation(database_learned, min_num, max_num):
    logger.debug(len(database_learned))
    logger.debug(database_learned)

    full_max_num = 10
    if not len(database_learned) == (max_num - min_num + 1) * (full_max_num - min_num + 1):
        current = -1
        while current in database_learned or current == -1:
            first = randint(min_num, max_num)
            second = randint(min_num, full_max_num)
            current = (first, second)
        return current
    return None


def multi_table(app, database):
    _init_db(database)
    max_num = app.get_config()["max_num"]
    com_interface = app.get_com_interface()
    com_interface.clear()
    com_interface.dialog(
        f"Перевіряємо табличку множення до цифри {max_num}\n"
        "Нажми 'q', щоб повернутися назад в меню"
    )

    read_line = ""
    num_learned_samples = 0
    while read_line.lower() not in ["q", "й"]:
        com_interface.dialog("---------")
        values = get_mult_table_operation(database["done"], 0, max_num)

        if values is None:
            com_interface.dialog(
                f"Оуоу. Здається ти все вивчив до цифри {max_num}. Ти супер крутий."
            )
            break

        shuf_values = list(values)
        random.shuffle(shuf_values)
        read_line = com_interface.input(f"{shuf_values[0]} * {shuf_values[1]} = ")
        if read_line.isdigit():
            if shuf_values[0] * shuf_values[1] == int(read_line):
                num_learned_samples += 1
                com_interface.dialog(
                    f"Правильно. Ура. Ти повторив {num_learned_samples} прикладів."
                )

                _add_correct(database, values)
            else:
                com_interface.dialog(
                    f"Не правильно. {shuf_values[0]} * {shuf_values[1]} = {shuf_values[0] * shuf_values[1]}"
                )
                _add_incorrect(database, values)

        logger.debug(f"Database: {database}")

    com_interface.dialog("Гарно попрацював.")


def _add_correct(database, values):
    if values in database["todo"]:
        database["todo"][values] -= 1
        if database["todo"][values] == 0:
            del database["todo"][values]
    else:
        database["done"].append(values)


def _add_incorrect(database, values):
    if values in database["todo"]:
        database["todo"][values] += 1
    else:
        database["todo"][values] = 1


def division_multi_table(app, database):
    _init_db(database)
    max_num = app.get_config()["max_num"]
    com_interface = app.get_com_interface()
    com_interface.clear()
    com_interface.dialog(
        f"Перевіряємо ділення в табличці множення до цифри {max_num}\n"
        "Нажми 'q', щоб повернутися назад в меню",
    )

    num_learned_samples = 0
    read_line = ""
    while read_line.lower() not in ["q", "й"]:
        com_interface.dialog("---------")
        values = get_mult_table_operation(database["done"], 1, max_num)

        if values is None:
            com_interface.dialog(
                f"Оуоу. Здається ти все вивчив до цифри {max_num}. Ти супер крутий."
            )
            break

        shuf_values = list(values)
        random.shuffle(shuf_values)
        read_line = com_interface.input(f"{shuf_values[0] * shuf_values[1]} / {shuf_values[0]} = ")
        if read_line.isdigit():
            if shuf_values[1] == int(read_line):
                num_learned_samples += 1
                com_interface.dialog(
                    f"Правильно. Ура. Ти повторив {num_learned_samples} прикладів."
                )

                _add_correct(database, values)
            else:
                com_interface.dialog(
                    f"Не правильно. {shuf_values[0] * shuf_values[1]} / {shuf_values[0]} = {shuf_values[1]}"
                )
                _add_incorrect(database, values)

        logger.debug(f"Database: {database}")

    com_interface.dialog("Гарно попрацював.")


def _init_db(database):
    if not database:
        database["done"] = []
        database["todo"] = {}
