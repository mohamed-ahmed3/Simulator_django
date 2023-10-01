import random
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
import json
import requests

from itertools import product

from configuration_manager_reader.configuration_manager_abstract import ConfigurationManager
from simulator_data_generation import cycles_creation, missing_values_creation, noise_creation, outliers_creation, seasonality_creation, time_series_generation, trend_creation


class DataGenerator:
    def __init__(self, configuration_manager: ConfigurationManager):
        """
        This class initializes its attributes based on the provided ConfigurationManager.

        Parameters:
                configuration_manager (ConfigurationManager): An instance of ConfigurationManager
                that holds various configuration parameters.

        Attributes:
            start_date (datetime.datetime): The start date for data generation.
            Frequencies (List[str]): A list of frequency strings.
            daily_seasonality_options (List[...]): A list of daily seasonality options.
            weekly_seasonality_options (List[...]): A list of weekly seasonality options.
            noise_levels (List[...]): A list of noise levels.
            trend_levels (List[...]): A list of trend levels.
            cyclic_periods (List[...]): A list of cyclic periods.
            data_types (List[str]): A list of data types.
            percentage_outliers_options (List[...]): A list of percentage outliers options.
            data_sizes (List[...]): A list of data sizes.
        """
        self.start_date = configuration_manager.start_date
        self.frequencies = configuration_manager.frequencies
        self.daily_seasonality_options = configuration_manager.daily_seasonality_options
        self.weekly_seasonality_options = configuration_manager.weekly_seasonality_options
        self.noise_levels = configuration_manager.noise_levels
        self.trend_levels = configuration_manager.trend_levels
        self.cyclic_periods = configuration_manager.cyclic_periods
        self.time_series_type = configuration_manager.time_series_type
        self.percentage_outliers_options = configuration_manager.percentage_outliers_options
        self.data_size = configuration_manager.data_size

    def generate(self):
        """
        Generate time series data with various configurations and yield data points.
        This generator function creates time series data with multiple combinations of
        configuration parameters, including daily and weekly seasonality, noise levels,
        trends, cyclic patterns, data types, and more. It yields data points in the form
        of dictionaries containing 'value', 'timestamp', and 'anomaly' information.
        Yields:
            A tuple containing two dictionaries:
            - The first dictionary includes 'value' (time series data), 'timestamp' (time index),
                and 'anomaly' (outlier information).
            - The second dictionary includes metadata such as 'id', 'data_type', 'daily_seasonality',
                'weekly_seasonality', 'noise (high 30% - low 10%)', 'trend', 'cyclic_period (3 months)',
                'data_size', 'percentage_outliers', 'percentage_missing', and 'freq'.
        """

        config_params = [
            self.daily_seasonality_options,
            self.weekly_seasonality_options,
            self.noise_levels,
            self.trend_levels,
            self.cyclic_periods,
            self.percentage_outliers_options,
        ]

        counter = 0
        #used the itertools.product to make all the combinations without the need of nested for loops
        for configs in product(*config_params):
            daily_seasonality, weekly_seasonality, noise_level, trend, cyclic_period, percentage_outliers= configs

            for _ in range(16):
                freq = random.choice(self.frequencies)
                counter += 1
                file_name = f"TimeSeries_daily_{daily_seasonality}_weekly_{weekly_seasonality}_noise_{noise_level}_trend_{trend}_cycle_{cyclic_period}_outliers_{int(percentage_outliers * 100)}%_freq_{freq}_size_{self.time_series_type}Days.csv"
                print(f"File '{file_name}' generated.")

                date_rng = time_series_generation.TimeSeriesGenerator.generate_time_series(self.start_date,
                                                                    self.start_date + timedelta(days=self.data_size),
                                                                    freq)

                daily_seasonality_instance = seasonality_creation.DailySeasonality()
                daily_seasonal_component = daily_seasonality_instance.add_seasonality(date_rng, daily_seasonality,
                                                                                      season_type=self.time_series_type)

                weekly_seasonality_instance = seasonality_creation.WeeklySeasonality()
                weekly_seasonal_component = weekly_seasonality_instance.add_seasonality(date_rng, weekly_seasonality,
                                                                                        season_type=self.time_series_type)

                trend_component = trend_creation.Trend.add_trend(date_rng, trend, data_size=self.data_size, data_type=self.time_series_type)
                cyclic_period = "exist"
                cyclic_component = cycles_creation.Cycles.add_cycles(date_rng, cyclic_period, season_type=self.time_series_type)

                if self.time_series_type == 'multiplicative':
                    data = daily_seasonal_component * weekly_seasonal_component * trend_component * cyclic_component
                else:
                    data = daily_seasonal_component + weekly_seasonal_component + trend_component + cyclic_component

                scaler = MinMaxScaler(feature_range=(-1, 1))
                data = scaler.fit_transform(data.values.reshape(-1, 1))
                data = noise_creation.Noise.add_noise(data, noise_level)
                data, anomaly = outliers_creation.Outliers.add_outliers(data, percentage_outliers)
                data = missing_values_creation.MissingValues.add_missing_values(data, 0.05)

                try:
                    url = "http://Apachi_NIFI:8443"
                    data_list = str(data.tolist())
                    date_rng_str = str(date_rng.strftime('%Y-%m-%d %H:%M:%S').tolist())
                    anomaly_list = str(anomaly.tolist())
                    payload = {"value":data_list, "timestamp":date_rng_str, "anomaly":anomaly_list}
                    response = requests.post(url, data=json.dumps(payload))
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print('Error sending data:', e)

                yield ({'value': data, 'timestamp': date_rng, 'anomaly': anomaly},
                       {'id': str(counter) + '.csv',
                        'data_type': self.time_series_type,
                        'daily_seasonality': daily_seasonality,
                        'weekly_seasonality': weekly_seasonality,
                        'noise (high 30% - low 10%)': noise_level,
                        'trend': trend,
                        'cyclic_period (3 months)': cyclic_period,
                        'data_size': self.data_size,
                        'percentage_outliers': percentage_outliers,
                        'percentage_missing': 0.05,
                        'freq': freq})
