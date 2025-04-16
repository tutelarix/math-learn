from common.communication_interface.com_interface import ComInterface
from common.general.logger import logger


class EmptyInterface(ComInterface):
    """
    Implements communication interface that do nothing.
    Convenient for testing of math functions that depends on communication interface with user.
    """

    def __init__(self):
        self._input_result = 0

    def dialog(self, text):
        """
        Print multi-line text
        :param text: text
        """
        logger.debug(text)

    def clear(self):
        """
        Clear any visible text
        """
        logger.debug("Clear")

    def input(self, text):
        """
        Print multi-line text and ask input
        :param text:
        :return: resulted text
        """
        logger.debug(f"{text}. Return {self._input_result}")
        return self._input_result

    def set_input_result(self, input_result):
        self._input_result = input_result
