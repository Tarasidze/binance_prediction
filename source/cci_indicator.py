import os
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
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
        _, ax = plt.subplots(2, sharex=True)
        ax[0].plot(df["close"])
        ax[0].legend(loc="upper left")
        ax[1].plot(df["cci"])
        ax[1].legend(loc="upper left")
        plt.suptitle("__--__sdasd__--__")
        plt.show()
