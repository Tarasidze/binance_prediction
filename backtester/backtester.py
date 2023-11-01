import numpy as np
import pandas as pd
from source.settings import Settings
from source.trading_strategy import Strategy
from source.logger import LoggerCsv


class Backtester:
    def __init__(self) -> None:
        settings = Settings()
        self.trade_volume = settings.trade_volume
        self.trading_fees = 1 - (settings.trading_fees / 100)  # 0.9995
        self.fees_coeff = np.float64(settings.trading_fees / 100)  # 0.0005

        self.long_tp_perc = np.float64(1)
        self.long_sl_perc = np.float64(0.4)
        self.short_tp_perc = np.float64(1.1)
        self.short_sl_perc = np.float64(0.5)

        self.long_tp_coeff = np.divide(self.long_tp_perc, 100)    # 0.01
        self.long_sl_coeff = np.divide(self.long_sl_perc, 100)    # 0.004
        self.short_tp_coeff = np.divide(self.short_tp_perc, 100)  # 0.011
        self.short_sl_coeff = np.divide(self.short_sl_perc, 100)  # 0.005

        self.long_tp_multiplier = np.multiply(
            np.subtract(np.add(1, self.long_tp_coeff), self.fees_coeff),
            self.trading_fees)  # 1.00899525

        self.long_sl_multiplier = np.subtract(
            np.float64(1),
            np.multiply(
                np.subtract(1, self.long_sl_coeff),
                np.square(self.trading_fees)
                )
            )  # 0.00499575

        self.short_tp_multiplier = np.multiply(
            np.add(
                np.multiply(1, self.trading_fees),
                np.subtract(
                    self.trading_fees, np.subtract(1, self.short_tp_coeff)
                    )
                ),
            self.trading_fees
        )  # 1.009495

        self.short_sl_multiplier = np.multiply(
            np.subtract(np.add(1, self.short_sl_coeff), self.trading_fees),
            self.trading_fees
        )  # 0.00549725

        self.long_profit = np.subtract(
            np.multiply(self.trade_volume, self.long_tp_multiplier),
            self.trade_volume
        )
        self.long_loss = np.multiply(self.trade_volume, self.long_sl_multiplier)
        self.short_profit = np.subtract(
            np.multiply(self.trade_volume, self.short_tp_multiplier),
            self.trade_volume
        )
        self.short_loss = np.multiply(self.trade_volume, self.short_sl_multiplier)

        self.total_profit = 0
        self.total_loss = 0
        self.contracts_negative = 0
        self.contracts_positive = 0

    def run_tester(self, df: pd.DataFrame) -> dict:

        for i in range(2, len(df) - 1):
            signal = Strategy().get_signals(df.iloc[i-2:i])

            if signal.get("action") and signal.get("side") == "SELL":
                self.calculate_short(df, i, signal)

            elif signal.get("action") and signal.get("side") == "BUY":
                self.calculate_long(df, i, signal)
                print("BUY, pos: ", self.contracts_positive, df["open_time"][i])

        return {
            "total_profit": self.total_profit,
            "total_loss": self.total_loss,
            "contracts_positive": self.contracts_positive,
            "contracts_negative": self.contracts_negative,
            "profit_factor": np.divide(self.total_profit, self.total_loss),
            "win_rate": np.divide(
                self.contracts_positive,
                np.add(self.contracts_positive, self.contracts_negative)
            )
        }

    def calculate_short(self, df, index, signal):
        for j in range(index + 1, len(df)):
            if df["close"][j] <= signal.get("tp"):

                self.total_profit += self.short_profit
                self.contracts_positive += 1

                LoggerCsv().logg_info_message(
                    {
                        "open_time": signal.get("open_time"),
                        "open_price": signal.get("entry_price"),
                        "close_time": df["open_time"].iloc[j],
                        "close_price": df["close"].iloc[j],
                        "trade_type": "SHORT",
                        "result": "win",
                        "profit": self.short_profit
                    }
                )

                return

            if df["close"][j] > signal.get("sl"):

                self.total_loss += self.short_loss
                self.contracts_negative += 1

                LoggerCsv().logg_info_message(
                    {
                        "open_time": df["open_time"].iloc[index],
                        "open_price": df["close"].iloc[index],
                        "close_time": df["open_time"].iloc[j],
                        "close_price": df["close"].iloc[j],
                        "trade_type": "SHORT",
                        "result": "loss",
                        "profit": -1 * self.short_loss
                    }
                )

                return

    def calculate_long(self, df, index, signal):
        for j in range(index + 1, len(df)):
            if df["close"][j] >= signal.get("tp"):

                self.total_profit += self.long_profit
                self.contracts_positive += 1

                LoggerCsv().logg_info_message(
                    {
                        "open_time": signal.get("open_time"),
                        "open_price": signal.get("entry_price"),
                        "close_time": df["open_time"].iloc[j],
                        "close_price": signal.get("tp"),
                        "result": "win",
                        "trade_type": "LONG",
                        "profit": self.long_profit
                    }
                )

                return

            if df["close"][j] < signal.get("sl"):

                self.total_loss += self.long_loss
                self.contracts_negative += 1

                LoggerCsv().logg_info_message(
                    {
                        "open_time": df["open_time"].iloc[index],
                        "open_price": df["close"].iloc[index],
                        "close_time": df["open_time"].iloc[j],
                        "close_price": df["close"].iloc[j],
                        "trade_type": "LONG",
                        "result": "loss",
                        "profit": -1 * self.long_loss
                    }
                )

                return
