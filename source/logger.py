import os
import csv
import logging
from source.settings import Settings


class LoggHandler:
    pass


class LoggerLog:
    def __init__(self) -> None:
        settings = Settings()

        self.file_name = settings.loger_file
        self.catalog = settings.outputs_catalogue

        self.file = os.path.join(os.getcwd(), self.catalog, self.file_name)

    def logg_info_message(self, message: str) -> None:
        logging.basicConfig(filename=self.file, level=logging.INFO)
        logging.info(message)


class LoggerCsv:
    def __init__(self) -> None:
        settings = Settings()

        self.file_name = settings.loger_file
        self.catalog = settings.outputs_catalogue
        self.file_path = os.path.join(
            os.getcwd(),
            self.catalog,
            self.file_name
        )

    def logg_info_message(self, message: dict, fields: list = None) -> None:

        if fields is None:
            fields = [
                "open_time",
                "open_price",
                "close_time",
                "close_price",
                "trade_type",
                "profit"
            ]

        file_exists = os.path.exists(self.file_path)

        with open(
            self.file_path,
            "a+",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(csv_file, fieldnames=fields)

            if not file_exists:
                writer.writeheader()

            writer.writerow(message)
