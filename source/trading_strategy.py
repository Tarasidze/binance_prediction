import pandas as pd
import numpy as np


class Strategy:

    """
    The module provides trading stradigy basad on CCI-indicator and RSI bands
    """

    @staticmethod
    def apply_strategy(
        df: pd.DataFrame,
    ) -> dict:

        """
        Implementing trading stratagy
        Args:   df: pandas data-frame
                rsi_up_band: pandas series
                rsi_down_band: pandas series
        Returns:
            dictionary: dictionary with all necessary points
        """

        if (
            df["close"].iloc[-1] > df["rsi_up"].iloc[-1] and
            df["close"].iloc[-2] < df["rsi_up"].iloc[-2] and
            df["cci"].iloc[-1] > 120
        ):
            entry_price = df["close"].iloc[-1]

            signal = {
                "action": True,
                "side":  "SELL",
                "entry_price": entry_price,
                "tp": np.multiply(entry_price, 0.989),
                "sl": np.multiply(entry_price, 1.005),
            }

        elif (df["close"].iloc[-1] < df["rsi_down"].iloc[-1] and
              df["close"].iloc[-2] > df["rsi_down"].iloc[-2] and
              df["cci"].iloc[-1] < -100):
            entry_price = df["close"].iloc[-1]

            signal = {
                "action": True,
                "side":  "BUY",
                "entry_price": entry_price,
                "tp": np.multiply(entry_price, 1.01),
                "sl": np.multiply(entry_price, 0.96),
            }

        else:
            signal = {"action": False}

        return signal
