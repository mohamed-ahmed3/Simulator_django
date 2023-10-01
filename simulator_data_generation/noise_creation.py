import numpy as np
import pandas as pd


class Noise:
    @staticmethod
    def add_noise(data, noise_level):
        """
        Add noise component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            noise_level (str): The magnitude of noise ('No Noise', 'Small Noise', 'Intermediate Noise', 'Large Noise').

        Returns:
            numpy.ndarray: The noise component of the time series.
        """
        if noise_level == "small":
            noise_level = 0.1
            # noise = np.random.normal(0, 0.05, len(data))
        elif noise_level == "large":
            noise_level = 0.3
            # noise = np.random.normal(0, 0.1, len(data))
        else:  # No Noise
            noise_level = 0

        noise = np.zeros_like(data)
        for i in range(len(data)):
            noise[i] = np.random.normal(0, abs(data[i]) * noise_level) if noise_level > 0 else 0
        return pd.Series((data + noise)[:, 0])