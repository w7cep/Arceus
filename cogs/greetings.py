from random import choice

import config
import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import command
import json


class GreetingsCog(commands.Cog, name="Greetings"):
	"""Greeting commands"""
	
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self._last_member = None

	@commands.command(name="hello", aliases=["hi"])
	async def say_hello(self, ctx):
		"""Say hi to the bot and it will say hi back."""
		await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

	@commands.command(name="bye")
	async def say_bye(self, ctx):
		"""Say bye to the bot and it will say bye back."""
		await ctx.send(f"{choice(('Bye', 'Peace', 'See Ya', 'Later'))} {ctx.author.mention}!")

def setup(bot: commands.Bot):
	bot.add_cog(GreetingsCog(bot))
