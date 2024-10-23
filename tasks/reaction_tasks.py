import discord
from discord.ext import commands
from database.tasks import get_user_progress, save_user_progress

class ReactionTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_user_progress(self, user_id: str, user_progress: dict):
        """Actualiza y guarda el progreso del usuario en la base de datos."""
        save_user_progress(
            user_id, 
            user_progress['messages_sent'], 
            user_progress['reactions_made'], 
            user_progress['extra_rolls']
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        user_id = str(user.id)
        user_progress = get_user_progress(user_id)

        user_progress['reactions_made'] += 1
        
        # Verificar si ha reaccionado a 5 mensajes
        if user_progress['reactions_made'] == 5:
            await reaction.message.channel.send(f"{user.mention}, ¡has reaccionado a 5 mensajes y ganas una tirada extra!")
            user_progress['reactions_made'] = 0 
            user_progress['extra_rolls'] += 1 

        await self.update_user_progress(user_id, user_progress)

async def setup(bot):
    await bot.add_cog(ReactionTask(bot))
