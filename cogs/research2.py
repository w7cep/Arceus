import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import BucketType, cooldown
import utils.json_loader as jl
from utils import checks
import inspect
import datetime
from collections import Counter
import asyncio
import os
import random
import traceback
from urllib.parse import quote_plus
from typing import List
import requests


class Research2(commands.Cog, name="Research2"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(5, 30, type=BucketType.user)
    async def suggest(self, ctx, *, description):
        """
        `Suggest anything you want`
        """
        if ctx.channel.id == 881408403006697502:
            try:
                embed = nextcord.Embed(title='Suggestion', description=f'Suggested by: {ctx.author.mention}', color=nextcord.Color.dark_purple())
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
                embed.add_field(name='Description:', value=description)
                embed.timestamp = datetime.datetime.utcnow()
                channel = ctx.guild.get_channel(881408403006697502)
                poo = await channel.send(embed=embed)
                await poo.add_reaction("✅")
                await poo.add_reaction("❌")
            except Exception as error:
                raise(error)
        else:
            await ctx.send("Go to <#881408403006697502> to use this command!")

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(description='❌ Please make sure to include your suggestion:\n```!suggest <suggestion>```', color=nextcord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
            await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Research2(bot))