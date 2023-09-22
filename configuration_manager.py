from abc import ABC, abstractmethod
import sqlite3

import yaml
import json
from datetime import datetime

from simulator_api.models import Simulator


class ConfigurationManagerCreator:
    def __init__(self, source: str, simulator_name):
        """
        Initializes the configuration manager instance.

        Parameters:
            source: The source of the data. Can be yaml file or json file
        """
        self.source = source
        self.simulator_name = simulator_name

    @classmethod
    def create(cls, source: str, simulator_name):
        """
        Creates an instance from the chosen source.

        Parameters:
            source: The source of the data. Can be yaml file or json file

        """
        if source.endswith('.yml'):
            return YamlConfigurationManager(source)

        elif source.endswith('.json'):
            return JsonConfigurationManager(source)

        else:
            return DatabaseReader(source, simulator_name)


class ConfigurationManager(ABC):
    """
    An abstract class that provides a configuration manager framework.
    methods:
        _init_: Initializes the configuration manager instance.
        create: Factory method to create an instance of a specific configuration manager.
        read: Abstract method for reading configuration data from a source.

    """

    def __init__(self, source: str):
        """
        Initializes the configuration manager instance.

        Parameters:
            source: The source of the data. Can be yaml file or json file
        """
        self.source = source
        self.configs = self.read()

    @abstractmethod
    def read(self):
        pass

    @property
    def start_date(self):
        """
        Gets the start_date from the file

        return:
            start_date
        """
        return self.configs['start_date']

    @property
    def frequencies(self):
        """
        Gets the frequencies from the file

        return:
            frequencies
        """
        return self.configs['frequencies']

    @property
    def daily_seasonality_options(self):
        """
        Gets the daily_seasonality_options from the file

        return:
            daily_seasonality_options
        """
        return self.configs['daily_seasonality_options']

    @property
    def weekly_seasonality_options(self):
        """
        Gets the weekly_seasonality_options from the file

        return:
            weekly_seasonality_options
        """
        return self.configs['weekly_seasonality_options']

    @property
    def noise_levels(self):
        """
        Gets the noise_levels from the file

        return:
            noise_levels
        """
        return self.configs['noise_levels']

    @property
    def trend_levels(self):
        """
        Gets the trend_levels from the file

        return:
            trend_levels
        """
        return self.configs['trend_levels']

    @property
    def cyclic_periods(self):
        """
        Gets the cyclic_periods from the file

        return:
            cyclic_periods
        """
        return self.configs['cyclic_periods']

    @property
    def time_series_type(self):
        """
        Gets the data_types from the file

        return:
            data_types
        """
        return self.configs['time_series_type']

    @property
    def percentage_outliers_options(self):
        """
        Gets the percentage_outliers_options from the file

        return:
            percentage_outliers_options
        """
        return self.configs['percentage_outliers_options']

    @property
    def data_size(self):
        """
        Gets the data_sizes from the file

        return:
            data_sizes
        """
        return self.configs['data_size']


class YamlConfigurationManager(ConfigurationManager):
    """
    Concrete class to implement the abstract class when it is yaml file

    methods:
        read
    """

    def read(self):
        """
        read yaml file

        return:
            data
        """
        with open(self.source) as f:
            data = yaml.safe_load(f)

        return data


class JsonConfigurationManager(ConfigurationManager):
    def read(self):
        """
        read json file

        return:
            data
        """
        with open(self.source) as f:
            jsondata = f.read()
            data = json.loads(jsondata)

            date_str = data['start_date']
            date_format = '%Y-%m-%d'
            date_obj = datetime.strptime(date_str, date_format)
            data['start_date'] = date_obj

        return data


class DatabaseReader(ConfigurationManager):
    def __init__(self, source: str, simulator_name):
        self.source = source
        self.simulator_name = simulator_name
        self.configs = self.read()

    def read(self):

        try:
            simulator = Simulator.objects.get(name=self.simulator_name)
        except Simulator.DoesNotExist:
            return None

        simulator_data = {
            'name': simulator.name,
            'start_date': simulator.start_date,
            'end_date':simulator.end_date,
            'data_size': simulator.data_size,
            'use_case_name':simulator.use_case_name,
            'time_series_type':simulator.time_series_type,
            'producer_type':simulator.producer_type,
            'process_id':simulator.process_id,
            'status':simulator.status,
            'metadata':simulator.metadata,
            'configurations': []
        }

        configurations_data = []

        for configuration in simulator.configurations.all():
            config_data = {
                'frequency': configuration.frequency,
                'noise_level': configuration.noise_level,
                'trend_coefficients': configuration.trend_coefficients,
                'missing_percentage':configuration.missing_percentage,
                'outlier_percentage': configuration.outlier_percentage,
                'cycle_component_amplitude':configuration.cycle_component_amplitude,
                'cycle_component_frequency': configuration.cycle_component_frequency,
                'seasons': []
            }

            for seasonality_component in configuration.seasons.all():
                seasonality_data = {
                    'amplitude':seasonality_component.amplitude,
                    'phase_shift':seasonality_component.phase_shift,
                    'frequency_type': seasonality_component.frequency_type,
                    'frequency_multiplier':seasonality_component.frequency_multiplier
                }
                config_data['seasons'].append(seasonality_data)

            configurations_data.append(config_data)

        simulator_data['configurations']=configurations_data

        # Move the following code here to ensure it has access to self.simulator_name
        frequencies = [config_data['frequency'] for config_data in configurations_data]
        noise_level = [config_data['noise_level'] for config_data in configurations_data]
        trends = [config_data['trend_coefficients'] for config_data in configurations_data]
        cycles = [config_data['cycle_component_frequency'] for config_data in configurations_data]
        outliers = [config_data['outlier_percentage'] for config_data in configurations_data]

        daily_seasonality_options = []
        weekly_seasonality_options = []

        for config_data in configurations_data:
            for season_data in config_data['seasons']:
                if season_data['frequency_type'] == 'Daily':
                    daily_seasonality_options.append("exist")
                    weekly_seasonality_options.append("none")
                elif season_data['frequency_type'] == 'Weekly':
                    daily_seasonality_options.append("none")
                    weekly_seasonality_options.append("exist")

        simulator_data['configurations'] = configurations_data
        simulator_data['frequencies'] = frequencies
        simulator_data['daily_seasonality_options'] = daily_seasonality_options
        simulator_data['weekly_seasonality_options'] = weekly_seasonality_options
        simulator_data['noise_levels'] = noise_level
        simulator_data['trend_levels'] = trends
        simulator_data['cyclic_periods'] = cycles
        simulator_data['percentage_outliers_options'] = outliers

        return simulator_data
