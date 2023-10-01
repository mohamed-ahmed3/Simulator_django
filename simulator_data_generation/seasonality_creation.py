from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

class Seasonality(ABC):
    """
    Abstract class to add seasonality

    methods:
        add_seasonality: abstract method
    """

    @abstractmethod
    def add_seasonality(cls, data, seasonality, season_type):
        pass


class WeeklySeasonality(Seasonality):

    def add_seasonality(cls, data, seasonality, season_type):
        """
        Add weekly seasonality component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').
            season_type

        Returns:
            numpy.ndarray: The seasonal component of the time series.

        """
        if seasonality == "exist":  # Weekly Seasonality
            seasonal_component = np.sin(2 * np.pi * data.dayofweek / 7)
            seasonal_component += 1 if season_type == 'multiplicative' else 0
        else:
            seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
        return pd.Series(seasonal_component)


class DailySeasonality(Seasonality):

    def add_seasonality(cls, data, seasonality, season_type):
        """
        Add daily seasonality component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').

        Returns:
            numpy.ndarray: The seasonal component of the time series.
        """
        if seasonality == "exist":  # Daily Seasonality
            seasonal_component = np.sin(2 * np.pi * data.hour / 24)
            seasonal_component += 1 if season_type == 'multiplicative' else 0
        else:
            seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
        return pd.Series(seasonal_component)
