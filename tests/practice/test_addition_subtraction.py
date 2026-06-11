import unittest
from unittest.mock import patch

from common.Database import DatabaseID
from common.application import Application
from common.communication_interface import CommunicationInterface
from practice.addition_subtraction import _generate_number, _Operation, addition_subtraction_testing


class TestAdditionSubtraction(unittest.TestCase):
    def test_generate_number_bounds(self):
        # Hardcoded expected ranges for 1, 2 and 3 digits
        test_cases = [(1, 0, 9), (2, 10, 99), (3, 100, 999)]

        for digits, expected_min, expected_max in test_cases:
            for _ in range(50):  # Run multiple times to cover random distribution
                val = _generate_number(digits)
                self.assertGreaterEqual(val, expected_min)
                self.assertLessEqual(val, expected_max)

    def test_add_subtraction_positive_and_negative_flow(self):
        # Initialize application and clear database for isolation
        app = Application(com_interface_type=CommunicationInterface.Empty)
        com_interface = app.get_com_interface()
        app.get_database().load_db(is_clear_db=True)
        database = app.get_database().get_data(DatabaseID.AdditionSubtraction)

        # Configure exactly one problem per phase
        # pylint: disable=protected-access
        app._config["addition_subtraction"]["max_checks"] = 1
        app._config["addition_subtraction"]["digits"] = 2
        # pylint: enable=protected-access

        # --- Phase 1: Positive flow (Addition) ---
        with (
            patch(
                "practice.addition_subtraction._Operation.get_operation",
                return_value=_Operation.Addition,
            ),
            patch("practice.addition_subtraction._generate_number", side_effect=[5, 3]),
        ):
            com_interface.set_input_result("8")  # Correct answer for 5 + 3
            addition_subtraction_testing(app, database)

            # Verify positive DB state
            self.assertEqual(len(database["correct_done"][0]), 1)
            self.assertIn((5, 3), database["correct_done"][0])
            self.assertEqual(len(database["incorrect"][0]), 0)

        # --- Phase 2: Negative flow (Subtraction) ---
        # Clear DB to isolate the second phase checks
        app.get_database().load_db(is_clear_db=True)
        database = app.get_database().get_data(DatabaseID.AdditionSubtraction)

        with (
            patch(
                "practice.addition_subtraction._Operation.get_operation",
                return_value=_Operation.Subtraction,
            ),
            patch("practice.addition_subtraction._generate_number", side_effect=[9, 4]),
            patch.object(com_interface, "input", side_effect=["6", "q"]),
        ):  # Wrong answer, then exit
            addition_subtraction_testing(app, database)

            # Verify negative DB state (Subtraction is index 1)
            self.assertEqual(len(database["correct_done"][1]), 0)
            self.assertIn((9, 4), database["incorrect"][1])
            self.assertEqual(database["incorrect"][1][(9, 4)], 1)


if __name__ == "__main__":
    unittest.main()
