# Discord Test - Utilities

def split_list(list_, n):
    "リストをサブリストに分割して返します。"
    for idx in range(0, len(list_), n):
        yield list_[idx:idx + n]
