import os
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from source.settings import Settings


class CCIInicator:
    def __init__(self) -> None:
        settings = Settings()

        self.period = settings.cci_period
        self.file_name = settings.data_file
        self.catalogue = settings.outputs_catalogue

    def get_data_from_file(self, file_name: str = None) -> pd.DataFrame | None:
        if file_name is None:
            file_name = self.file_name

        file_path = os.path.join(os.getcwd(), self.catalogue, file_name)

        try:
            df = pd.read_csv(file_path)

        except FileNotFoundError as exc:
            print("File not found: ", exc)
            return None

        return df

    def calculate_cci(self, df: pd.DataFrame = None) -> pd.Series:

        """
        Calculate CCI-indicator using talib library

        Args:
            df (pd.DataFrame, optional): data-frame should
            contain "high", "low", "close" series

        Returns:
            pd.DataFrame: pandas Series cci-indicator
        """

        if df is None:
            df = self.get_data_from_file()

        return ta.CCI(df["high"], df["low"], df["close"], self.period)

    def show_plot(self, df: pd.DataFrame) -> None:
        x_axis_date = df["open_time"]
        rsi_up = df["rsi_up"]
        rsi_down = df["rsi_down"]

        plt.plot(x_axis_date, rsi_up, label="rsi_up")
        plt.legend()

        plt.plot(x_axis_date, rsi_down, label="rsi down")
        plt.title("RSI Indicator")
        plt.legend()
        plt.xticks(rotation=20)

        num_ticks = 7
        x_ticks = x_axis_date[::len(x_axis_date)//num_ticks]
        plt.xticks(x_ticks)

        plt.show()
