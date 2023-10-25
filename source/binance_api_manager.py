import os
from dotenv import load_dotenv
import pandas as pd
import mplfinance as mpf
from source.settings import Settings
import datetime
from dateutil.relativedelta import relativedelta
from binance import Client


class BinanceApiManager:
    def __init__(self) -> None:

        """
        Object provides base functionality for Binance API.
        Takes data from API convert to Pandas DataFrame, and return it
        """

        load_dotenv()
        self.apikey = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")

        settings = Settings()

        self.file_name = settings.data_file
        self.interval_minutes = settings.interval_minutes
        self.period_years = settings.period_years
        self.symbol = settings.symbol
        self.catalogue = settings.outputs_catalogue

    def get_klines_from_api(
            self, symbol: str = None, interval: int = None, period: int = None
            ) -> pd.DataFrame:

        """
        The function recieves data from Binance API and return Pandas DataFrame
        Args:
            symbol (str, optional): trade token. Defaults to None.
            interval (int, optional): interval (minutes). Defaults to None.
            period (int, optional): years. Defaults to None.

        Returns:
            pd.DataFrame: ruturns clear data in Pandas format
        """

        if symbol is None:
            symbol = self.symbol
        if interval is None:
            interval = self.interval_minutes
        if period is None:
            period = self.period_years

        start_date = datetime.datetime.now() - relativedelta(years=period)
        start_date_str = start_date.strftime("%d %b %Y")

        client = Client(self.apikey, self.secret_key)
        historical = client.get_historical_klines(
            symbol=symbol,
            interval=Client.KLINE_INTERVAL_1WEEK,
            start_str=start_date_str
            )

        df = pd.DataFrame(historical)

        df = df.rename(columns={
            0: "open_time",
            1: "open",
            2: "high",
            3: "low",
            4: "close",
            5: "volume",
            6: "close_time",
            7: "quote_asset_volume",
            8: "number_of_trades",
            9: "taker_buy_base_asset_volume",
            10: "taker_buy_quote_asset_volume"
            })

        return df

    def seve_data_to_file(
            self, df: pd.DataFrame, file_name: str = None
            ) -> bool:

        """
        The function writes Pandas DataFrame to file
        """
        if file_name is None:
            file_name = self.file_name

        name, extension = file_name.split(".")
        counter = 1
        file_path = os.path.join(os.getcwd(), self.catalogue, file_name)

        while os.path.exists(file_path):
            file_name = f"{name}({counter}).{extension}"
            file_path = os.path.join(os.getcwd(), self.catalogue, file_name)
            counter += 1

        df.to_csv(file_path)

    def get_data_from_file(self, file_name: str = None) -> pd.DataFrame | None:

        """
        The function reads dataframe from file
        """

        if file_name is None:
            file_name = self.file_name

        file_path = os.path.join(os.getcwd(), self.catalogue, file_name)

        try:
            df = pd.read_csv(file_path)

        except FileNotFoundError as exc:
            print("File not found: ", exc)
            return None

        return df

    def show_charts(self, df: pd.DataFrame = None) -> bool:

        """
        The function draws charts based on dataframe,

        Args:
            df (pd.DataFrame, optional): Defaults to None.

        Returns:
            bool: False if file isn't exists
        """

        if df is None:
            try:
                file_path = os.path.join(
                    os.getcwd(), self.catalogue, self.file_name
                    )
                df = pd.read_csv(file_path)

            except (FileExistsError, FileNotFoundError) as exc:
                print("File not found or invalid path: ", exc)
                return False

        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df.set_index("open_time", inplace=True)
        title = f"Chart for {self.symbol}, in last {self.period_years} periods"

        mpf.plot(df, type="candle", volume=True, title=title, style="yahoo")

        return True
