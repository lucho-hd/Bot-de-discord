import discord
from discord import app_commands
from discord.ext import commands

class MediaCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_image(self, interaction: discord.Interaction, image_url : str, description: str = ""):
        """
        Envía un mensaje con una imagen incrustada en un embed.

        Args:
            interaction (discord.Interaction): La interacción del usuario.
            image_url (str): URL de la imagen a mostrar.
            description (str, optional): Descripción de la imagen. Defaults to "".
            title (str, optional): Título del embed. Defaults to "".
        """
        embed = discord.Embed(description=description)
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)

    """
        ----------------------------------------- Comandos de barra -------------------------------------------------------------------------
    """ 

    @app_commands.command(name="nacho-kaczka", description="Muestra la imagen de Nacho Kaczka.")
    async def nacho_kaczka(self, interaction: discord.Interaction):
        image_url = "https://imgur.com/Ktfrmu4.jpg"
        await self.send_image(interaction, image_url, "Aquí está la imagen de Nacho Kaczka")
        

    @app_commands.command(name="lusis-baby", description="Muestra la imagen de Lusis Baby")
    async def lusis_baby(self, interaction: discord.Interaction):
        image_url = "https://imgur.com/apS2hYE.jpg"
        await self.send_image(interaction, image_url, "Aquí está la imagen de Lusis Baby")


    @app_commands.command(name="williams-dafoe", description="Muestra la imagen de Williams Dafoe")
    async def william_dafoe(self, interaction: discord.Interaction):
        image_url = "https://imgur.com/QLODOyA.jpg"
        await self.send_image(interaction, image_url, "Aquí está la imagen de Williams Dafoe")


    @app_commands.command(name="nachoneitor", description="Muestra la imagen de Nachoneitor")
    async def nachoneitor(self, interaction: discord.Interaction):
        image_url = "https://imgur.com/iFB0bAy.jpg"
        await self.send_image(interaction, image_url, "Aquí está la imagen de Nachoneitor")

# Esta es la función que el bot buscará para cargar la extensión
async def setup(bot):
    await bot.add_cog(MediaCommands(bot))

# URL para invitar al bot
    # https://discord.com/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot
