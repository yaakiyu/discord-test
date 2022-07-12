# RT type hints

from typing import TypedDict, Literal


class Config(TypedDict, total=False):
    "Config data"
    language: Literal["ja", "en"]

    # Defaults
    default_guild: int
    default_channel: int
    default_user: int
    default_mode: str

    # TOKEN
    token: str
