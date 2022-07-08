# discord Test - Interpreter

from typing import Union, Any

from discord.ext import commands
import discord

from aioconsole import aprint, ainput


__all__ = ["main"]


async def _ask_id(
    bot: Union[commands.Bot, discord.Client, discord.Guild],
    mode: str, function: str
) -> Any:
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
        return obj


async def bot_wait_for_loop(
    bot: Union[commands.Bot, discord.Client], event: str, 
    channel: discord.TextChannel, config: dict
) -> None:
    pass


async def wait_for_send_loop(
    bot: Union[commands.Bot, discord.Client],
    channel: discord.TextChannel, config: dict
) -> None:
    pass


async def main(bot: Union[commands.Bot, discord.Client], config: dict) -> None:
    "Runs interpreter."
    await bot.wait_until_ready()
    await aprint("Discord Test - Interpreter")
    # サーバーIDを入力。 TODO: これら全てdefaultをconfigから読み込む
    guild: discord.Guild = await _ask_id(bot, "Guild ID", "get_guild")
    # ユーザーIDを入力。
    user: discord.Member = await _ask_id(guild, "User ID", "get_member")
    # チャンネルIDを入力。
    channel: discord.TextChannel = await _ask_id(
        guild, "Channel ID", "get_channel"
    )

    async for message in channel.history(limit=10):
        await aprint(f">{message.author}: {message.content.splitlines()[0]}")

