import discord
from discord.ui import View, Button

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=180)

    # ...existing code...

    @discord.ui.button(label="⚙️ Settings", style=discord.ButtonStyle.secondary)
    async def settings_button(self, interaction: discord.Interaction, button: Button):
        from .settings import SettingsView
        embed = discord.Embed(
            title="⚙️ Bot Settings",
            description="Click the buttons below to view and modify settings:",
            color=discord.Color.blue()
        )
        
        settings_view = SettingsView(interaction.client.settings_data)
        await interaction.response.send_message(embed=embed, view=settings_view, ephemeral=True)

    # ...existing code...
