import config
import nextcord
from util.ticket_view import TicketView
from utils.utils import custom_id

VIEW_NAME = "TicketsView"


class TicketsView(TicketView):
	def __init__(self):
		super().__init__()

	@nextcord.ui.button(
		label="Open",
		style=nextcord.ButtonStyle.primary,
		custom_id="open",
	)
	async def open_button(self, button, interaction):
		await self.handle_click(button, interaction)


