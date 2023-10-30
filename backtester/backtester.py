import numpy as np
import pandas as pd
from source.settings import Settings
from source.trading_strategy import Strategy


class Backtester:
    def __init__(self) -> None:
        settings = Settings()
        self.trade_volume = settings.trade_volume
        self.trading_fees = 1 - (settings.trading_fees / 100)

    def run_tester(self, df: pd.DataFrame) -> dict:
        total_profit = 0
        total_loss = 0
        contracts_negative = 0
        contracts_positive = 0

        for i in range(2, len(df) - 1):
            signal = Strategy().apply_strategy(df.iloc[i-2:i], df.iloc[i-2:i]["rsi_up"], df.iloc[i-2:i]["rsi_down"])

            if signal.get("action") and signal.get("side") == "SELL":
                start_wallet = np.multiply(self.trade_volume, self.trading_fees)
                current_coins = np.divide(start_wallet, signal.get("entry_price"))

                for j in range(i + 1, len(df)):
                    if df["close"][j] < signal.get("tp"):
                        close_wallet = np.multiply(current_coins, df["close"][j])
                        clear_profit = np.subtract(start_wallet, close_wallet)
                        close_profit = np.multiply(np.add(clear_profit, start_wallet), self.trading_fees) - self.trade_volume

                        total_profit += close_profit
                        contracts_positive += 1
                        print("SELL, poss: ", contracts_positive, df["open_time"][i])
                        break

                    if df["close"][j] > signal.get("sl"):
                        close_wallet = np.multiply(current_coins, df["close"][j])
                        clear_loss = np.subtract(close_wallet, start_wallet)
                        close_loss = self.trade_volume - np.multiply(np.subtract(start_wallet, clear_loss), self.trading_fees)

                        total_loss -= close_loss
                        contracts_negative -= 1
                        break

            elif signal.get("action") and signal.get("side") == "BUY":
                start_wallet = np.multiply(self.trade_volume, self.trading_fees)
                current_coins = np.divide(start_wallet, signal.get("entry_price"))

                for j in range(i + 1, len(df)):
                    if df["close"][j] > signal.get("tp"):
                        close_wallet = np.multiply(current_coins, df["close"][j])
                        clear_profit = np.subtract(close_wallet, start_wallet)
                        close_profit = np.multiply(np.add(clear_profit, start_wallet), self.trading_fees) - self.trade_volume

                        total_profit += close_profit
                        contracts_positive += 1
                        print("BUY, pos: ", contracts_positive, df["open_time"][i])
                        break

                    if df["close"][j] < signal.get("tp"):
                        close_wallet = np.multiply(current_coins, df["close"][j])
                        clear_lose = np.subtract(start_wallet, close_wallet)
                        close_lose = self.trade_volume - np.multiply(np.subtract(start_wallet, clear_lose), self.trading_fees)

                        total_loss -= close_lose
                        contracts_negative += 1

        return {
            "total_profit": total_profit,
            "total_loss": total_loss,
            "contracts_positive": contracts_positive,
            "contracts_negative": contracts_negative,
        }
