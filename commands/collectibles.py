# Imports
import discord
from discord.ext import commands
import random
from database.firebase_config import db
from services.card import save_card_to_user, get_user_collection

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
        Selecciona y envía una carta aleatoria al usuario desde Firestore.

        Args:
            ctx (commands.Context): El contexto del comando invocado por el usuario.
        """
        user_id = str(ctx.author.id)

        user_cards = get_user_collection(user_id)

        if len(user_cards) >= 3:
            await ctx.send("Ya has tirado 3 veces en la última hora.")
            return

        cards_ref = db.collection('cards').stream()
        cards = [card.to_dict() for card in cards_ref]

        if not cards:
            await ctx.send("No hay cartas disponibles.")
            return
            
        card = random.choice(cards)
        
        save_card_to_user(user_id, card)

        embed = discord.Embed(description=f"¡Has recibido una nueva carta: **{card['name']}**!\n\n"
                                        f"**Calidad:** {card['quality']}\n\n"
                                        f"{card['description'].replace('.', '\n')}")
        embed.set_image(url=card['image_url'])
        await ctx.send(embed=embed)

    @commands.command(name="coleccion")
    async def collection(self, ctx):
        """
        Muestra las cartas que el usuario tiene en su colección.

        Args:
            ctx (commands.Context): El contexto del comando invocado por el usuario.
        """
        user_id = str(ctx.author.id)

        user_cards = get_user_collection(user_id)

        if not user_cards:
            await ctx.send("Aún no tienes ninguna carta en tu colección.")
            return

        def get_quality_color(quality):
            """Devuelve un color basado en la calidad de la carta"""  
            colors = {
                "Común": 0x808080,
                "Rara": 0x0000FF,
                "Épica": 0x800080,
                "Legendaria": 0xFFD700
            }
            return colors.get(quality, 0xFFFFFF)

        for card in user_cards:
            embed_color = get_quality_color(card['quality'])

            card_embed = discord.Embed(
                title=card['name'],
                description=f"**Calidad**: {card['quality']}\n\n {card['description']}",
                color=embed_color
            )
            card_embed.set_thumbnail(url=card['image_url'])

            await ctx.send(embed=card_embed)

async def setup(bot) -> None:
    """
    Configura el Cog de comandos coleccionables.

    Args:
        bot (commands.Bot): La instancia del bot de Discord.

    Returns:
        None: Este método no retorna nada.
    """
    await bot.add_cog(CollectibleCommands(bot))






