import unittest
from django.test import TestCase
from django.urls import reverse


class TestSimulatorView(TestCase):

    def setUp(self) -> None:
        self.simulator_data = {"name": "simulator4",
                               "start_date": "2025-01-01 00:00:00",
                               "end_date": "2026-01-01 00:00:00",
                               "use_case_name": "test3",
                               "time_series_type": "Multiplicative",
                               "producer_type": "Kafka"}

    def test_simulator_creation(self):
        response = self.client.get(reverse('Simulator'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_simulator_list(self):
        response = self.client.get(reverse('Simulator'), follow=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
