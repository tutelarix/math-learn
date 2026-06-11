import random
from enum import IntEnum

from common.general.logger import logger


class _Operation(IntEnum):
    Addition = 0
    Subtraction = 1

    @staticmethod
    def get_operation():
        return _Operation(random.randint(0, 1))


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
            correct_answers_db.append(values)
            logger.debug(f"Added {values} to correct pool. Removed from incorrect pool.")
    else:
        correct_answers_db.append(values)
        logger.debug(f"Added {values} to correct pool (no prior failures).")


def _add_incorrect(database, operation, values):
    incorrect_answers_db = database["incorrect"][operation]
    if values in incorrect_answers_db:
        incorrect_answers_db[values] += 1
    else:
        incorrect_answers_db[values] = 1
    logger.debug(f"Added {values} to incorrect pool. Failure count: {incorrect_answers_db[values]}")


def _generate_number(num_digits: int) -> int:
    if num_digits <= 0:
        return 0
    min_val = 10 ** (num_digits - 1) if num_digits > 1 else 0
    max_val = 10**num_digits - 1
    return random.randint(min_val, max_val)


def _get_status_message(database):
    correct_count = sum(len(lst) for lst in database["correct_done"])
    lines = [f"Засвоєно прикладів: {correct_count}"]

    incorrect_items = []
    for op_idx, op_dict in enumerate(database["incorrect"]):
        op_name = "додавання" if op_idx == _Operation.Addition else "віднімання"
        for values, count in op_dict.items():
            incorrect_items.append(f"{op_name}: {values} - потрібно ще {count} разів")

    if incorrect_items:
        lines.append("Незасвоєні приклади:")
        lines.extend(incorrect_items)

    return "\n".join(lines)


def _get_user_answer(answer):
    try:
        # Robustly handle negative numbers and potential formatting issues (spaces, en-dashes, em-dashes)
        cleaned_answer = answer.strip().replace("–", "-").replace("—", "-")
        user_answer = int(cleaned_answer)
    except ValueError:
        user_answer = None
    return user_answer


def _gen_question(a, b, operation):
    question = ""
    correct_answer = 0
    if operation == _Operation.Addition:
        question = f"{a} + {b} = "
        correct_answer = a + b
    elif operation == _Operation.Subtraction:
        question = f"{a} - {b} = "
        correct_answer = a - b
    return correct_answer, question


def _use_failed(database, max_session_problems, session_problems_count):
    failed_samples_count = sum(len(item) for item in database["incorrect"])
    if failed_samples_count == 0:
        use_failed = False
    else:
        use_failed = True
        if failed_samples_count < max_session_problems - session_problems_count:
            use_failed = random.random() < 0.5
    return use_failed


def addition_subtraction_testing(app, database):
    _init_db(database)
    com_interface = app.get_com_interface()
    config = app.get_config()["addition_subtraction"]

    num_digits = config.get("digits", 2)
    max_session_problems = config.get("max_checks", 100)

    com_interface.clear()
    com_interface.dialog(
        f"Перевіряємо додавання та віднімання.\n"
        f"Числа будуть з {num_digits} цифр. "
        "Нажми 'q', щоб завершити тестування."
    )

    session_problems_count = sum(len(lst) for lst in database["correct_done"])
    com_interface.dialog(_get_status_message(database))

    while True:
        if session_problems_count >= max_session_problems:
            com_interface.dialog(
                f"Оуоу. Здається ти все вивчив. Ти зроби {session_problems_count} прикладів. Ти супер крутий."
            )
            break

        if _use_failed(database, max_session_problems, session_problems_count):
            # Pick failed sample weighted by failure count
            incorrect_candidates = []
            weights = []
            for op_idx, op_dict in enumerate(database["incorrect"]):
                for values, count in op_dict.items():
                    incorrect_candidates.append((op_idx, *values))
                    weights.append(count)

            operation, a, b = random.choices(incorrect_candidates, weights=weights, k=1)[0]
        else:
            operation = _Operation.get_operation()
            a = _generate_number(num_digits)
            b = _generate_number(num_digits)

        correct_answer, question = _gen_question(a, b, operation)
        answer = com_interface.input(question)
        if answer.lower() in ["q", "й"]:
            break

        user_answer = _get_user_answer(answer)
        if user_answer is not None and user_answer == correct_answer:
            com_interface.dialog("Правильно!")
            _add_correct(database, operation, (a, b))

            if (a, b) not in database["incorrect"][operation]:
                session_problems_count += 1

            com_interface.dialog(_get_status_message(database))
        else:
            com_interface.dialog(f"Не правильно. Правильна відповідь: {correct_answer}")
            _add_incorrect(database, operation, (a, b))

    com_interface.dialog("Тестування завершено! Гарно попрацював!")
