# Imports
import discord
from discord.ext import commands
import random
from database.cards import cards 
from database.collections import user_collections

class CollectibleCommands(commands.Cog):
    def __init__(self, bot) -> None:
        """
        Inicializa el Cog con el bot.

        Args:
            bot (commands.Bot): La instancia del bot de Discord.
        """
        self.bot = bot

    @commands.command(name="tirar")
    @commands.cooldown(3, 3600, commands.BucketType.user)
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
            await ctx.send("Ya has tirado 3 veces en la última hora.")
            return

        card = random.choice(cards)
        user_collections[user_id].append(card)

        embed = discord.Embed(description=f"¡Has recibido una nueva carta:\nRareza: {card['quality']}\n\n {card['name']}!\n\n{card['description'].replace('.', '\n')}")
        embed.set_image(url=card['image_url'])
        await ctx.send(embed=embed)

    # !TODO: Solucionar el xq no se guarda la carta de cada usuario en collections.py 
    @commands.command(name="coleccion")
    async def collection(self, ctx):
        """
        Muestra las cartas que el usuario tiene en su colección.

        Args:
            ctx (commands.Context): El contexto del comando invocado por el usuario.
        """
        user_id = str(ctx.author.id)
        if user_id not in user_collections or not user_collections[user_id]:
            await ctx.send("Aún no tienes ninguna carta en tu colección.")
            return

        collection_embed = discord.Embed(title="Tu colección de cartas")

        for card in user_collections[user_id]:
            collection_embed.add_field(name=card['name'], value=card['description '], inline=False)
        
        await ctx.send(embed=collection_embed)

async def setup(bot) -> None:
    """
    Configura el Cog de comandos coleccionables.

    Args:
        bot (commands.Bot): La instancia del bot de Discord.

    Returns:
        None: Este método no retorna nada.
    """
    await bot.add_cog(CollectibleCommands(bot))






