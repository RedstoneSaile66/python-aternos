import asyncio
import logging
import os

import discord
from discord import app_commands
from python_aternos import Client as AternosClient
from python_aternos.aterrors import ServerStartError

logging.basicConfig(level=logging.INFO)

aternos = AternosClient()

server_id = os.environ["ATERNOS_SERVER_ID"]

bot = discord.Client(intents=discord.Intents.none())
commands = app_commands.CommandTree(bot)


@commands.command(name="start", description="Start the configured Aternos server")
async def start(interaction: discord.Interaction) -> None:

    await interaction.response.defer(ephemeral=True, thinking=True)

    def start_server() -> None:
        aternos.login(
            os.environ["ATERNOS_USERNAME"],
            os.environ["ATERNOS_PASSWORD"],
        )
        aternos.account.get_server(server_id).start(accepteula=False)

    try:
        await asyncio.to_thread(start_server)
        await interaction.followup.send(
            "Aternos accepted the start request. It may still be queued or "
            "need confirmation on Aternos.",
            ephemeral=True,
        )
    except ServerStartError as error:
        await interaction.followup.send(
            f"Aternos refused the start request: {error}",
            ephemeral=True,
        )
    except Exception:
        logging.exception("Failed to start the Aternos server")
        await interaction.followup.send(
            "Something went wrong. Check the bot's PowerShell output.",
            ephemeral=True,
        )


@bot.event
async def on_ready() -> None:
    await commands.sync()
    print(f"Bot is online as {bot.user}")


bot.run(os.environ["DISCORD_TOKEN"])