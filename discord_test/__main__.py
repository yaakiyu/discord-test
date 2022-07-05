# discord test - cli interface
import discord_test
import json


def main() -> None:
    print(f"Discord Test version {discord_test.__version__} by yaakiyu loading...")
    config = discord_test.load_config()
    if not config["language"] in discord_test.configure.LANGUAGES:
        config["language"] = discord_test.configure.LANGUAGES[0]
    
    # load language file
    with open("./languages/{}.json".format(config["language"]), "r") as f:
        language = json.load(f)

    if "default_mode" not in config:
        ...


if __name__ == '__main__':
    main()
