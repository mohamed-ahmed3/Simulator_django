from rest_framework import serializers
from .models import *

import logging


class SeasonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalityComponentDetails
        fields = [
            'amplitude',
            'phase_shift',
            'frequency_type',
            'frequency_multiplier'
        ]


class ConfigurationSerializer(serializers.ModelSerializer):
    seasonality_components = SeasonalitySerializer(many=True, source='seasons')

    class Meta:
        model = Configuration
        fields = [
            'frequency',
            'noise_level',
            'trend_coefficients',
            'missing_percentage',
            'outlier_percentage',
            'cycle_component_amplitude',
            'cycle_component_frequency',
            'seasonality_components'
        ]

    def create(self, validated_data):
        seasonality_data = validated_data.pop('seasons', [])
        configuration, created = Configuration.objects.get_or_create(**validated_data)

        for season_data in seasonality_data:
            SeasonalityComponentDetails.objects.get_or_create(config=configuration, **season_data)

        return configuration


logger = logging.getLogger(__name__)


class SimulatorSerializer(serializers.ModelSerializer):
    end_date = serializers.DateTimeField(allow_null=True, required=False)
    data_size = serializers.IntegerField(allow_null=True, required=False)
    datasets = ConfigurationSerializer(many=True, source='configurations')

    def create(self, validated_data):
        configurations_data = validated_data.pop('configurations', [])
        simulator, created = Simulator.objects.get_or_create(**validated_data)

        for config_data in configurations_data:
            seasonality_data = config_data.pop('seasons', [])
            configuration, created = Configuration.objects.get_or_create(simulator=simulator, **config_data)

            for season_data in seasonality_data:
                SeasonalityComponentDetails.objects.get_or_create(config=configuration, **season_data)

        return simulator

    def validate(self, data):
        end_date = data.get('end_date')
        data_size = data.get('data_size')

        if end_date is None and data_size is None:
            raise serializers.ValidationError("Either 'end_date' or 'data_size' should have a value, but not both.")

        if end_date is not None and data_size is not None:
            raise serializers.ValidationError("Choose either 'end_date' or 'data_size', but not both.")

        return data

    class Meta:
        model = Simulator
        fields = [
            'name',
            'start_date',
            'end_date',
            'data_size',
            'use_case_name',
            'time_series_type',
            'producer_type',
            'process_id',
            'metadata',
            'status',
            'datasets'
        ]
