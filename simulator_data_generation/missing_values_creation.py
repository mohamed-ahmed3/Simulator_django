import numpy as np


class MissingValues:
    @staticmethod
    def add_missing_values(data, percentage_missing=0.05):
        """
        Add missing values to the time series data within a specified date range.

        Parameters:
            data (numpy.ndarray): The time series data.
            percentage_missing (Float): percentage of missing value.

        Returns:
            numpy.ndarray: The time series data with missing values.
        """
        num_missing = int(len(data) * percentage_missing)
        missing_indices = np.random.choice(len(data), size=num_missing, replace=False)

        data_with_missing = data.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing