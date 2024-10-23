import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

"""
    Cargué las variables de entorno desde un archivo (/.env) para facilitar su acceso en el proyecto
"""
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

# Inicializa el bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento para indicar que el bot está listo
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot conectado como {bot.user}. Comandos sincronizados.")


async def setup_hook():
    await bot.load_extension('commands.commands')
    await bot.load_extension('commands.collectibles')
    await bot.load_extension('tasks.message_tasks')
    await bot.load_extension('tasks.reaction_tasks')
    await bot.load_extension('commands.tasks')
    await bot.load_extension('tasks.neither_lops_or_it_caster_hours')
    
    
async def main():
    """
        Inicializa al bot
    """
    await setup_hook()
    await bot.start(TOKEN)

# Ejecuta la función asincrónica principal
asyncio.run(main())
