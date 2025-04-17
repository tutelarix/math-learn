from typing import List

from beaupy import select
from rich.console import Console

from common.communication_interface.com_interface import ComInterface


class ConsoleInterface(ComInterface):
    """
    Implements communication interface with console input/output.
    """

    def __init__(self):
        self._console = Console(color_system="windows")

    def dialog(self, text):
        """
        Print multi-line text
        :param text: text
        """
        if isinstance(text, str):
            self._console.print(text)
        else:
            raise ValueError(f"Not supported type: {type(text)}")

    def clear(self):
        """
        Clear any visible text
        """
        self._console.clear()

    def input(self, text):
        """
        Print multi-line text and ask input
        :param text:
        :return: resulted text
        """
        if isinstance(text, str):
            return self._console.input(text)

        raise ValueError(f"Not supported type: {type(text)}")

    def select(self, options: List):
        """
        Interactive options selection
        :param options: list of options
        :return: index of option from the list
        """
        selected_option = select(options, cursor="🢧", cursor_style="cyan")
        return options.index(selected_option)
