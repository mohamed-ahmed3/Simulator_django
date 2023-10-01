from simulator_api.models import Simulator
from .configuration_manager_abstract import ConfigurationManager


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
