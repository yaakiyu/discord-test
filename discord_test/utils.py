# Discord Test - Utilities

from typing import Generator

def split_list(list_, number: int) -> Generator[list, None, None]:
    "Splits list into multiple lists."
    for i in range(0, len(list_), number):
        yield list_[i:i+number]
