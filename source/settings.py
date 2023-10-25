import json


class Settings:
    
    """
    Object for using settings.json file
    """
    
    __slots__ = (
        "script_version",
        "script_name",
        "rsi_ob_level",
        "rsi_os_level",
        "rsi_length",
        "interval_minutes",
        "period_years",
        "cci_period",
        "data_file",
        "symbol",
        "outputs_catalogue"
    )
    
    def __init__(self) -> None:

        """
        The function gets all settings attributes from the file
        """
                
        try:
            settings_file = "settings.json" 
              
            with open(settings_file, "r") as file_obj:
                script_settings = json.load(file_obj)
                
            for script_setting_key, scrip_setting_value in script_settings.items():
                setattr(self, script_setting_key, scrip_setting_value)
                
            list(getattr(self, attr) for attr in self.__slots__)
                
        
        # TODO:  write exceptions to the logger file 
        except FileExistsError:
            print("Config argument found, but there is no file. Exception: ", exc)
            exit(-1)
        except AttributeError as exc:
            print("Wrong setting provided or missing in the config file, Exception: ", exc)
            exit(-1) 
