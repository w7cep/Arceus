import config
import nextcord
import datetime
from nextcord.ext import commands
from better_profanity import profanity


class Profanity(commands.Cog, name="Profanity"):
    """Server Suggestion Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__bot = bot

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def profanity(self, ctx):
        """Add or Delete banned words."""
        await ctx.send("Invalid sub-command specified")

    @profanity.command(name="add")
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, *words):
        '''Add cuss word to file.'''
        with open("./data/profanity.txt", "a", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in words]))

        profanity.load_censor_words_from_file("./data/profanity.txt")
        await ctx.channel.trigger_typing()
        await ctx.send("Action complete.")

    @profanity.command(name="del")
    @commands.has_permissions(manage_messages=True)
    async def remove_profanity(self, ctx, *words):
        '''Delete cuss word from file.'''
        with open("./data/profanity.txt", "r", encoding="utf-8") as f:
            stored = [w.strip() for w in f.readlines()]

        with open("./data/profanity.txt", "w", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in stored if w not in words]))

        profanity.load_censor_words_from_file("./data/profanity.txt")
        await ctx.channel.trigger_typing()
        await ctx.send("Action complete.")

def setup(bot: commands.Bot):
    bot.add_cog(Profanity(bot))
