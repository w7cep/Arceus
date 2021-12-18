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
        if number + 1 >= 1000000:
            button.style = nextcord.ButtonStyle.red
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=nextcord.ButtonStyle.primary, label='\u200b', row=y)
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
class Fun(commands.Cog, name="Fun"):
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    @commands.is_owner()
    async def counter(self, ctx):
        """Starts a counter for pressing."""
        await ctx.send('Press the Green Button to count to 1,000,000!', view=Counter())
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command()
    async def tic(self, ctx):
        """Starts a tic-tac-toe game with yourself."""
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name='google', description="button test function",)
    @cooldown(1, 15, BucketType.guild)
    #if you want to restrict command to a role
    #@commands.has_role("nextcordAdmin")
    @commands.has_permissions(send_messages=True)
    async def google(self, ctx, *, query: str):

        await ctx.send(f"Google Result for: `{query}`", view=Google(query))

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
    bot.add_cog(Fun(bot))
