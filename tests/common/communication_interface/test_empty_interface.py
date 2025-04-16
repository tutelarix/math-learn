import logging
import unittest
from unittest.mock import patch

from common.communication_interface.empty_interface import EmptyInterface


class TestEmptyInterface(unittest.TestCase):
    def test_empty_interface(self):
        com_interface = EmptyInterface()
        with patch.object(logging.StreamHandler, "emit", return_value=None) as mock_method:
            com_interface.dialog("Test dialog")
            mock_method.assert_called()
            self.assertEqual(mock_method.call_args[0][0].msg, "Test dialog")

        with patch.object(logging.StreamHandler, "emit", return_value=None) as mock_method:
            com_interface.clear()
            mock_method.assert_called()

        input_result = "res"
        with patch.object(logging.StreamHandler, "emit", return_value=None) as mock_method:
            com_interface.set_input_result(input_result)
            self.assertEqual(com_interface.input("Enter res"), input_result)
            mock_method.assert_called()
            self.assertTrue("Enter res" in mock_method.call_args[0][0].msg)


if __name__ == "__main__":
    unittest.main()
