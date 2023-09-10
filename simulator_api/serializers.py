from rest_framework import serializers

from .models import *


class SeasonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalityComponentDetails
        fields = [
            'amplitude',
            'phase_shift',
            'frequency_type',
            'frequency_multiplier']


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['frequency'
            , 'noise_level'
            , 'trend_coefficients'
            , 'missing_percentage'
            , 'outlier_percentage'
            , 'cycle_component_amplitude'
            , 'cycle_component_frequency'
            , 'status'
            , 'seasonality_components']

    seasonality_components = SeasonalitySerializer(read_only=True)


class SimulatorSerializer(serializers.ModelSerializer):
    end_date = serializers.DateTimeField(allow_null=True)
    data_size = serializers.IntegerField(allow_null=True)

    datasets = ConfigurationSerializer(read_only=True)

    def validate(self, data):
        end_date = data.get('end_date')
        data_size = data.get('data_size')

        if end_date is None and data_size is None:
            raise ValidationError("Either 'end_date' or 'data_size' should have a value, but not both.")

        if end_date is not None and data_size is not None:
            raise ValidationError("Choose either 'end_date' or 'data_size', but not both.")

        return data

    class Meta:
        model = Simulator
        fields = [
            'start_date',
            'end_date',
            'data_size',
            'use_case_name',
            'time_series_type',
            'producer_type',
            'process_id',
            'metadata',
            'datasets'
        ]
