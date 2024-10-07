import discord
from discord.ext import commands
from models.card import Card
from database.collections import user_collections
from utils.generate_image import generate_card_image

class CollectibleCommands(commands.Cog):
    def __init__(self, bot) -> None:
        """
        Inicializa el Cog con el bot.

        Args:
            bot (commands.Bot): La instancia del bot de Discord.
        """
        self.bot = bot


    @commands.command(name="tirar")
    async def tirar(self, ctx):
        """
        Selecciona y envía una carta aleatoria al usuario.

        Args:
            ctx (commands.Context): El contexto del comando invocado por el usuario.
        """
        user_id = str(ctx.author.id)
        if user_id not in user_collections:
            user_collections[user_id] = []

        if len(user_collections[user_id]) >= 3:
            await ctx.send("Ya has tirado 3 veces en las últimas 6 horas.")
            return

        card = self.generate_random_card()
        user_collections[user_id].append(card)
        embed = discord.Embed(description = f"¡Has recibido una nueva carta!")
        embed.set_image(url = card.image_url)
        await ctx.send(embed = embed)


    @commands.command(name = "coleccion")
    async def collection(self, ctx):
        """
        Muestra la colección de cartas del usuario.

        Args:
            ctx (commands.Context): El contexto del comando invocado por el usuario.
        """
        user_id = str(ctx.author.id)

        # Verifica si el usuario tiene cartas en su colección
        if user_id not in user_collections or not user_collections[user_id]:
            await ctx.send("Aún no tienes ninguna carta en tu colección.")
            return
        
        # Crea un embed con la colección del usuario
        collection_embed = discord.Embed(title="Tu colección de cartas")

        for card in user_collections[user_id]:
            collection_embed.add_field(name=card.name, value=card.description)
        await ctx.send(embed=collection_embed)


    def generate_random_card(self):     
        """
        Genera una carta aleatoria con una imagen.

        Returns:
            Card: Una instancia de la clase Card con información sobre la carta generada.
        """
        prompt = ""
        image_url   = generate_card_image(prompt)

        # Si no se puede generar una imagen, usa una imagen de placeholder, lo cual va a pasar ya que todavía no tenemos una API | IA que genere las imágenes
        if  image_url is None:
            image_url = "https://via.placeholder.com/1024"

        description = "Una carta mística generada por IA." 
        return Card(name = "Carta Mística", image_url = image_url, description = description)


async def setup(bot):
    """
    Configura el Cog de comandos coleccionables.

    Args:
        bot (commands.Bot): La instancia del bot de Discord.

    Returns:
        None: Este método no retorna nada.
    """
    await bot.add_cog(CollectibleCommands(bot))






