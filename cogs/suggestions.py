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

class Counter(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(
        label="0", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        number = int(button.label) if button.label else 0
        if number + 1 >= 50:
            button.style = nextcord.ButtonStyle.red
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

    @nextcord.ui.button(label="0", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        number = int(button.label) if button.label else 0
        if number + 1 >= 50:
            button.style = nextcord.ButtonStyle.red
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

class Suggestions(commands.Cog, name="Suggestions"):
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
        if ctx.channel.id == 919640480025817129:
            try:
                embed = nextcord.Embed(title='Suggestion', description=f'Suggested by: {ctx.author.mention}', color=nextcord.Color.dark_purple())
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
                embed.add_field(name='Description:', value=description)
                embed.timestamp = datetime.datetime.utcnow()
                channel = ctx.guild.get_channel(881408403006697502)
                poo = await channel.send(embed=embed, view=Counter())
                await ctx.message.delete()

            except Exception as error:
                raise(error)
        else:
            await ctx.send("Go to <#919640480025817129> to use this command!")

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            amount=3
            embed = nextcord.Embed(description='❌ Please make sure to include your suggestion:\n```.suggest <suggestion>```', color=nextcord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
            await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Suggestions(bot))