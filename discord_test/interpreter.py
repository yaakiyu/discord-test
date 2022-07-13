# discord Test - Interpreter

from typing import Union, Any

from discord.ext import commands
import discord

from aioconsole import aprint, ainput

from discord_test.types_ import Config
from discord_test.utils import split_list


__all__ = ["main", "messaging"]


async def main(bot: Union[commands.Bot, discord.Client], config: Config) -> None:
    "Runs interpreter."
    await aprint("Discord Test - Interpreter")
    await aprint("Waiting until ready...")
    await bot.wait_until_ready()

    # モード選択
    first_mode = True
    while True:
        if "default_mode" in config and first_mode:
            await aprint("loading default mode from config file...")
            mode = config["default_mode"]
            first_mode = False
        else:
            await aprint(
                "Please select mode.",
                "`test` - normal testing mode.",
                "`chat` - Only for chatting.",
                "`settings` - Settings.",
                sep="\n"
            )
            mode = await ainput("Mode: ")
        if mode in ["test", "chat"]:
            await selecting(bot, config)
        elif mode == "settings":
            pass
        else:
            await aprint("Invalid mode.")


async def messaging(
    bot: Union[discord.Client, commands.Bot],
    channel: discord.TextChannel, user: discord.Member, config: Config,
    mode: str
) -> None:
    "Messaging on a discord channel."
    async for message in channel.history(limit=10):
        await aprint(f">{message.author}: {message.content.splitlines()[0]}")

    message_task = bot.loop.create_task(bot_wait_for_loop(bot, channel, config))
    input_task = bot.loop.create_task(wait_for_send_loop(bot, user, channel, config, mode))
    await input_task

    await aprint("Closing...")
    message_task.cancel()


async def _ask_id(
    bot: Union[commands.Bot, discord.Client, discord.Guild],
    mode: str, function: str
) -> Any:
    # Asks any ID.
    await aprint(f"Please type {mode} to go on.")
    await aprint("> ")
    objects = tuple(split_list(getattr(bot, f"{function[4:]}s"), 10) or ())
    index = 0

    while True:
        # objectsを10個ずつ表示するシステム。
        if index != -1:
            await aprint("\033[2A" + "\n".join(
                "{0.name}({0.id})".format(m) for m in objects[index]
            ))
            if index == len(objects) - 1:
                index = -1
            else:
                index += 1
        id_ = await ainput("")
        if id_ is None:
            continue
        if not id_.isdigit():
            await aprint(f"Invalid {mode}.")
            continue
        try:
            obj = objects[index - 1][int(id_)]
        except IndexError:
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
        message = await bot.wait_for(
            "message",
            check=lambda m: m.channel == channel and m.author != bot.user
        )
        try:
            content = message.content.splitlines()[0]
        except IndexError:
            content = message.content or "None"
        await aprint(f">{message.author}: {content}")


async def wait_for_send_loop(
    bot: Union[commands.Bot, discord.Client], user: discord.Member,
    channel: discord.TextChannel, config: Config, mode: str = "test"
) -> None:
    "Forever waits for input and sends it."
    while True:
        try:
            content = await ainput("> ")
        except (EOFError, KeyboardInterrupt):
            return
        if mode == "test":
            msg = await channel.send(content)
            msg.author = user
            bot.dispatch("message", msg)
        else:
            await channel.send(content) 


async def selecting(
    bot: Union[commands.Bot, discord.Client], config: Config,
    mode: str = "test"
) -> None:
    "Select server / channel / user."
    first_guild = True  # サーバー選択が初めてかどうかを表す。初めての場合のみdefaultでのバイパスを行う。
    while True:
        # サーバーを選択。
        if "default_guild" in config and first_guild:
            await aprint("getting guild from config file...")
            first_guild = False
            gu = bot.get_guild(config.get("default_guild", 0))
            if not gu:
                await aprint("Guild not found.")
                continue
            guild = gu
        else:
            try:
                guild: discord.Guild = await _ask_id(bot, "Guild ID", "get_guild")
            except (EOFError, KeyboardInterrupt):
                break

        first_channel = True  # チャンネル選択が初めてかどうかを表す。
        while True:
            # チャンネルを選択。
            if "default_channel" in config and first_channel:
                await aprint("getting channel from config file...")
                first_channel = False
                ch = guild.get_channel(config.get("default_channel", 0))
                if not isinstance(ch, discord.TextChannel):
                    await aprint("channel not found.")
                    continue
                else:
                    channel = ch
            else:
                try:
                    channel: discord.TextChannel = await _ask_id(
                        guild, "Channel ID", "get_channel"
                    )
                except (EOFError, KeyboardInterrupt):
                    break

            first_user = True  # ユーザー選択が初めてかどうかを表す。
            while True:
                # ユーザーを選択。
                if "default_user" in config and first_user:
                    await aprint("getting user from config file...")
                    first_user = False
                    us = guild.get_member(config.get("default_user", 0))
                    if not isinstance(us, discord.Member):
                        await aprint("user not found.")
                        continue
                    user = us
                try:
                    user: discord.Member = await _ask_id(
                        guild, "User ID", "get_member"
                    )
                except (EOFError, KeyboardInterrupt):
                    break

                # メッセージングを開始。
                await messaging(bot, channel, user, config, mode)
