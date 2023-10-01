import numpy as np


class Outliers:
    @staticmethod
    def add_outliers(data, percentage_outliers=0.05):
        """
        Add outliers to the time series data.

        Parameters:
            data (numpy.ndarray): The time series data.
            percentage_outliers (float): The percentage of outliers to add (e.g., 0.2 for 20%).

        Returns:
            numpy.ndarray: The time series data with outliers.
        """
        # data = pd.Series(data)
        num_outliers = int(len(data) * percentage_outliers)
        outlier_indices = np.random.choice(len(data), num_outliers)
        # data_with_outliers = pd.Series(data.copy())
        data_with_outliers = data.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask