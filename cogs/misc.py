import platform
import random
from typing import Optional

import config
import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument


class Misc(commands.Cog, name="Misc"):
	"""Misc. Commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def random(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@random.command()
	async def roll(self, ctx: commands.Context, dice: str):
		"""Rolls a given amount of dice in the form _d_
		
		Example: ?roll 2d20
		"""
		try:
			rolls = ""
			total = 0
			amount, die = dice.split("d")
			for _ in range(int(amount)):
				roll = random.randint(1, int(die))
				total += roll
				rolls += f"{roll} "
			await ctx.channel.trigger_typing()
			await ctx.send(f"Rolls: {rolls}\nSum: {total}")
		except ValueError:
			await ctx.channel.trigger_typing()
			await ctx.send("Dice must be in the format \_d\_ (example: 2d6)")

	@random.command()
	async def choose(self, ctx: commands.Context, *args):
		"""Chooses a random item from a list
		
		Example: ?choose "First Option" "Second Option" "Third Option"
		"""
		try:
			choice = random.choice(args)
			await ctx.channel.trigger_typing()
			await ctx.send(choice)
		except IndexError:
			await ctx.channel.trigger_typing()
			await ctx.send("You must specify at least one argument.")
			
	@random.command(name="joke")
	async def joke(self, ctx):
		"""Random dad joke."""
		selectjoke = random.choice([
			"Why don’t crabs give to charity? Because they’re shellfish.",
			"Why did the man name his dogs Rolex and Timex? Because they were watch dogs.",
			"My kid wants to invent a pencil with an eraser on each end, but I just don’t see the point."
		])
		await ctx.channel.trigger_typing()
		await ctx.send(selectjoke)

	@random.command(name="coinflip")
	async def coinflip(self, ctx):
		"""Flip a coin."""
		await ctx.channel.trigger_typing()
		await ctx.send("Heads" if random.randint(1, 2) == 1 else "Tails")

	@random.command(name="mirror")
	async def mirror(self, ctx, message):
		"""Bot will mirror your message."""
		await ctx.channel.trigger_typing()
		await ctx.send(message)

	@random.command(name="length")
	async def length(self, ctx, sent):
		"""Gives you the details of a sentence."""
		sentence: str = ctx.message.content[7:]
		print(sentence)
		length: int = len(sentence)
		i = 0
		count: int = 0
		while i < length - 1:
			i += 1
			if sentence[i] == " ":
				count += 1
		word = count + 1
		letter = i + 1
		await ctx.channel.trigger_typing()
		await ctx.send(f"World count : {word}, letter count : {letter}")

	@random.command(name="fact")
	async def animal_fact(self, ctx, animal: str):
		"""Gives you a fact for these animals: "dog", "cat", "panda", "fox", "bird", "koala"."""
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala", ):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.channel.trigger_typing()
					await ctx.send(embed=embed)
					await ctx.message.delete()

				else:
					await ctx.channel.trigger_typing()
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.channel.trigger_typing()
			await ctx.send("No facts are available for that animal.")   
	 
	@random.command(
		 name="slap", 
		aliases=["hit"])
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
		"""Slap another member for a reason or no reason."""
		await ctx.channel.trigger_typing()
		await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
		await ctx.message.delete()

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.channel.trigger_typing()
			await ctx.send("I can't find that member.")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def reaction(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@reaction.command(name="tableflip")
	async def tableflip(self, ctx):
		# I hope this unicode doesn't break
		"""(╯°□°）╯︵ ┻━┻"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/tableflip.gif"))

	@reaction.command(name="unflip")
	async def unflip(self, ctx):
		# I hope this unicode doesn't break
		"""┬─┬﻿ ノ( ゜-゜ノ)"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/unflip.gif"))

	@reaction.command(name="triggered")
	async def triggered(self, ctx):
		"""*TRIGGERED*"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/triggered.gif"))

	@reaction.command(name="delet")
	async def delet(self, ctx):
		"""Delet this"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/delet_this.png"))

	@reaction.command(name="weirdshit")
	async def weirdshit(self, ctx):
		"""WHY ARE YOU POSTING WEIRD SHIT?!?!?!"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/weirdshit.jpg"))

	@reaction.command(name="filth")
	async def filth(self, ctx):
		"""THIS IS ABSOLUTELY FILTHY!"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/filth.gif"))

	@reaction.command(name="heckoff")
	async def heckoff(self, ctx):
		"""heck off fools"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/heckoff.png"))

	@reaction.command(name="repost")
	async def repost(self, ctx):
		"""It's just a repost smh"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/repost.gif"))

	@reaction.command(name="boi")
	async def boi(self, ctx):
		"""BOI"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/boi.jpg"))



def setup(bot: commands.Bot):
	bot.add_cog(Misc(bot))
