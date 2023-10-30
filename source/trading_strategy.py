import pandas as pd


class Strategy:

    """
    The module provides trading stradigy basad on CCI-indicator and RSI bands
    """

    @staticmethod
    def apply_strategy(
        df: pd.DataFrame,
        rsi_up_band: pd.Series,
        rsi_down_band: pd.Series
    ) -> dict:

        """
        Implementing trading stratagy

        Returns:
            _type_: dictionary with all necessary points
        """

        if (
            df["close"].iloc[-1] > rsi_up_band.iloc[-1] and
            df["close"].iloc[-2] < rsi_up_band.iloc[-2] and
            df["cci"].iloc[-1] > 120
        ):
            entry_price = df["close"].iloc[-1]
            signal = {
                "action": True,
                "side":  "SELL",
                "entry_price": entry_price,
                "tp": entry_price * 0.989,
                "sl": entry_price * 1.005,
            }

        elif (df["close"].iloc[-1] < rsi_down_band.iloc[-1] and
              df["close"].iloc[-2] > rsi_down_band.iloc[-2] and
              df["cci"].iloc[-1] < -100):
            entry_price = df["close"].iloc[-1]
            signal = {
                "action": True,
                "side":  "BUY",
                "entry_price": entry_price,
                "tp": entry_price * 1.01,
                "sl": entry_price * 0.96,
            }

        else:
            signal = {"action": False}

        return signal
