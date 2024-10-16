from discord.ext import commands
from database.tasks import get_user_progress, save_user_progress

class MessageTask(commands.Cog):
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
    async def on_message(self, message):
        if message.author.bot:
            return
        
        user_id = str(message.author.id)
        user_progress = get_user_progress(user_id)

        user_progress['messages_sent'] += 1
        
        if user_progress['messages_sent'] == 10:
            await message.channel.send(f"{message.author.mention}, ¡has enviado 10 mensajes y ganas una tirada extra!")
            user_progress['messages_sent'] = 0 
            user_progress['extra_rolls'] += 1 

        await self.update_user_progress(user_id, user_progress)

async def setup(bot):
    await bot.add_cog(MessageTask(bot))
