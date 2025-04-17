from typing import List

from common.communication_interface.com_interface import ComInterface
from common.general.logger import logger


class EmptyInterface(ComInterface):
    """
    Implements communication interface that do nothing.
    Convenient for testing of math functions that depends on communication interface with user.
    """

    def __init__(self):
        self._input_result = ""
        self._select_result = -1

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
        logger.debug(f"{text}. Return: {self._input_result}")
        return self._input_result

    def set_input_result(self, input_result):
        """
        Set intput result to be returned from input function
        :param input_result: input result
        """
        self._input_result = input_result

    def select(self, options: List):
        """
        Interactive options selection
        :param options: list of options
        :return: index of selected option from the list
        """
        logger.debug(f"Select from options: {options}. Return: {options[self._select_result]}")
        return self._select_result

    def set_select_result(self, select_option: int):
        """
        Set select option to be returned from select option
        :param select_option: selected option
        """
        self._select_result = select_option
