# discord Test - Interpreter

from typing import Union, Any

from discord_test.types_ import Config
from discord_test.utils import split_list

from discord.ext import commands
import discord

from aioconsole import aprint, ainput


__all__ = ["main"]


async def main(bot: Union[commands.Bot, discord.Client], config: Config) -> None:
    "Runs interpreter."
    await bot.wait_until_ready()
    await aprint("Discord Test - Interpreter")
    # TODO: モード選択を追加。
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

    message_task = bot.loop.create_task(bot_wait_for_loop(bot, channel, config))
    input_task = bot.loop.create_task(wait_for_send_loop(bot, user, channel, config))
    await input_task

    await aprint("Closing...")
    message_task.cancel()


async def _ask_id(
    bot: Union[commands.Bot, discord.Client, discord.Guild],
    mode: str, function: str
) -> Any:
    # Asks any ID.
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
    bot: Union[commands.Bot, discord.Client], 
    channel: discord.TextChannel, config: Config
) -> None:
    "Forever waits for event and prints it."
    while True:
        message = await bot.wait_for("message", check=lambda m: m.channel == channel)
        await aprint(f">{message.author}: {message.content.splitlines()[0]}")


async def wait_for_send_loop(
    bot: Union[commands.Bot, discord.Client], user: discord.Member,
    channel: discord.TextChannel, config: Config
) -> None:
    while True:
        try:
            message = await ainput("> ")
        except (EOFError, KeyboardInterrupt):
            break
        await channel.send(message)

async def test_mode(bot: Union[commands.Bot, discord.Client], config: Config) -> None:
    "Test mode."
    first_guild = True

    while True:
        # サーバーを選択。
        if "default_guild" in config and first_guild:
            first_guild = False
            guild = bot.get_guild(config.get("default_guild", 0))  # type: ignore
            if not guild:
                continue
        else:
            guild: discord.Guild = await _ask_id(bot, "Guild ID", "get_guild")

        first_channel = True
        while True:
            # チャンネルを選択。
            if "default_channel" in config and first_channel:
                first_channel = False
                channel = guild.get_channel(config.get("default_channel", 0))  # type: ignore
                if not channel:
                    continue
            else:
                channel: discord.TextChannel = await _ask_id(
                    guild, "Channel ID", "get_channel"
                )

