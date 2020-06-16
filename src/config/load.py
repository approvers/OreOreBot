from typing import Dict, Union
import json


def load_config() -> Dict[str, Dict[str, Union[str, int]]]:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config
