import uuid

from django.db import models
from django.core.exceptions import ValidationError


class Simulator(models.Model):
    time_series_type_choices = (("Multiplicative", "multiplicative"), ("Additive", "additive"))
    producer_type_choices = (("Kafka", "kafka"), ("CSV", "csv file"))
    status_choices = (
        ("Submitted", "submitted"), ("Running", "running"), ("Succeeded", "succeeded"), ("Failed", "failed"))

    name = models.CharField(max_length=50, default='simulator', unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    data_size = models.IntegerField(blank=True, default=0, null=True)
    use_case_name = models.CharField(max_length=200)
    time_series_type = models.CharField(max_length=50, choices=time_series_type_choices)
    producer_type = models.CharField(max_length=20, choices=producer_type_choices)
    process_id = models.AutoField(primary_key=True)
    metadata = models.CharField(max_length=100, editable=False, default=None, null=True)
    status = models.CharField(max_length=100, choices=status_choices, editable=False, default='Submitted')

    datasets = models.ManyToManyField('Configuration', related_name='configs', default=None)


class Configuration(models.Model):
    frequency_choice = (("1D","1D"),("10T","10T"),("30T","30T"),("1H","1H"), ("6H","6H"), ("8H","8H"))
    frequency = models.CharField(max_length=20, choices=frequency_choice)
    noise_level = models.IntegerField()
    trend_coefficients = models.IntegerField(default=0)
    missing_percentage = models.IntegerField(default=0)
    outlier_percentage = models.IntegerField(default=0)
    cycle_component_amplitude = models.IntegerField(editable=False)
    cycle_component_frequency = models.IntegerField()

    simulator = models.ForeignKey(Simulator, related_name='configurations', on_delete=models.CASCADE, default=None)
    seasonality_components = models.ManyToManyField('SeasonalityComponentDetails', related_name='seasons', default=None)

    def save(self, *args, **kwargs):
        # Access the associated Simulator instance
        simulator = self.simulator

        if simulator.time_series_type == "Multiplicative":
            self.cycle_component_amplitude = 1
        elif simulator.time_series_type == "Additive":
            self.cycle_component_amplitude = 0

        super(Configuration, self).save(*args, **kwargs)


class SeasonalityComponentDetails(models.Model):
    frequency_type_choices = (("Daily", "daily"), ("Weekly", "weekly"), ("Monthly", "monthly"))
    amplitude = models.IntegerField()
    phase_shift = models.IntegerField()
    frequency_type = models.CharField(max_length=20, choices=frequency_type_choices)
    frequency_multiplier = models.FloatField(max_length=10)

    config = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='seasons', default=None)
