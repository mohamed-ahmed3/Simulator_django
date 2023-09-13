from rest_framework import serializers
from .models import *


class SeasonalitySerializer(serializers.ModelSerializer):
    """
    This class defines the serialization fields for the
    SeasonalityComponentDetails model.
    """
    class Meta:
        model = SeasonalityComponentDetails
        fields = [
            'amplitude',
            'phase_shift',
            'frequency_type',
            'frequency_multiplier'
        ]


class ConfigurationSerializer(serializers.ModelSerializer):
    """
    This class defines the serialization fields for the
    Configuration model. It assigns the SeasonalitySerializer to
    the seasonality_components field.
    """
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

    """
    This function overrides the create function in the base class.
    It pops the data from the seasonality_components field.
    
    arguments:
        validated_data: dict
        
    return:
        configuration: Configuration
    """
    def create(self, validated_data):
        seasonality_data = validated_data.pop('seasons', [])
        configuration, created = Configuration.objects.get_or_create(**validated_data)

        for season_data in seasonality_data:
            SeasonalityComponentDetails.objects.get_or_create(config=configuration, **season_data)

        return configuration



class SimulatorSerializer(serializers.ModelSerializer):
    """
    This class defines the serialization fields for the
    Simulator model. It assigns the ConfigurationSerializer to
    the datasets field.
    """
    end_date = serializers.DateTimeField(allow_null=True, required=False)
    data_size = serializers.IntegerField(allow_null=True, required=False)
    datasets = ConfigurationSerializer(many=True, source='configurations')

    """
    This function overrides the create function in the base class.
    It pops the data from the seasonality_components field and datasets field.

    arguments:
        validated_data: dict

    return:
        simulator: Simulator
    """
    def create(self, validated_data):
        configurations_data = validated_data.pop('configurations', [])
        simulator, created = Simulator.objects.get_or_create(**validated_data)

        for config_data in configurations_data:
            seasonality_data = config_data.pop('seasons', [])
            configuration, created = Configuration.objects.get_or_create(simulator=simulator, **config_data)

            for season_data in seasonality_data:
                SeasonalityComponentDetails.objects.get_or_create(config=configuration, **season_data)

        return simulator

    """
    This function overrides the validate function from the base class.
    It validates that one of end_date or data_size should be present.
    
    arguments:
        data: dict
        
    return:
        data: dict
    """
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
