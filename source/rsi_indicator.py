import pandas as pd
import numpy as np
import talib as ta
from source.settings import Settings


class RsiLbIndicator:

    """
    The module converts RSI Bands [LazyBear] pine-script to python code
    """

    def __init__(self) -> None:

        """
        initialize object using settings json file
        """

        settings = Settings()

        self.ob_level = settings.rsi_ob_level
        self.os_level = settings.rsi_os_level
        self.length = settings.rsi_length

    @staticmethod
    def _calculate_aus(src, ep) -> pd.Series:
        """calculate apper line of rsi lazy bear

        Args:
            src (_type_): _description_
            ep (_type_): _description_

        Returns:
            pd.Series: _description_
        """

        diff = src - src.shift(1)
        positive_diff = diff.where(diff > 0, 0)

        return positive_diff.ewm(span=ep, adjust=False).mean()

    @staticmethod
    def _calculate_adc(src: pd.Series, ep: int) -> pd.Series:

        """
        calculate apper line of rsi lazy bear

        Args:
            src (_type_): pandas series
            ep (_type_): period

        Returns:
            pd.Series: _description_
        """
        diff = src.shift(1) - src
        positive_diff = diff.where(diff > 0, 0)

        return positive_diff.ewm(span=ep, adjust=False).mean()

    def calculate_rsi_bands_lb(self, df: pd.DataFrame) -> pd.Series:

        """
        Main logic of script, based on source code.

        Args:
            df (pd.DataFrame): data frame for analyzing

        Returns:
            pd.Series: upper and down line
        """

        src = df["close"]
        ep = 2 * self.length - 1

        auc = ta.EMA(np.maximum(src - np.roll(src, 1), 0), ep)
        adc = ta.EMA(np.maximum(np.roll(src, 1) - src, 0), ep)

        x1 = (self.length - 1) * (adc * self.ob_level
                                 / (100-self.ob_level) - auc)
        ub = np.where(x1 >= 0, src + x1, src + x1 * (100 - self.ob_level)
                      / self.ob_level)

        x2 = (self.length - 1) * (adc * self.os_level
                                  / (100 - self.os_level) - auc)
        db = np.where(x2 >= 0, src + x2, src + x2 * (100 - self.os_level)
                      / self.os_level)

        ds_up = pd.Series(ub)
        ds_down = pd.Series(db)

        return ds_up, ds_down
