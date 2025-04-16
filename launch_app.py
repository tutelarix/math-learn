import logging
from enum import IntEnum

import click
from beaupy import select

from common.Database import DatabaseID
from common.application import Application
from common.communication_interface import CommunicationInterface
from common.general.logger import logger
from math_ops.math_testing_ops import multi_table, division_multi_table


class MainOptions(IntEnum):
    Multiplication = 0
    Deletion = 1
    AdditionSubtraction = 2


def launch_app(is_clear_db=False, com_interface_type=CommunicationInterface.Console):
    """
    Launch application
    :param is_clear_db: clear database file
    :param com_interface_type: type of communication interface
    """
    app = Application(com_interface_type=com_interface_type)
    db = app.get_database()
    db.load_db(is_clear_db)
    com_interface = app.get_com_interface()

    com_interface.clear()
    com_interface.dialog("Привіт Вовчик! Давай потренуємо математику.")

    op_index = -1
    ops = ["Табличка множення", "Ділення", "Вихід"]
    while op_index != len(ops) - 1:
        com_interface.dialog("Вибери з опцій нижче, що хочеш потренувати.")
        operation = select(ops, cursor="🢧", cursor_style="cyan")
        com_interface.clear()
        com_interface.dialog(f"Ти вибрав: {operation}.")

        op_index = ops.index(operation)
        if op_index == MainOptions.Multiplication:
            multi_table(app, db.get_data(DatabaseID.MultiplicationTable))
        elif op_index == MainOptions.Deletion:
            division_multi_table(app, db.get_data(DatabaseID.MultiplicationTable))
        elif op_index == MainOptions.AdditionSubtraction:
            pass

        db.save_db()
        com_interface.dialog("")


@click.command()
@click.option("--verbose", "-V", is_flag=True, help="Print debug output.")
@click.option("--clear-db", is_flag=True, help="Clear database")
def main(verbose=False, clear_db=False):
    if not verbose:
        logger.level = logging.CRITICAL

    launch_app(is_clear_db=clear_db)


if __name__ == "__main__":
    main()
