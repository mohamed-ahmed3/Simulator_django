import numpy as np


class Cycles:
    @staticmethod
    def add_cycles(data, cyclic_periods, season_type):
        """
        Add cyclic component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            cyclic_periods (str): The type of cyclic periods ('No Cyclic Periods', 'Short Cycles', or 'Long Cycles').

        Returns:
            numpy.ndarray: The cyclic component of the time series.
        """
        if cyclic_periods == "exist":  # Quarterly
            cycle_component = 1 if season_type == 'multiplicative' else 0
            cycle_component += np.sin(2 * np.pi * (data.quarter - 1) / 4)
        else:  # No Cyclic Periods
            cycle_component = 0 if season_type == 'additive' else 1

        return cycle_component
