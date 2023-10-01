import pandas as pd


class TimeSeriesGenerator:
    @staticmethod
    def generate_time_series(start_date, end_date, freq):
        """
        Generate a time index (DatetimeIndex) with the specified frequency.

        Parameters:
            start_date (datetime): The start date of the time index.
            end_date (datetime): The end date of the time index.
            freq (str): The frequency for the time index (e.g., '10T' for 10 minutes, '1H' for hourly, 'D' for daily).

        Returns:
            DatetimeIndex: The generated time index.
        """
        date_rng = pd.date_range(start=start_date, end=end_date, freq=freq)
        return date_rng
