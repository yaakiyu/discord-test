# discord test - cli interface
import discord_test

import importlib
import json


def main() -> None:
    print(f"Discord Test version {discord_test.__version__} by yaakiyu loading...")
    config = discord_test.load_config()

    import discord

    if not config["language"] in discord_test.configure.LANGUAGES:
        config["language"] = discord_test.configure.LANGUAGES[0]

    # 言語ファイル読み込み
    with open(f"./languages/{config['language']}.json",
              "r", encoding="utf-8") as file:
        print_data = json.load(file)

    print(print_data["welcome"])
    run_file = input("file Path? ")
    try:
        module = importlib.import_module(
            run_file.replace(".py", "").replace("/", ".").replace("\\", ".")
        )
    except ImportError:
        return print(print_data["error_file"])


if __name__ == '__main__':
    main()
