from pathlib import Path

from common.Database import Database
from common.communication_interface import CommunicationInterface
from common.communication_interface.console_interace import ConsoleInterface
from common.communication_interface.empty_interface import EmptyInterface


class Application:
    """
    Application class to hold all helpful objects.
    """

    def __init__(
        self,
        com_interface_type: CommunicationInterface,
    ):
        """
        :param com_interface_type: type of communication interface
        """
        self._set_com_interface(com_interface_type)
        self._config = {"max_num": 7}
        self._database = Database(Path(__file__).parent)

    def get_com_interface(self):
        """
        :return: current communication interface for the application
        """
        return self._com_interface

    def get_config(self):
        """
        :return: application config
        """
        return self._config

    def get_database(self):
        """
        :return: application database
        """
        return self._database

    def _set_com_interface(self, com_interface_type):
        if com_interface_type == CommunicationInterface.Empty:
            self._com_interface = EmptyInterface()
        elif com_interface_type == CommunicationInterface.Console:
            self._com_interface = ConsoleInterface()
        else:
            raise ValueError(f"Not supported communication interface {com_interface_type}")
