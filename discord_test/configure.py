# discord test - configure
from typing import Optional
from discord_test.types_ import Config

import os
import json


__all__ = ["LANGUAGES", "load_config", "write_config"]


LANGUAGES = ["en", "ja"]


def _check_config_file() -> bool:
    # Checks if config file exists.
    return (os.path.isdir(".discord_test")
        and os.path.isfile(".discord_test/config.json"))


def load_config() -> Config:
    "Loads config."
    if _check_config_file():
        with open(".discord_test/config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def write_config(config: Optional[Config] = None) -> None:
    "Writes config data to config file."
    if not os.path.isdir(".discord_test"):
        os.mkdir(".discord_test")
    if config is None:
        config = {}

    with open(".discord_test/config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
