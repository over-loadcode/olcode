import discord
from discord.ext import commands
import os

token = ''
intents = discord.Intents().all()

client = commands.Bot(command_prefix='\'', intents=intents)
client.remove_command('help')

@client.command()
async def ping(ctx):
    await ctx.send('https://tenor.com/view/no-sad-frustrated-no-way-yell-gif-17334973')

@client.command()
async def mappers(ctx):
    import os
    list_message = ''
    mappers = os.listdir('mappers')
    mappers.sort()
    for mapper in mappers:
        list_message += f'{mapper}, '
    list_message = list_message[:-2]
    await ctx.send(f'Mappers available: {list_message}.\nSome alternate names for mappers are accepted.')

@client.event
async def on_ready():
    print('Ready.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)