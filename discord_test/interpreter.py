# discord Test - Interpreter

from typing import Union

from discord.ext import commands
import discord


async def main(bot: Union[commands.Bot, discord.Client], config) -> None:
    "Runs interpreter."
    await bot.wait_until_ready()
    print("Discord Test - Interpreter")
    print()
