import nextcord
from nextcord.ext import commands
import asyncio
import datetime
from datetime import datetime
from typing import List
from utils.utils import custom_id
import config

#----------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------------------------------

class App(commands.Cog, name="App"):
    """Application to become a moderator"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

#----------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.guild_only()
    async def applymod(self, ctx, member: nextcord.Member = None):

        """`Apply for Moderator (Testing)`"""

        member = ctx.author if not member else member
        def checkmsg(m):
            return m.author == member
        def checkreact(reaction, user):
            return user.id == member.id and str(reaction.emoji) in ['✅', '❌']
        try:
            doodoo = nextcord.Embed(title="Application will start soon...", description="Remember to be 100% Honest and provide good answers!\nThe Questions will be sent shortly...", color=nextcord.Color.dark_orange())
            await member.send(embed=doodoo)
            async with member.typing():
                await asyncio.sleep(5)
            await member.send("Discord Username?")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            first = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("How old are you? (If you feel uncomfortable saying this, just confirm if you're at least a teenager.)")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            second = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("What Time Zone do you live in? (So I know when you're online.)")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            third = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("Why do you want to be Moderator?")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            fourth = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("What will you do for the discord Server?")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            fifth = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("Anything else you want to say?")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            sixth = msg.content

        except asyncio.TimeoutError:
            await member.send("You took too long to write in a response :(")
        else:
            channel = self.bot.get_channel(918060994855575582)
            poo = await member.send("Are you sure you want to submit this application?")
            await poo.add_reaction('✅')
            await poo.add_reaction('❌')
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=checkreact)
            if str(reaction.emoji) == '✅':
                async with member.typing():
                    await asyncio.sleep(3)
                await member.send('Thank you for applying! Your application will be sent to the Owner soon')
                await asyncio.sleep(3)
                poopoo = nextcord.Embed(title='Application Answers', color=nextcord.Color.dark_orange())
                poopoo.add_field(name=f"1: What\'s your Discord Username?", value=f"{first}")
                poopoo.add_field(name="2: How old are you? (If you're not comfortable saying this at least confirm if you're a teenager", value=f"{second}")
                poopoo.add_field(name="3: What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active", value=f"{third}")
                poopoo.add_field(name="4:Why do you want to be Moderator?", value=f"{fourth}")
                poopoo.add_field(name="5: What will you do for the Discord Server?", value=f"{fifth}")
                poopoo.add_field(name="6: Anything else you want to say?", value=f"{sixth}")

                poopoo.set_author(name=f"Application taken by: {member}", icon_url=f"{member.avatar.url}")
                poopoo.set_footer(text=f"{member}")
                poopoo.timestamp = datetime.datetime.now()
                await channel.send(embed=poopoo)
            else:
                if str(reaction.emoji) == '❌':
                    await member.send('Application won\'t be sent')

#----------------------------------------------------------------------------------------------------------------------------------------------------------

def setup(bot: commands.Bot):
    bot.add_cog(App(bot))