import unittest

from simulator_api.models import *


class TestSimulator(unittest.TestCase):
    """
    A class to test the simulator model. It sets up the environment with simulator data.

    methods:
        test_simulator_creation
    """
    def setUp(self):
        self.simulator_data = {
            "name": "Test Simulator",
            "start_date": "2023-01-01 00:00:00",
            "end_date": "2023-01-31 23:59:59",
            "use_case_name": "Test Use Case",
            "time_series_type": "Multiplicative",
            "producer_type": "Kafka",
            "metadata": "Test Metadata",
            "status": "Submitted"
        }

    """
    This function tests the successful creation of the model. It asserts the equality of 
    some fields such as: name, status, and producer_type.
    """
    def test_simulator_creation(self):
        simulator = Simulator(**self.simulator_data)
        self.assertEqual(simulator.name, "Test Simulator")
        self.assertEqual(simulator.status, "Submitted")
        self.assertEqual(simulator.producer_type, "Kafka")


class TestConfiguration(unittest.TestCase):
    """
    A class to test the configuration model. It sets up the environment with configuration data.

    methods:
        test_configuration_creation
    """
    def setUp(self):
        self.configuration_data = {
            "frequency": "1H",
            "noise_level": 3,
            "trend_coefficients": 3
        }

    """
    This function tests the successful creation of the model. It asserts the equality of 
    some fields such as: frequency, noise_level, and trend_coefficients.
    """

    def test_configuration_creation(self):
        configurator = Configuration(**self.configuration_data)
        self.assertEqual(configurator.frequency, "1H")
        self.assertEqual(configurator.noise_level, 3)
        self.assertEqual(configurator.trend_coefficients, 3)


class TestSeasonality(unittest.TestCase):
    """
    A class to test the seasonality model. It sets up the environment with seasonality data.

    methods:
        test_seasonality_creation
    """
    def setUp(self):
        self.seasonality_data = {
            "amplitude": 2,
            "phase_shift": 3,
            "frequency_type": "Daily"
        }

    """
    This function tests the successful creation of the model. It asserts the equality of 
    some fields such as: amplitude, phase_shift, frequency_type.
    """
    def test_seasonality_creation(self):
        seasonality = SeasonalityComponentDetails(**self.seasonality_data)
        self.assertEqual(seasonality.amplitude, 2)
        self.assertEqual(seasonality.phase_shift, 3)
        self.assertEqual(seasonality.frequency_type, "Daily")


if __name__ == '__main__':
    unittest.main()
