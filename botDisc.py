import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import logging
from functions_mongodb import summoner_highest_damage

load_dotenv()
id_channel = int(os.getenv('ID_CHANNEL'))
id_bot = (os.getenv('ID_BOT'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
intents.presences = True 

# Configuração do bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Executa texto no cmd
@bot.command()
async def run(ctx, text:str):
    cmd = [f'{text}']
    process = await asyncio.create_subprocess_exec(*cmd)
    await process.communicate()

# Envia query Top Damage no chat
@bot.command()
async def topdamage(ctx):
    channel = bot.get_channel(id_channel)
    text = summoner_highest_damage()
    if text:
        await channel.send(text)

if __name__ == "__main__":
    logging.basicConfig(filename='log/botDisc.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    bot.run(id_bot)