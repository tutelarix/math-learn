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
