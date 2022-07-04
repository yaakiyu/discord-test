# discord test - cli interface
import sys
import discord_test


def main() -> None:
    print(f"Discord Test version {discord_test.__version__} by yaakiyu loading...")
    discord_test.load_config()


if __name__ == '__main__':
    main()
    sys.exit(0)
