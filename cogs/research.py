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
class Google(nextcord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        # we need to quote the query string to make a valid url. nextcord will raise an error if it isn't valid.
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(nextcord.ui.Button(label='Click Here', url=url))
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
class EphemeralCounter(nextcord.ui.View):
    # When this button is pressed, it will respond with a Counter view that will
    # give the button presser their own personal button they can press 5 times.
    @nextcord.ui.button(label='Click', style=nextcord.ButtonStyle.blurple)
    async def receive(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # ephemeral=True makes the message hidden from everyone except the button presser
        await interaction.response.send_message('Enjoy!', view=Counter(), ephemeral=True)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None
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
        self.__bot.add_view(ConfirmView())
        self.__bot.add_view(SysBotRuleView())
        self.__bot.add_view(ColorRoleView())

        # set flag
        self.__bot.persistent_views_added = True
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name='google', description="button test function",)
    @cooldown(1, 15, BucketType.guild)
    #if you want to restrict command to a role
    #@commands.has_role("nextcordAdmin")
    @commands.has_permissions(send_messages=True)
    async def google(self, ctx, *, query: str):

        await ctx.send(f"Google Result for: `{query}`", view=Google(query))
#----------------------------------------------------------------------------------------------
    @commands.command()
    async def colour(self, ctx):
        """Sends a message with our dropdown containing colours"""

        # Create the view containing our dropdown
        view = DropdownView()

        # Sending a message containing our view
        await ctx.send('Pick your favourite colour:', view=view)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    async def counter(self, ctx):
        """Starts a counter for pressing."""
        await ctx.send('Press!', view=EphemeralCounter())
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
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
    @commands.command()
    async def tic(self, ctx):
        """Starts a tic-tac-toe game with yourself."""
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command()
    async def dicksize(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        sizes = ['8D',
                    '8=D',
                    '8==D',
                    '8===D',
                    '8====D',  
                    '8=====D',
                    '8======D', 
                    '8=======D',
                    '8========D',
                    '8=========D',
                    '8==========D',
                    '8===========D',
                    '8============D',
                    '8=============D',
                    '8==============D',
                    '8===============D',
                    '8================D']
        await ctx.send(f"{member.mention} has this dick size: {random.choice(sizes)}")

    @dicksize.error
    async def dicksize_error(ctx, error):
                if isinstance(error, commands.MissingRequiredArgument):
                    userembed=nextcord.Embed(title="__**Command help!**__", color=0xffffff)
                    userembed.add_field(name="Command --> ``dicksize <user>``", value="Info --> `says how big of a dick a member has.`", inline=False)
                    await ctx.send(embed=userembed)
                    await ctx.send("You need to specify a member!")
#--------------------------------------------------------------------------------------------------------------------------------

    @commands.command(pass_context=True)
    async def hack(self, ctx, member:nextcord.Member = None):
        if not member:
            await ctx.send("Please specify a member")
            return

        passwords=['imnothackedlmao','sendnoodles63','ilovenoodles','icantcode','christianmicraft','server','icantspell','hackedlmao','WOWTONIGHT','69'] 
        fakeips=['154.2345.24.743','255.255. 255.0','356.653.56','101.12.8.6053','255.255. 255.0']

        embed=nextcord.Embed(title=f"**Hacking: {member}** 0%", color=0x2f3136)
        m = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 19%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 34%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 55%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 67%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 84%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 99%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(1)
        embed=nextcord.Embed(title=f"**Hacking: {member}** 100%", color=0x2f3136)
        await m.edit(embed=embed)
        await asyncio.sleep(3)
        embed=nextcord.Embed(title=f"{member} info ", description=f"*Email `{member}@hacked.com` Password `{random.choice(passwords)}`  IP `{random.choice(fakeips)}`*", color=0x2f3136)
        embed.set_footer(text="this is a joke plses dont worry.")
        await m.edit(embed=embed)
        await asyncio.sleep(1)
#--------------------------------------------------------------------------------------------------------------------------------
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
            await member.send("What's your Minecraft IGN + nextcord Username?")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            first = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("How old are you? (If you feel uncomfortable saying this, just confirm if you're at least a teenager)")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            second = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active)")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            third = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("Why do you want to be Moderator? Isn't it fun to play without any responsibilites?")
            msg = await self.bot.wait_for('message', check=checkmsg, timeout=250.0)
            fourth = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("What will you do for the nextcord Server?")
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
                poopoo.add_field(name=f"1: What\'s your Minecraft IGN + Discord Username?", value=f"{first}")
                poopoo.add_field(name="2: How old are you? (If you're not comfortable saying this at least confirm if you're a teenager", value=f"{second}")
                poopoo.add_field(name="3: What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active", value=f"{third}")
                poopoo.add_field(name="4:Why do you want to be Moderator? Isn\'t it fun to play without any responsibilites?", value=f"{fourth}")
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
    @commands.command()
    async def members(self, ctx):
        await ctx.send("`Membercount : {0.member_count}`".format(ctx.message.guild))
#--------------------------------------------------------------------------------------------------------------------------------
def setup(bot: commands.Bot):
    bot.add_cog(Research(bot))
