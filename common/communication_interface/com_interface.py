from typing import List


class ComInterface:
    """
    Basic communication interface
    """

    def dialog(self, text):
        """
        Print multi-line text
        :param text: text
        """
        raise NotImplementedError

    def clear(self):
        """
        Clear any visible text
        """
        raise NotImplementedError

    def input(self, text):
        """
        Print multi-line text and ask input
        :param text:
        :return: resulted text
        """
        raise NotImplementedError

    def select(self, options: List):
        """
        Interactive options selection
        :param options: list of options
        :return: index of selected option from the list
        """
        raise NotImplementedError
