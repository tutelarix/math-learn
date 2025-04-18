import logging
from enum import IntEnum

import click

from common.Database import DatabaseID
from common.application import Application
from common.communication_interface import CommunicationInterface
from common.general.logger import logger
from practice.multiplication_table import multi_table


class MainOptions(IntEnum):
    MultiplicationTable = 0
    AdditionSubtraction = 1
    Exit = 2


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
    com_interface.dialog("Привіт Вовчик! Давай потренуємось.")

    op_index = -1
    ops = ["Табличка множення", "Додавання/Віднімання", "Вихід"]
    while op_index != MainOptions.Exit:
        com_interface.dialog("Вибери з опцій нижче, що хочеш потренувати.")
        op_index = com_interface.select(ops)
        com_interface.clear()
        com_interface.dialog(f"Ти вибрав: {ops[op_index]}.")

        if op_index == MainOptions.MultiplicationTable:
            multi_table(app, db.get_data(DatabaseID.MultiplicationTable))
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
