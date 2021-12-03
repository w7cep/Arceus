import contextlib
import io
import logging
import os
import asyncio
import aiohttp
import nextcord
import nextcord.ext
from nextcord.ext import commands, tasks
import platform
import config
from urllib.request import urlopen
import json
from pathlib import Path
import utils.json_loader as jl
import random
from utils.mongo import Document

import motor.motor_asyncio

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print("~~~~~~~~~~~\n\n")
print(f"Current Working Directory:\n{cwd}\n")

initial_extensions = [
    'cogs.owner',
    'cogs.prefix',
    'cogs.interactions',
    'cogs.error',
    'cogs.ping',
    'cogs.help',
    'cogs.greetings',
    'cogs.events'
    ]

async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

    try:
        data = await bot.pf.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

def main():
    # allows privledged intents for monitoring members joining, roles editing, and role assignments
    intents = nextcord.Intents.all()
    DEFAULTPREFIX = ">"
    secret_file = jl.read_json("secrets")
    bot = commands.Bot(
        command_prefix=get_prefix,
        intents=intents,
        #activity=activity,
        case_insensitive=True,
        owner_id=741118153299591240
    )
    bot.connection_url = secret_file["mongo"]
    logging.basicConfig(level=logging.INFO)
    bot.DEFAULTPREFIX = DEFAULTPREFIX
    bot.cwd = cwd

    async def ch_pr():
        await bot.wait_until_ready()
        prefix = get_prefix

        member_count = 0
        member_string = ""
        for m in bot.guilds:
            member_string += f"{m.member_count} Members"
            member_count += m.member_count

        statuses = [f'on {len(bot.guilds)} servers', f'to {member_count} members', 'discord.gg/dm7gSAT68d']

        while not bot.is_closed():

            status = random.choice(statuses)

            await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=status))


            await asyncio.sleep(10)

    # boolean that will be set to true when views are added
    bot.persistent_views_added = False
    @bot.event
    async def on_ready():
        print('\nPrefixes:')
        for document in await bot.pf.get_all():
            print(document)
        print('\nWarnings:\n')
        for document in await bot.warns.get_all():
            print(document)
        print('\nInitialized Database\n')
        member_count = 0
        guild_string = ""
        for g in bot.guilds:
            guild_string += f"**{g.name}** - {g.id} - __**Members:**__ {g.member_count}\n"
            member_count += g.member_count
        print(
            f"Bot: '{bot.user.name}' has connected to Discord, active on **{len(bot.guilds)}** guilds:\n{guild_string}")
        print(f"__**nextcord API version:**__ {nextcord.__version__}")
        print(f"__**Python version:**__ {platform.python_version()}")
        print(
            f"__**Running on**__ {platform.system()} {platform.release()} ({os.name})\n")
        try:
            update_channel = await bot.fetch_channel(config.BOT_START_CHANNEL_ID)
            embed = nextcord.Embed(
                title="I am online!",
                description=f"I logged in at {nextcord.utils.format_dt(nextcord.utils.utcnow(), 'F')}\n\nI am connected to __**{len(bot.guilds)}**__ guilds:\n{guild_string}\n__**Nextcord API version:**__ {nextcord.__version__}\n__**Python version:**__ {platform.python_version()}\n__**Running on:**__ {platform.system()} {platform.release()} ({os.name})",
            )
            await update_channel.send(embed=embed)
        except:
            print(
                f"Can't Fetch The Update Channel!\nMake Sure That You Kept The Right ID, If You Did Try And Contact || W7CEP#0001"
            )
    @bot.event
    async def on_command_error(error, ctx):
        if isinstance(error, commands.NoPrivateMessage):
            await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.content.startswith == "$trade Kyurem-White":
            await message.channel.send("Fused pokemon cant be traded.\n\nExample:\nKyurem-White\nKyurem-Black\nNecrozma-Dusk-Mane\nNecrozma-Dawn-Wings\nCalyrex-Ice\nCalyrex-Shadow\n")

    @bot.event
    async def on_message(message):
        # Ignore messages sent by yourself
        if message.author.bot:
            return

        # Whenever the bot is tagged, respond with its prefix
        if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(
            f"<@!{bot.user.id}>"
        ):
            data = await bot.pf.find_by_id(message.guild.id)
            if not data or "prefix" not in data:
                prefix = bot.DEFAULTPREFIX
            else:
                prefix = data["prefix"]
            await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

        await bot.process_commands(message)

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db1 = bot.mongo["configs"]
    bot.db2 = bot.mongo["infractions"]
    bot.pf = Document(bot.db1, "Arceus_Prefixes")
    bot.warns = Document(bot.db2, "Arceus_Warns")
    bot.db3 = bot.mongo["blacklist"]
    bot.bl = Document(bot.db3, "Users")

        # load essential cogs

    for extension in initial_extensions:
        bot.load_extension(extension)

    async def startup():
        bot.session = aiohttp.ClientSession()

    bot.loop.create_task(startup())
    bot.loop.create_task(ch_pr())
    # run the bot
    bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
    main()
