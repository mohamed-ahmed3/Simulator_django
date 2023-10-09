import unittest
from django.test import TestCase
from rest_framework.test import APIClient

from simulator_api.serializers import *


class TestSeasonalitySerializer(TestCase):
    """
    This class tests the serialization of the seasonality model.
    It sets up the data needed for the seasonality model.

    methods:
        test_seasonality_serializer
    """
    def setUp(self) -> None:
        self.client = APIClient()

        self.valid_data = {
            'amplitude': 2,
            'phase_shift': 3,
            'frequency_type': 'Daily',
            'frequency_multiplier': 2.0}

    def test_seasonality_serializer(self):
        """
        This method tests the successful serialization of the seasonality model.
        It asserts if the serializer is valid or not.
        """
        serializer = SeasonalitySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())


class TestConfiguraionSerializer(TestCase):
    """
    This class tests the serialization of the configuration model.
    It sets up the data needed for the configuration model.

    methods:
        test_configuration_serializer
    """
    def setUp(self) -> None:
        self.client = APIClient()

        self.valid_data = {
            'frequency': '1D',
            'noise_level': 2,
            'trend_coefficients': 6,
            'missing_percentage': 10,
            'outlier_percentage': 20,
            'cycle_component_amplitude': 1,
            'cycle_component_frequency': 3,
            'seasonality_components': [
                {
                    'amplitude': 2,
                    'phase_shift': 3,
                    'frequency_type': 'Daily',
                    'frequency_multiplier': 2.0
                },
                {
                    'amplitude': 3,
                    'phase_shift': 0,
                    'frequency_type': 'Weekly',
                    'frequency_multiplier': 2.1
                }
            ]
        }

    def test_configuration_serializer(self):
        """
        This method tests the successful serialization of the configuration model.
        It asserts if the serializer is valid or not.
        """
        serializer = ConfigurationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())


class TestSimulatorSerializer(TestCase):
    """
    This class tests the serialization of the simulator model.
    It sets up the data needed for the simulator model.

    methods:
        test_simulator_serializer
    """
    def setUp(self) -> None:
        self.client = APIClient()

        self.valid_data = {"name": "simulator4",
                           "start_date": "2025-01-01 00:00:00",
                           "end_date": "2026-01-01 00:00:00",
                           "use_case_name": "test3",
                           "time_series_type": "Multiplicative",
                           "producer_type": "Kafka",
                           "datasets": [
                               {"frequency": "1D",
                                "noise_level": 2,
                                "trend_coefficients": 6,
                                "missing_percentage": 10,
                                "outlier_percentage": 20,
                                "cycle_component_frequency": 3,
                                "seasonality_components": [
                                    {"amplitude": 2,
                                     "phase_shift": 3,
                                     "frequency_type": "Daily",
                                     "frequency_multiplier": 2.0},
                                    {"amplitude": 3,
                                     "phase_shift": 0,
                                     "frequency_type": "Weekly",
                                     "frequency_multiplier": 2.1}]}]}

    def test_simulator_serializer(self):
        """
        This method tests the successful serialization of the simulator model.
        It asserts if the serializer is valid or not.
        """
        serializer = SimulatorSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())


if __name__ == '__main__':
    unittest.main()
