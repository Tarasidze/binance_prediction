import os
import logging
from source.settings import Settings


class Logger:
    def __init__(self) -> None:
        settings = Settings()

        self.file_name = settings.loger_file
        self.catalogue = settings.outputs_catalogue

        self.file_path = os.path.join(os.getcwd(), self.catalogue, self.file_name)
        
        
    def logg_info_message(self, message):
        logging.basicConfig(filename=self.file_path, level=logging.INFO)
        logging.info(message)