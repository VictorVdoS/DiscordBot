#1 passo: definir o bot
#2 passo: criar o dado, 8ball, e alguns comandos de jogos 
#3 passo: reprodutor de video
#4 passo: comandos adm, clear, kick, ban
#5 passo: comando help custom
#6 passo: tratamento de erro
#7 passo: mudar o layout, dar nome, cores etc
#8 passo: verificar ortografia
#9 passo: deixar online

import os #token
import discord
from discord.ext import commands
import json #prefixos
import random #dado
import asyncio #resposta
import time #dado
from keep_alive import keep_alive


intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)


def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]
  
client = commands.Bot(command_prefix = get_prefix, case_insensitive = True, status=discord.Status.idle, description=' ',intents=intents)

# #comando para remover o help padrao
# #esse comando removerá o help padrao, e importara a cog help personalizada, posso criar um help aqui
# client.remove_command('help')
# initial_extensions = [
#         'cogs.help',
#             ]  

#---------COG---------------

#cog usar isso para criar arquivos tipo player de musica, rpg, waifu etc
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

#---------FIM DO COG---------------

#comando de dado
@client.command()
async def rolldice(ctx):
    message = await ctx.send("Escolha um dado:\n**4**, **6**, **8**, **10**, **12**, **20**, **100** ")
    
    def check(m):
        return m.author == ctx.author

    try:
        message = await client.wait_for("message", check = check, timeout = 10.0)
        m = message.content

        if m != "4" and m != "6" and m != "8" and m != "10" and m != "12" and m != "20" and m != "100":
            await ctx.send("Desculpe, escolha inválida.")
            return
        
        coming = await ctx.send("Aqui vai...")
        time.sleep(1)
        await coming.delete()
        await ctx.send(f" Você tirou **{random.randint(1, int(m))}** no dado")
    except asyncio.TimeoutError:
        await message.delete()
        await ctx.send("A solicitação foi cancelada por você demorar mais de **10** segundos.")
#fim do comando de dado 
#---------------EVENTS----------

#Bot on
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Youjo Senki'))
#   # Setting `Playing ` status
# await bot.change_presence(activity=discord.Game(name="a game"))
# # Setting `Streaming ` status
# await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
# # Setting `Listening ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
# # Setting `Watching ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
  print('Entramos como {0.user}'. format(client))

#Member has joined
@client.event
async def on_member_join(member):
  print(f'{member} entrou no servidor ^.^')
  
#Member has left
@client.event
async def on_member_remove(member):
  print(f'{member} saiu do servidor T_T')

#--------------ERROS-------------------
#tratamento de erro
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('COMANDO INVÁLIDO')
  # if isinstance(error, commands.MissingRequiredArgument):
  #   await ctx.send('Digite a sentença toda')

@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = '.' 

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

#colocar permissão
@client.command()
async def changeprefix(ctx, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(ctx.guild.id)] = prefix

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)  
  
  await ctx.send(f'Você mudou o prefixo para: {prefix}')
  
keep_alive()
client.run(os.getenv('TOKEN')) #ou colocar o token direto