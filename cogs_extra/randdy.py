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

class Yea(nextcord.ui.Button):
    async def callback(self, interaction):
        # check if the interaction.user is the ctx.author
        print("ctx.author.id: ",self.view.ctx.author.id)
        print("interaction.user.id: ",interaction.user.id)
        if interaction.user.id == self.view.ctx.author.id:

            #Prints the button label for the button clicked
            print(self.label, self.style, interaction.user)

            #responds with an ephemeral message showing button clicked
            await interaction.response.send_message(self.label, ephemeral=True)

            #Sets the view.value to the label of the button clicked
            self.view.value = self.label

            #Ends the interation to stop other buttons being clicked
            self.view.stop()




# Define a simple View that gives us a confirmation menu
class btn_create(nextcord.ui.View):
    def __init__(self, ctx, data):
        super().__init__()
        self.value = None
        self.ctx = ctx

    #######################################
    #Create dynamic buttons based on data passed

        for x in data:
            #creates an instance and sets the label

            btn = Yea(label = x['label'])


            #Sets the label colour to grey if colour given not in
            #the list of available colours

            if x['colour'].lower()=='green':
                btn.style = nextcord.ButtonStyle.green
            elif x['colour'].lower()=='red':
                btn.style = nextcord.ButtonStyle.red
            elif x['colour'].lower()=='blurple':
                btn.style = nextcord.ButtonStyle.blurple
            else:
                btn.style = nextcord.ButtonStyle.grey

            #add the button to the view
            self.add_item(btn)

async def ask(self, ctx, msg_title, msg_desc, btn_data, img = None, thumb = None):
    """displays an embed with dynamically generated buttons beneath"""
    # We create the view and assign it to a variable so we can wait for it later.
    view = btn_create(ctx, btn_data)

    # Create an embed for the buttons
    embed = nextcord.Embed(
        title=msg_title,
        description=msg_desc,
        colour = self.bot.colors["BRANN"],
    )
    # Set an img if provided
    if img:
        embed.set_image(url=img)
    # Set a thumbnail if provided
    if thumb:
        embed.set_thumbnail(url=thumb)


    # Sending a embed containing our view
    msg = await ctx.send(embed=embed, view=view)

    # Wait for the View to stop listening for input...
    await view.wait()

    #

    if view.value is None:
        print('Timed out...')
        await msg.delete
        return

    else:
        return(view.value)

class Research(commands.Cog, name="Research"):
    """Test commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


# Define a class and callback method to handle button clicks
#=========================================#
# This is the command that sends the button list and recieves the answer (button clicked) by user

    @commands.command(
        name='pong',
        description="button test function",

    )
    #if you want to restrict command to a role
    #@commands.has_role("DiscordAdmin")
    @commands.has_permissions(send_messages=True)
    async def pong(self, ctx):
        #create embed title and description
        msg_title = 'Button Test Embed'
        msg_desc = 'Choose a button'
        #create button list - actually a list of dictionaries
        btn_data = [
            {'label':'Button A', 'colour': 'red'},
            {'label':'Button B', 'colour': 'green'},
            {'label':'Button C', 'colour': 'blurple'},
            {'label':'Button D', 'colour': 'grey'},


        ]
        #Launch the ask function
        btn_pressed= await ask(self, ctx, msg_title, msg_desc, btn_data, None, self.bot.user.avatar.url)
        await ctx.send(f"The button pressed: {btn_pressed}")

def setup(bot: commands.Bot):
    bot.add_cog(Research(bot))
