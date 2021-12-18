import nextcord
from typing import List

class TicketView(nextcord.ui.View):
    def __init__(self):

        super().__init__(timeout=None)

    async def handle_click(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        guild = ctx.guild
        category = nextcord.utils.get(guild.categories, name="TICKETS")
        # Gets the category of that channel (used your version so I don't know if this works)
        ticket = await ctx.guild.create_text_channel(f"{ctx.author.name}#{ctx.author.discriminator}'s ticket", category=category)
        # Creates the text channel in the specified category
        await ticket.send(f"Here's your ticket #{ticket}")
        await ctx.send(embed=created_em)
