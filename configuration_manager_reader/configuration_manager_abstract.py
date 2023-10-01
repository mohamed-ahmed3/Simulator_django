from abc import ABC, abstractmethod


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