import unittest

from common.Database import Database
from common.application import Application
from common.communication_interface import CommunicationInterface
from common.communication_interface.console_interace import ConsoleInterface
from common.communication_interface.empty_interface import EmptyInterface


class TestApplication(unittest.TestCase):
    def test_application(self):
        app = Application(CommunicationInterface.Console)
        self.assertTrue(isinstance(app.get_com_interface(), ConsoleInterface))

        with self.assertRaises(ValueError):
            Application(CommunicationInterface.GUI)

        app = Application(CommunicationInterface.Empty)
        com_interface = app.get_com_interface()
        self.assertTrue(isinstance(com_interface, EmptyInterface))
        self.assertTrue(isinstance(app.get_config(), dict))
        self.assertTrue(isinstance(app.get_database(), Database))


if __name__ == "__main__":
    unittest.main()
