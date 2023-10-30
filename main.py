import json
from source.binance_api_manager import BinanceApiManager
from source.rsi_indicator import RsiLbIndicator
from source.cci_indicator import CCIInicator

from backtester.backtester import Backtester


def main():
    am = BinanceApiManager()

    df = am.get_klines_from_api()

    # am.seve_data_to_file(df=df)
    # df = am.get_data_from_file()

    rsi_up_band, rsi_down_band = RsiLbIndicator().calculate_rsi_bands_lb(df)
    df["rsi_up"] = rsi_up_band
    df["rsi_down"] = rsi_down_band
    df = CCIInicator().calculate_cci(df)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    am.seve_data_to_file(df=df)

    data_dict = Backtester().run_tester(df)

    json.dump(data_dict, open("result.json", "w"))

    print(data_dict)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Something went wrong, error: ", exc)
