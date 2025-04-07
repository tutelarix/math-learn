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
