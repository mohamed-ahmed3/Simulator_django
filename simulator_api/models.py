import uuid

from django.db import models
from django.core.exceptions import ValidationError


class SeasonalityComponentDetails(models.Model):
    frequency_type_choices = (("Daily", "daily"), ("Weekly", "weekly"), ("Monthly", "monthly"))
    amplitude = models.CharField(max_length=50)
    phase_shift = models.CharField(max_length=50)
    frequency_type = models.CharField(max_length=20, choices=frequency_type_choices)
    frequency_multiplier = models.FloatField(max_length=10)


class Configuration(models.Model):
    status_choices = (
        ("Submitted", "submitted"), ("Running", "running"), ("Succeeded", "succeeded"), ("Failed", "failed"))
    frequency = models.CharField(max_length=100)
    noise_level = models.CharField(max_length=100)
    trend_coefficients = models.CharField(max_length=100, default=0)
    missing_percentage = models.CharField(max_length=100, default=0)
    outlier_percentage = models.CharField(max_length=100, default=0)
    cycle_component_amplitude = models.CharField(max_length=100)
    cycle_component_frequency = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=status_choices)
    seasonality_components = models.ForeignKey(SeasonalityComponentDetails, on_delete=models.CASCADE, default=None)


class Simulator(models.Model):

    time_series_type_choices = (("Multiplicative", "multiplicative"), ("Additive", "additive"))
    producer_type_choices = (("Kafka", "kafka"), ("CSV", "csv file"))

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    data_size = models.IntegerField(blank=True, default=0, null=True)
    use_case_name = models.CharField(max_length=200)
    time_series_type = models.CharField(max_length=50, choices=time_series_type_choices)
    producer_type = models.CharField(max_length=20, choices=producer_type_choices)
    process_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metadata = models.CharField(max_length=100, editable=False, default=None, null=True)
    datasets = models.ForeignKey('Configuration', on_delete=models.CASCADE, default=None, null=True)

