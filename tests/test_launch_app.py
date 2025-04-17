import unittest
from unittest.mock import patch

from common.communication_interface import CommunicationInterface
from common.communication_interface.empty_interface import EmptyInterface
from launch_app import MainOptions, launch_app


class TestLaunchApp(unittest.TestCase):
    def test_launch_app(self):
        with patch.object(EmptyInterface, "select", return_value=MainOptions.Exit):
            launch_app(com_interface_type=CommunicationInterface.Empty)
            launch_app(is_clear_db=True, com_interface_type=CommunicationInterface.Empty)


if __name__ == "__main__":
    unittest.main()
