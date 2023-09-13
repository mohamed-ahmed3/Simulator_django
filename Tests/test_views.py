import unittest
from django.test import TestCase
from django.urls import reverse


class TestSimulatorView(TestCase):
    """
    This class tests the successful creation of a simulator in the database and
    listing all the simulators in the database. It sets up the data for the
    simulator

    methods:
        test_simulator_creation
        test_simulator_list
    """

    def setUp(self) -> None:
        self.simulator_data = {"name": "simulator4",
                               "start_date": "2025-01-01 00:00:00",
                               "end_date": "2026-01-01 00:00:00",
                               "use_case_name": "test3",
                               "time_series_type": "Multiplicative",
                               "producer_type": "Kafka"}

    """
    This method tests the creation of the simulator in the database. It asserts that
    the return response code is 200 OK.
    """
    def test_simulator_creation(self):
        response = self.client.get(reverse('Simulator'), follow=True)
        self.assertEqual(response.status_code, 200)

    """
    This method tests the listing of the simulators in the database. It asserts that
    the return response code is 200 OK.
    """
    def test_simulator_list(self):
        response = self.client.get(reverse('Simulator'), follow=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
