import random
import discord  
from discord.ext import commands, tasks
from datetime import datetime

class NeitherLopsOrItCasterHours(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
        self.neither_lops_hours_task.start()

    def cog_unload(self):
        self.neither_lops_hours_task.cancel()

    @tasks.loop(minutes=1)
    async def neither_lops_hours_task(self):
        """ Tarea que se ejecuta a cada minuto para verificar si son las hs y enviar la imagen """
        now = datetime.now()

        if now.hour == 18 and now.minute == 24:
            channel = self.bot.get_channel(1049398666877747312)

            images = [
                'https://imgur.com/I1DzYmO.jpg',
                'https://imgur.com/86O8NY4.jpg',
                'https://imgur.com/4iQKQKL.jpg',
                'https://imgur.com/cgcUyXG.jpg',
                'https://imgur.com/oeaC6BL.jpg',
                'https://imgur.com/yoAkMc1.jpg',
                'https://imgur.com/bkRpVYv.jpg',
                'https://imgur.com/b7e6fch.jpg',
                'https://imgur.com/mq5uCzm.jpg'
            ]

            random_image = random.choice(images)

            embed = discord.Embed(
                title="🎉 ¡Neither Lops or it Caster Hours ha comenzado!",
                description="¡Disfruta de este momento especial!",
                color=discord.Color.random()
            )
            embed.set_image(url=random_image)

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NeitherLopsOrItCasterHours(bot))
        