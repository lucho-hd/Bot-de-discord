import discord
from discord.ext import commands
from database.tasks import get_user_progress

class TasksCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="tareas")
    async def tareas(self, ctx):
        """
            Muestra las tareas actuales del usuario para ganar tiradas extras.
        """
        user_id = str(ctx.author.id)
        user_progress = get_user_progress(user_id)

        if not user_progress:
            await ctx.send(f"{ctx.author.mention}, no se pudo obtener tu progreso. Por favor, intenta de nuevo.")
            return

        tasks_embed = discord.Embed(
            title="Tus tareas diarias para ganar tiradas extras.",
            color=0x00ff00
        )

        reactions_made = user_progress.get('reactions_made', 0)
        messages_sent = user_progress.get('messages_sent', 0)
        extra_rolls = user_progress.get('extra_rolls', 0)

        tasks_embed.add_field(
            name="Reaccionar a 5 mensajes",
            value=f"{reactions_made} / 5 reacciones",
            inline=False
        )

        tasks_embed.add_field(
            name="Enviar 10 mensajes",
            value=f"{messages_sent} / 10 mensajes",
            inline=False
        )

        tasks_embed.add_field(
            name="Tiradas extras",
            value=f"Tiradas extras disponibles: {extra_rolls}",
            inline=False
        )

        if user_progress['reactions_made'] >= 5 and user_progress['messages_sent'] >= 10:
            tasks_embed.add_field(
                name="🎉 ¡Tareas Completadas!",
                value="Has completado todas las tareas diarias y no puedes ganar más tiradas extras hoy.",
                inline=False
            )

        await ctx.send(embed=tasks_embed)

async def setup(bot):
    await bot.add_cog(TasksCog(bot))
