import os
import logging
from source.settings import Settings


class Logger:
    def __init__(self) -> None:
        settings = Settings()

        self.file_name = settings.loger_file
        self.catalog = settings.outputs_catalogue

        self.file = os.path.join(os.getcwd(), self.catalog, self.file_name)

    def logg_info_message(self, message):
        logging.basicConfig(filename=self.file, level=logging.INFO)
        logging.info(message)
