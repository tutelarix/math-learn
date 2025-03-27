import logging
import unittest
from unittest.mock import patch

from common.general.logger import logger, handle_exception


class TestLogger(unittest.TestCase):
    def test_logger_pos(self):
        with patch.object(logging.StreamHandler, "emit", return_value=None) as mock_method:
            test_msg = "Critical test log"
            logger.critical(test_msg)

            # Check streaming to console is called
            mock_method.assert_called()
            # Check correct data prepared
            self.assertEqual(mock_method.call_args[0][0].msg, test_msg)

    def test_handle_exception_pos(self):
        @handle_exception
        def func_raising_exception():
            raise ValueError("Test logging raising exception")

        with self.assertRaises(ValueError):
            with patch.object(logger, "critical", return_value=None) as mock_method:
                func_raising_exception()

                # Check logger critical called
                mock_method.assert_called()
