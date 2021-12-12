from nextcord.ext import commands, tasks
import nextcord
import datetime
import nextcord.errors
from nextcord.ext.commands import MissingPermissions



class Block(commands.Cog, name="Block"):
    """Receives ping commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot



def setup(bot: commands.Bot):
    bot.add_cog(Block(bot))