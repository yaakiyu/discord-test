# discord Test - Interpreter

from typing import Union

from discord.ext import commands
import discord

from aioconsole import aprint, ainput


async def ask_id(
    bot: Union[commands.Bot, discord.Client],
    mode: str, function: str
) -> int:
    "Asks any ID."
    await aprint(f"Please type {mode} to go on.")
    while True:
        id_ = await ainput(f"{mode}: ")
        if not id_.isdigit():
            await aprint(f"Invalid {mode}.")
            continue
        obj = getattr(bot, function)(int(id_))
        if not obj:
            await aprint(f"{mode} not found.")
            continue
        return int(id_)


async def main(bot: Union[commands.Bot, discord.Client], config: dict) -> None:
    "Runs interpreter."
    await bot.wait_until_ready()
    print("Discord Test - Interpreter")
    # ユーザーIDを入力。 TODO: これら全てdefaultをconfigから読み込む
    await ask_id(bot, "User ID", "get_user")
    # サーバーIDを入力。
    await ask_id(bot, "Guild ID", "get_guild")
    # チャンネルIDを入力。
    await ask_id(bot, "Channel ID", "get_channel")
