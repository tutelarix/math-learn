import unittest

from common.Database import DatabaseID
from common.application import Application
from common.communication_interface import CommunicationInterface
from practice.multiplication_table import multi_table, _get_mult_table_operation


class TestMultiplicationTable(unittest.TestCase):
    def test_multi_table(self):
        app = Application(com_interface_type=CommunicationInterface.Empty)
        com_interface = app.get_com_interface()
        app.get_database().load_db(is_clear_db=True)
        database = app.get_database().get_data(DatabaseID.MultiplicationTable)

        com_interface.set_input_result("q")
        multi_table(app, database)

    def test_get_mult_table_operation(self):
        # Check order of values, important for saving in database
        values = _get_mult_table_operation([], 1, 10)
        self.assertLess(values[0], values[1])

        # Check values generation
        database = []
        num = 7
        for _ in range(10 - num + 1):
            values = _get_mult_table_operation(database, num, num)
            self.assertIsNotNone(values)
            database.append(values)

        values = _get_mult_table_operation(database, num, num)
        self.assertIsNone(values)


if __name__ == "__main__":
    unittest.main()
