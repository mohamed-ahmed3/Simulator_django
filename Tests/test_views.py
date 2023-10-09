import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from simulator_api.models import Simulator


class TestSimulatorListing(TestCase):
    """
    This class tests the successful listing all the simulators in the database.
    It sets up the url for the request.

    methods:
        test_simulator_list
    """

    def setUp(self) -> None:
        self.url = reverse("SimulatorListing")

    def test_simulator_list(self):
        """
        This method tests the listing of the simulators in the database. It asserts that
        the return response code is 200 OK.
        """
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)


class TestSimulatorCreation(TestCase):
    """
    This class tests the successful creation of a simulator in the database .
    It sets up the data for the simulator, the client that will send the request,
    and the url.

    methods:
        test_create_simulator_success
        test_create_simulator_failed
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('SimulatorCreation')

    def test_create_simulator_success(self):
        """
        This method tests the successful creation of the simulators in the database. It asserts that
        the return response code is 201 created. It also asserts the response data
        equals the expected.
        """
        simulator_data = {
            "name": "simulator2",
            "start_date": "2020-01-01 00:00:00",
            "end_date": "2026-01-01 00:00:00",
            "use_case_name": "test2",
            "time_series_type": "Multiplicative",
            "producer_type": "Kafka",
            "datasets": [
                {"frequency": "1D",
                 "noise_level": 2,
                 "trend_coefficients": [1, 3, 3],
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
                      "frequency_multiplier": 2.1}]}]

        }

        response = self.client.post(self.url, simulator_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_simulator = Simulator.objects.get(name='simulator2')
        self.assertIsNotNone(created_simulator)

        expected = {'detail': 'Simulator and related data created successfully.'}
        self.assertEqual(response.data, expected)

    def test_create_simulator_failed(self):
        """
        This method tests the failed creation of a simulator. It asserts that
        the return response code is 400 BAD REQUEST.
        """
        invalid_data = {
            "name": 2
        }

        response = self.client.post(self.url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.assertRaises(Simulator.DoesNotExist):
            Simulator.objects.get(name='simulator')


class TestSimulatorRunning(TestCase):
    """
    This class tests the successful running of a simulator.
    It sets up the data for the simulator, the client that will send the request,
    and the url.

    methods:
        test_run_simulator
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('run', kwargs={"simulator_name": "simulator2"})
        self.data = {
            "name": "simulator2",
            "start_date": "2020-01-01 00:00:00",
            "end_date": "2026-01-01 00:00:00",
            "use_case_name": "test2",
            "time_series_type": "Multiplicative",
            "producer_type": "Kafka",
        }

        self.simulator = Simulator.objects.create(**self.data)

    def test_run_simulator(self):
        """
        This method tests running a simulator. It asserts that
        the return response code is 200 OK and the response data equals the expected data.
        """
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, {"simulator2": "Running"})


class TestSimulatorStopping(TestCase):
    """
    This class tests the successful stopping of a simulator.
    It sets up the data for the simulator, the client that will send the request,
    and the url.

    methods:
        test_stop_simulator
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('stop', kwargs={"simulator_name": "simulator2"})
        self.data = {
            "name": "simulator1",
            "start_date": "2020-01-01 00:00:00",
            "end_date": "2026-01-01 00:00:00",
            "use_case_name": "test1",
            "time_series_type": "Multiplicative",
            "producer_type": "Kafka",
        }

        self.simulator = Simulator.objects.create(**self.data)

    def test_stop_simulator(self):
        """
        This method tests stopping a simulator. It asserts that
        the return response code is 200 OK and the response data equals the expected data.
        """
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, {'message': 'simulator2 stopped.'})


if __name__ == '__main__':
    unittest.main()
