import uuid

from django.db import models
from django.core.exceptions import ValidationError


class Simulator(models.Model):
    """
    This class defines the schema of the simulator table in the database.

    attributes:
        name (str): The name of the simulator.
        start_date (datetime): The start date for data generation.
        end_date (datetime, optional): The end date for data generation (optional).
        data_size (int, optional): The size of generated data (optional, default is 0).
        use_case_name (str): The name of the use case associated with the simulator.
        time_series_type (str): The type of time series (Multiplicative or Additive).
        producer_type (str): The type of data producer (Kafka or CSV file).
        process_id (int): The unique identifier for the simulator.
        metadata (str, optional): Additional metadata (optional, default is None).
        status (str): The current status of the simulator (Submitted, Running, Succeeded, or Failed).
        datasets (ManyToManyField): Related configurations for data generation.
    """
    time_series_type_choices = (("Multiplicative", "multiplicative"), ("Additive", "additive"))
    producer_type_choices = (("Kafka", "kafka"), ("CSV", "csv file"))
    status_choices = (
        ("Submitted", "submitted"), ("Running", "running"), ("Succeeded", "succeeded"), ("Failed", "failed"))

    name = models.CharField(max_length=50, default='simulator', unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    data_size = models.IntegerField(blank=True, null=True, default=0)
    use_case_name = models.CharField(max_length=200)
    time_series_type = models.CharField(max_length=50, choices=time_series_type_choices)
    producer_type = models.CharField(max_length=20, choices=producer_type_choices)
    process_id = models.AutoField(primary_key=True)
    metadata = models.CharField(max_length=100, editable=False, default=None, null=True)
    status = models.CharField(max_length=100, choices=status_choices, editable=False, default='Submitted')

    datasets = models.ManyToManyField('Configuration', related_name='configs', default=None)


class Configuration(models.Model):
    """
    This class defines the schema of the Configuration table in the database.

    attributes:
        frequency (str): The frequency of data points (e.g., '1D' for daily, '1H' for hourly).
        noise_level (int): The noise level in the generated data.
        trend_coefficients (int, optional): The number of trend coefficients (optional, default is 0).
        missing_percentage (int, optional): The percentage of missing data points (optional, default is 0).
        outlier_percentage (int, optional): The percentage of outlier data points (optional, default is 0).
        cycle_component_amplitude (int, optional): The amplitude of the cycle component (editable, null, default is 0).
        cycle_component_frequency (int): The frequency of the cycle component.
        simulator (ForeignKey): The associated simulator for data generation.
        seasonality_components (ManyToManyField): Related seasonality component details.
        """
    frequency_choice = (("1D","1D"),("10T","10T"),("30T","30T"),("1H","1H"), ("6H","6H"), ("8H","8H"))
    frequency = models.CharField(max_length=20, choices=frequency_choice)
    noise_level = models.IntegerField()
    trend_coefficients = models.IntegerField(default=0)
    missing_percentage = models.IntegerField(default=0)
    outlier_percentage = models.IntegerField(default=0)
    cycle_component_amplitude = models.IntegerField(editable=False, null=True, default=0)
    cycle_component_frequency = models.IntegerField()

    simulator = models.ForeignKey(Simulator, related_name='configurations', on_delete=models.CASCADE, default=None)
    seasonality_components = models.ManyToManyField('SeasonalityComponentDetails', related_name='seasons', default=None)


class SeasonalityComponentDetails(models.Model):
    """
    This class defines the schema of the Configuration table in the database.

    attributes:
        amplitude (int): The amplitude of the seasonality component.
        phase_shift (float): The phase shift of the seasonality component.
        frequency_type (str): The type of frequency for the seasonality component
                             (e.g., 'Daily', 'Weekly', 'Monthly').
        frequency_multiplier (float): The multiplier for the frequency of the seasonality component.
        config (ForeignKey): The associated configuration for data generation.
    """
    frequency_type_choices = (("Daily", "daily"), ("Weekly", "weekly"), ("Monthly", "monthly"))
    amplitude = models.IntegerField()
    phase_shift = models.FloatField(max_length = 10)
    frequency_type = models.CharField(max_length=20, choices=frequency_type_choices)
    frequency_multiplier = models.FloatField(max_length=10)

    config = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='seasons', default=None)
