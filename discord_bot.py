import asyncio
import logging
import os

import discord
from discord import app_commands
from python_aternos import Client as AternosClient
from python_aternos.atserver import AternosServer
from python_aternos.aterrors import ServerStartError

logging.basicConfig(level=logging.INFO)

aternos = AternosClient()

server_id = os.environ["ATERNOS_SERVER_ID"]

bot = discord.Client(intents=discord.Intents.none())
commands = app_commands.CommandTree(bot)
aternos_lock = asyncio.Lock()


def fetch_server() -> AternosServer:
    aternos.login(
        os.environ["ATERNOS_USERNAME"],
        os.environ["ATERNOS_PASSWORD"],
    )
    server = aternos.account.get_server(server_id)
    server.fetch()
    return server


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
        async with aternos_lock:
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


@commands.command(name="status", description="Check the configured Aternos server")
async def status(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        async with aternos_lock:
            server = await asyncio.to_thread(fetch_server)
        await interaction.followup.send(
            f"**{server.subdomain}** is **{server.status}**.",
            ephemeral=True,
        )
    except Exception:
        logging.exception("Failed to fetch Aternos server status")
        await interaction.followup.send(
            "Couldn't retrieve the server status. Check the bot's logs.",
            ephemeral=True,
        )


@commands.command(name="serverinfo", description="Show details for the configured Aternos server")
async def serverinfo(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        async with aternos_lock:
            server = await asyncio.to_thread(fetch_server)

        embed = discord.Embed(
            title=server.subdomain,
            description=f"Status: **{server.status}**",
            color=discord.Color.green() if server.is_java else discord.Color.blue(),
        )
        embed.add_field(name="Address", value=server.address, inline=False)
        embed.add_field(
            name="Edition",
            value="Java" if server.is_java else "Bedrock",
            inline=True,
        )
        embed.add_field(
            name="Software",
            value=f"{server.software} {server.version}",
            inline=True,
        )
        embed.add_field(
            name="Players",
            value=f"{server.players_count}/{server.slots}",
            inline=True,
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception:
        logging.exception("Failed to fetch Aternos server information")
        await interaction.followup.send(
            "Couldn't retrieve server information. Check the bot's logs.",
            ephemeral=True,
        )


@bot.event
async def on_ready() -> None:
    await commands.sync()
    print(f"Bot is online as {bot.user}")


bot.run(os.environ["DISCORD_TOKEN"])