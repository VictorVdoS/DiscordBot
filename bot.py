import discord
from discord.ext import commands
import json
import os
import random
from urllib import parse, request
import re
import asyncio
import time
import datetime

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True,
                      status=discord.Status.idle, description=' ', intents=intents)

# ---------COMMANDS---------------

# #info do canal


@client.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description=' ',
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name='Servidor criado no dia', value=ctx.guild.created_at.strftime(
        '%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
    embed.add_field(name='Dono do servidor', value=f'{ctx.guild.owner}')
    embed.add_field(name='Região do servidor', value=f'{ctx.guild.region}')
    embed.add_field(name='Servidor ID', value=f'{ctx.guild.id}')
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.set_footer(icon_url=f'{ctx.author.avatar_url}',
                     text=f'Solicitado por: {ctx.author.name}')
    await ctx.send(embed=embed)

# cog usar isso para criar arquivos tipo player de musica, rpg, waifu etc


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

# clear


@client.command()
@commands.has_permissions(manage_messages=True)  # verifica permissao
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

# kick


@client.command()
@commands.has_permissions(manage_messages=True)  # verifica permissao
async def kick(ctx, member: discord.Member, *, reason=None):
    print(f'{member} foi kickado.')
    await member.kick(reason=reason)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

# ban


@client.command()
@commands.has_permissions(manage_messages=True)  # verifica permissao
async def ban(ctx, member: discord.Member, *, reason=None):
    print(f'{member} foi banido.')
    await member.ban(reason=reason)
    await ctx.send(f'Banido {member.mention}')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

# unban


@client.command()
@commands.has_permissions(manage_messages=True)  # verifica permissao
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Desbanido {user.mention}')
            print(f'{member} foi desbanido.')
            return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

# comando de dado


@client.command()
async def rolldice(ctx):
    message = await ctx.send("Escolha um dado:\n**4**, **6**, **8**, **10**, **12**, **20**, **100** ")

    def check(m):
        return m.author == ctx.author

    try:
        message = await client.wait_for("message", check=check, timeout=30.0)
        m = message.content

        if m != "4" and m != "6" and m != "8" and m != "10" and m != "12" and m != "20" and m != "100":
            await ctx.send("Desculpe, escolha inválida.")
            return

        coming = await ctx.send("Aqui vai...")
        time.sleep(1)
        await coming.delete()
        await ctx.send(f"**{random.randint(1, int(m))}**")
    except asyncio.TimeoutError:
        await message.delete()
        await ctx.send("A solicitação foi cancelad por você demorar mais de **30** segundos.")

# comando de ajuda


@client.command()
async def ajuda(ctx):
    embed = discord.Embed(
        #  title = 'AJUDA',
        description='BOT em criação, aprecie todas as usabilidades dele, não se esqueça que o comando prefixo neste canal é o "="',
        colour=6666111  # cor em decimal
    )
    embed.set_author(name='AJUDA', icon_url='https://64.media.tumblr.com/1e98a29e32a889552ca8f50ccd525d7d/135a1fac54a6e0a4-67/s128x128u_c1/e906c205d04f61aeb64566ee3e213affc0226310.pnj')  # url do icone

    # url do thumbnail
    embed.set_thumbnail(
        url='https://static.wikia.nocookie.net/digimonat/images/d/d1/Gabumon_b.jpg/revision/latest?cb=20140419005946&path-prefix=pt')

#  embed.set_image(url='https://4.bp.blogspot.com/-9JXkNq-2Hkg/WLNhFZYz7qI/AAAAAAAAcfU/5w0avymCZN8kDjuIV0bFYpZxXR7_x7IagCLcB/s1600/Digimon%2B01%2B-%2B2%2B-%2BGabumon.jpg')#url do thumbnail

    embed.set_footer(text='Qualquer duvida pode me chamar no privado')

   # embed.add_field(name='Nome do Field1', value='Valor do Field1', inline=False)
   # embed.add_field(name='Nome do Field2', value='Valor do Field2', inline=True)
   # embed.add_field(name='Nome do Field3', value='Valor do Field3', inline=True)

    await ctx.send(embed=embed)


@client.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    # print(html_content.read().decode())
    search_results = re.findall(
        r"watch\?v=(\S{11})", html_content.read().decode())
    print(search_results)
    # I will put just the first result, you can loop the response to show more results
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

# ---------------EVENTS----------

# Bot on


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

# Member has joined


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

# Member has left


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

# --------------ERROS-------------------
# tratamento de erro


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


@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Você mudou o prefixo para: {prefix}')

client.run('TOKEN')
