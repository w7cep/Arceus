import nextcord
from nextcord.ext import commands
import asyncio
import datetime
from datetime import datetime
#----------------------------------------------------------------------------------------------------------------------------------------------------------
class TestConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()
#----------------------------------------------------------------------------------------------------------------------------------------------------------
class Buttons(commands.Cog, name="Buttons"):
    """Channel Commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
#----------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(description="Confrim/Cancel template.")
    @commands.is_owner()
    async def test(self, ctx, channel: nextcord.TextChannel = None, setting = None):

            view = TestConfirm()

            em = nextcord.Embed(
                title="Are you sure?",
                description=f"Are you sure you want to use this command {ctx.author.mention}?",
                color=nextcord.Color.dark_red(),
                timestamp=datetime.now(),
            )

            await ctx.send(embed = em, view=view)

            await view.wait()

            if view.value is None:
                await ctx.author.send("Command has been Timed Out, please try again.")

            elif view.value:
                await ctx.send("You clicked Confirm")

            else:
                await ctx.send("You clicked Cancel")
            return
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def setup(bot: commands.Bot):
    bot.add_cog(Buttons(bot))