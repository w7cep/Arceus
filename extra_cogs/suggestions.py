import nextcord
from nextcord.ext import commands
import utils.json_loader as jl
from utils import checks
import inspect
import datetime
from collections import Counter
import asyncio
import os
import random
import traceback

class Covertcorm(commands.Converter):
    async def convert(self, ctx, argument: str):
        # In this example we have made a custom converter.
        # This checks if an input is convertible to a
        # `nextcord.Member` or `nextcord.TextChannel` instance from the
        # input the user has given us using the pre-existing converters
        # that the library provides.

        member_converter = commands.MemberConverter()
        try:
            # Try and convert to a Member instance.
            # If this fails, then an exception is raised.
            # Otherwise, we just return the converted member value.
            member = await member_converter.convert(ctx, argument)
        except commands.MemberNotFound:
            pass
        else:
            return member

        # Do the same for TextChannel...
        textchannel_converter = commands.TextChannelConverter()
        try:
            channel = await textchannel_converter.convert(ctx, argument)
        except commands.ChannelNotFound:
            pass
        else:
            return channel

        # If the value could not be converted we can raise an error
        # so our error handlers can deal with it in one place.
        # The error has to be CommandError derived, so BadArgument works fine here.
        raise commands.BadArgument(f'No Member or TextChannel could be converted from "{argument}"')

class Suggestions(commands.Cog, name="Suggestions"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="blacklist", description="Blacklist a user from the bot", usage="<user>"
    )
    @commands.has_role('Bot Manager')
    async def suggestchannel(self, ctx, channel: nextcord.TextChannel):


        self.bot.blacklisted_users.append(channel.id)
        data = jl.read_json("data")
        data["suggestion_ch_id"].append(channel.id)
        jl.write_json(data, "data")
        await ctx.send(f"Hey, I have added {channel.name} to the list.")

    @commands.command(
        name="delete_suggestion_channel", aliases=["dsc"], description="Delete your guilds suggestion channel!"
    )
    @commands.guild_only()
    @commands.has_role('Bot Manager')
    async def deletesuggestionchannel(self, ctx):
        await self.bot.pf.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds suggestion channel has been deleted.")

def setup(bot: commands.Bot):
    bot.add_cog(Suggestions(bot))
