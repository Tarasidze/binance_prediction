import numpy as np
import pandas as pd
from source.settings import Settings
from source.trading_strategy import Strategy
from source.logger import LoggerCsv


class Backtester:
    def __init__(self) -> None:
        settings = Settings()
        self.trade_volume = settings.trade_volume
        self.trading_fees = 1 - (settings.trading_fees / 100)
        self.trading_fees_short = 1 + settings.trading_fees
        
        self.total_profit = 0
        self.total_loss = 0
        self.contracts_negative = 0
        self.contracts_positive = 0

    def run_tester(self, df: pd.DataFrame) -> dict:
        start_wallet = np.multiply(self.trade_volume, self.trading_fees)

        for i in range(2, len(df) - 1):
            signal = Strategy().apply_strategy(df.iloc[i-2:i])

            if signal.get("action") and signal.get("side") == "SELL":
                current_coins = np.divide(start_wallet, signal.get("entry_price"))
                self.calculate_short(df, i, current_coins, start_wallet, signal)                

            elif signal.get("action") and signal.get("side") == "BUY":
                current_coins = np.divide(start_wallet, signal.get("entry_price"))
                self.calculate_long(df, i, current_coins, signal)
                print("BUY, pos: ", self.contracts_positive, df["open_time"][i])

        return {
            "total_profit": self.total_profit,
            "total_loss": self.total_loss,
            "contracts_positive": self.contracts_positive,
            "contracts_negative": self.contracts_negative,
            "profit_factor": np.divide(self.total_profit, -self.total_loss),
            "win_rate": np.divide(self.contracts_positive, np.add(self.contracts_positive, self.contracts_negative))
        }

    def calculate_short(self, df, index, current_coins, start_wallet, signal):
        for j in range(index + 1, len(df)):
                if df["close"][j] <= signal.get("tp"):                    
                    clear_profit = np.subtract(start_wallet, np.multiply(current_coins, df["close"][j]))
                    close_wallet = np.multiply(self.trading_fees, np.add(start_wallet, clear_profit))
                    profit = np.subtract(self.trade_volume, close_wallet)
                                        
                    if profit >=0:
                        self.total_profit += profit
                        self.contracts_positive += 1
                    else:
                        self.total_loss += profit
                        self.contracts_negative += 1
                    
                    LoggerCsv().logg_info_message(
                        {
                           "open_time": df["open_time"].iloc[index],
                           "open_price": df["close"].iloc[index],
                           "close_time": df["open_time"].iloc[j],
                           "close_price": df["close"].iloc[j],
                           "trade_type": "SHORT",
                           "profit": profit
                        }
                    )
                    
                    return

                if df["close"][j] > signal.get("sl"):
                    loss = np.subtract(start_wallet, np.multiply(current_coins, df["close"][j]))
                    close_wallet = np.multiply(np.subtract(start_wallet, loss), self.trading_fees)
                    clear_loss = np.subtract(self.trade_volume, close_wallet)
                    
                    self.total_loss += clear_loss
                    self.contracts_negative += 1
                    
                    LoggerCsv().logg_info_message(
                        {
                           "open_time": df["open_time"].iloc[index],
                           "open_price": df["close"].iloc[index],
                           "close_time": df["open_time"].iloc[j],
                           "close_price": df["close"].iloc[j],
                           "trade_type": "SHORT",
                           "profit": -1 * clear_loss
                        }
                    )
                    
                    return

    def calculate_long(self, df, index, current_coins, signal):
        for j in range(index + 1, len(df)):
                if df["close"][j] >= signal.get("tp"):
                    close_wallet = np.multiply(np.multiply(current_coins, df["close"][j]), self.trading_fees)                                        
                    profit = np.subtract(close_wallet, self.trade_volume)

                    if profit >= 0:
                        self.total_profit += profit
                        self.contracts_positive += 1
                    else:
                        self.total_loss += profit
                        self.contracts_negative += 1

                    LoggerCsv().logg_info_message(
                        {
                           "open_time": df["open_time"].iloc[index],
                           "open_price": df["close"].iloc[index],
                           "close_time": df["open_time"].iloc[j],
                           "close_price": df["close"].iloc[j],
                           "trade_type": "LONG",
                           "profit": profit
                        }
                    )

                    return

                if df["close"][j] < signal.get("sl"):
                    close_wallet = np.multiply(np.multiply(current_coins, df["close"][j]), self.trading_fees)
                    clear_loss = self.trade_volume - close_wallet

                    self.total_loss += clear_loss
                    self.contracts_negative += 1

                    LoggerCsv().logg_info_message(
                        {
                           "open_time": df["open_time"].iloc[index],
                           "open_price": df["close"].iloc[index],
                           "close_time": df["open_time"].iloc[j],
                           "close_price": df["close"].iloc[j],
                           "trade_type": "LONG",
                           "profit": -1 * clear_loss
                        }
                    )

                    return
