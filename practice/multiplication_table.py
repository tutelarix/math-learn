import random
from enum import IntEnum
from random import randint

from common.general.logger import logger


def _init_db(database):
    if not database:
        database["correct_done"] = [[], []]
        database["incorrect"] = [{}, {}]


def _add_correct(database, operation, values):
    incorrect_answers_db = database["incorrect"][operation]
    correct_answers_db = database["correct_done"][operation]

    if values in incorrect_answers_db:
        incorrect_answers_db[values] -= 1
        if incorrect_answers_db[values] == 0:
            del incorrect_answers_db[values]
    else:
        correct_answers_db.append(values)


def _add_incorrect(database, operation, values):
    incorrect_answers_db = database["incorrect"][operation]

    if values in incorrect_answers_db:
        incorrect_answers_db[values] += 1
    else:
        incorrect_answers_db[values] = 1


class Operation(IntEnum):
    Multiplication = 0
    Deletion = 1

    @staticmethod
    def get_operation():
        return Operation(randint(0, 1))


def _get_mult_table_operation(database_learned, min_num, max_num):
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
    """
    Launch testing of multiplication table
    :param app: application
    :param database: database
    """
    _init_db(database)
    com_interface = app.get_com_interface()
    max_num = app.get_config()["multiplication_table_max"]

    com_interface.clear()
    com_interface.dialog(
        f"Перевіряємо табличку множення до цифри {max_num}\n"
        "Нажми 'q', щоб повернутися назад в меню"
    )

    num_learned_samples_in_session = 0
    while True:
        com_interface.dialog("---------")

        operation = Operation.get_operation()
        values = _get_mult_table_operation(database["correct_done"][operation], 1, max_num)

        if values is None:
            com_interface.dialog(
                f"Оуоу. Здається ти все вивчив до цифри {max_num}. Ти супер крутий."
            )
            break

        shuffled_values = list(values)
        random.shuffle(shuffled_values)

        question = ""
        correct_answer = 0
        if operation == Operation.Multiplication:
            question = f"{shuffled_values[0]} * {shuffled_values[1]} = "
            correct_answer = shuffled_values[0] * shuffled_values[1]
        if operation == Operation.Deletion:
            question = f"{shuffled_values[0] * shuffled_values[1]} / {shuffled_values[0]} = "
            correct_answer = shuffled_values[1]
        correct_answer_text = f"{question}{correct_answer}"

        answer = com_interface.input(question)
        if answer.lower() in ["q", "й"]:
            break

        if answer.isdigit() and int(answer) == correct_answer:
            num_learned_samples_in_session += 1
            com_interface.dialog(
                f"Правильно. Ура. Ти повторив {num_learned_samples_in_session} прикладів."
            )
            _add_correct(database, operation, values)
        else:
            com_interface.dialog(f"Не правильно. {correct_answer_text}")
            _add_incorrect(database, operation, values)

    com_interface.dialog("Гарно попрацював.")
