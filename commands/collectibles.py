# Imports
import discord
from discord.ext import commands
import random
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
        """
        user_id = str(ctx.author.id)

        await self.procesar_tirada(ctx, user_id)

    async def procesar_tirada(self, ctx, user_id):
        """Procesa la tirada para el usuario."""
        cards = get_all_cards()

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

        user_progress = get_user_progress(user_id)
        save_user_progress(user_id, user_progress['messages_sent'], user_progress['reactions_made'], user_progress['extra_rolls'])

    @tirar.error
    async def tirar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            user_id = str(ctx.author.id)

            user_progress = get_user_progress(user_id)

            if user_progress['extraa_rolls'] > 0:
                user_progress['extra_rolls'] -= 1
                save_user_progress(user_id, user_progress['messages_sent'], user_progress['reactions_made'], user_progress['extra_rolls'] )

                await ctx.send(f"¡{ctx.author.mention} ha usado una tirada extra!")

                await self.procesar_tirada(ctx, user_id)
            else:
                cooldown_time = round(error.retry_after / 60)
                await ctx.send(f"Ya has tirado 3 veces. Debes esperar { cooldown_time } minutos antes de volver a tirar o puedes completar las misiones diarias para ganar una tirada extra.")


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






