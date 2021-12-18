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


#--------------------------------------------------------------------------------------------------------------------------------
class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

class Dropdown(nextcord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            nextcord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            nextcord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            nextcord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦')
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's 
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Define a simple View that gives us a confirmation menu
class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.grey)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PersistentView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Green', style=nextcord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('This is green.', ephemeral=True)

    @nextcord.ui.button(label='Red', style=nextcord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('This is red.', ephemeral=True)

    @nextcord.ui.button(label='Grey', style=nextcord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('This is grey.', ephemeral=True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''class TicketView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @nextcord.ui.button(label='Open', style=nextcord.ButtonStyle.green)
    async def Open(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Opening A New Ticket', ephemeral=True)
        self.value = True'''
#----------------------------------------------------------------'''------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Research(commands.Cog, name="Research"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When the bot is ready, load the role views"""
        # skip this function if views are already added
        if self.__bot.persistent_views_added:
            return
        self.__bot.add_view(PersistentView())
        self.__bot.add_view(TicketView())
        self.__bot.add_view(Counter())
        # set flag
        self.__bot.persistent_views_added = True
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------
    @commands.command()
    @commands.is_owner()
    async def colour(self, ctx):
        """Sends a message with our dropdown containing colours"""

        # Create the view containing our dropdown
        view = DropdownView()

        # Sending a message containing our view
        await ctx.send('Pick your favourite colour:', view=view)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.is_owner()
    async def ask(self, ctx):
        """Asks the user a question to confirm something."""
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await ctx.send('Do you want to continue?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Confirmed...')
        else:
            print('Cancelled...')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.is_owner()
    async def prepare(self, ctx):
        """Starts a persistent view."""
        # In order for a persistent view to be listened to, it needs to be sent to an actual message.
        # Call this method once just to store it somewhere.
        # In a more complicated program you might fetch the message_id from a database for use later.
        # However this is outside of the scope of this simple example.
        await ctx.send("What's your favourite colour?", view=PersistentView())
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------
    '''@commands.command()
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
            await ctx.channel.send(embed=embed)'''
#------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------
    '''@commands.command() #or bot
    async def ticket(self, ctx):
        view = TicketView()
        guild = ctx.guild
        category = nextcord.utils.get(guild.categories, name="TICKETS")
        em = nextcord.Embed(title="__**Open A Ticket**__", description="Click **Open** to open a new ticket.")
        await ctx.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.send("timeout")
        if view.value:
            guild = ctx.guild
            category = nextcord.utils.get(guild.categories, name="TICKETS")
            # Gets the category of that channel (used your version so I don't know if this works)
            ticket = await ctx.guild.create_text_channel(f"{ctx.author.name}#{ctx.author.discriminator}'s ticket", category=category)
            # Creates the text channel in the specified category
            await ticket.send(f"Here's your ticket #{ticket}")
        else:
            await ctx.send("I don't know how we got here! lmao")'''
#--------------------------------------------------------------------------------------------------------------------------------
def setup(bot: commands.Bot):
    bot.add_cog(Research(bot))
