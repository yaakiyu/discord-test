# discord test - cli interface
import discord_test

import importlib
import asyncio
import json
import os


def main() -> None:
    print(f"Discord Test version {discord_test.__version__} by yaakiyu loading...")
    config = discord_test.load_config()

    if config.get("language", None) not in discord_test.configure.LANGUAGES:
        config["language"] = discord_test.configure.LANGUAGES[0]  # type: ignore

    # 言語ファイル読み込み
    with open(f"{os.getcwd()}/languages/{config['language']}.json",  # type: ignore
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

    token = input("TOKEN? ")
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(module.bot.start(token))
    asyncio.ensure_future(discord_test.interpreter.main(module.bot, config))
    loop.run_forever()


if __name__ == "__main__":
    main()
