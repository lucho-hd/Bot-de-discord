# Imports
import discord
from discord.ext import commands, tasks
import random
from database.firebase_config import db
from services.card import get_all_cards, save_card_to_user, get_user_collection
from utils.cards import get_quality_color
from database.tasks import get_user_progress, save_user_progress

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
    
        # Obtiene el progreso del usuario en las distintas tareas
        user_progress = get_user_progress(user_id)

        if user_progress['extra_rolls'] > 0:
            user_progress['extra_rolls'] -= 1
        else:
            user_data = get_user_collection(user_id)

            if not user_data:
                user_data = {'cards': []}

        # Obtiene todas las cartas desde Firebase
        cards = get_all_cards()

        if not cards:
            await ctx.send("No hay cartas disponibles.")
            return

        # Elige una carta aleatoria de la lista de cartas
        card = random.choice(cards)

        # Añade la carta a la colección del usuario
        save_card_to_user(user_id, card)

        # Envía la carta al usuario
        embed = discord.Embed(description=f"¡Has recibido una nueva carta: **{card['name']}**!\n\n"
                                        f"**Calidad:** {card['quality']}\n\n"
                                        f"{card['description'].replace('.', '\n')}")
        embed.set_image(url=card['image_url'])
        await ctx.send(embed=embed)

        save_user_progress(user_id, user_progress['messages_sent'], user_progress['reactions_made'], user_progress['extra_rolls'])

    @tirar.error
    async def tirar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_time = round(error.retry_after / 60, 2)
            await ctx.send(f"Ya has tirado 3 veces. Debes esperar { cooldown_time } minutos antes de volver a tirar.") 


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






