import discord
from discord.ext import commands
import os
import random
from urllib import parse, request
import re
import datetime


intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)

client = commands.Bot(command_prefix='<', case_insensitive=True,
                      status=discord.Status.idle, description=' ', intents=intents)

# ---------COMMANDS---------------

# info do canalllll


@client.command()
async def info(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', description=' ',
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name='Server created at', value=ctx.guild.created_at.strftime(
        '%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
    embed.add_field(name='Server Owner', value=f'{ctx.guild.owner}')
    embed.add_field(name='Server Region', value=f'{ctx.guild.region}')
    embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.set_footer(icon_url=f'{ctx.author.avatar_url}',
                     text=f'Requested by {ctx.author.name}')
    await ctx.send(embed=embed)

# cog


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# ping


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# 8ball


# aliases eu posso colocar mais de um trigger para uma funcao
@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

# clear


@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

# kick


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    print(f'{member} foi kickado.')
    await member.kick(reason=reason)

# ban


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    print(f'{member} foi banido.')
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# unban


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            print(f'{member} foi desbanido.')
            return

# comando de olá


@client.command()
async def ola(ctx):
    await ctx.send(f'Olá, {ctx.author} tudo bem? Meu prefixo nesse canal é <')

# comando de dado


@client.command()
async def d(ctx, numero):
    D = random.randint(1, int(numero))
    await ctx.send(f'O número que saiu do dado é {D}')

# comando de ajuda


@client.command()
async def ajuda(ctx):
    embed = discord.Embed(
        #  title = 'AJUDA',
        description='BOT em criação, aprecie todas as usabilidades dele, não se esqueça que o comando prefixo neste canal é o "<"',
        colour=6666111  # cor em decimal
    )
    embed.set_author(name='AJUDA', icon_url='https://64.media.tumblr.com/1e98a29e32a889552ca8f50ccd525d7d/135a1fac54a6e0a4-67/s128x128u_c1/e906c205d04f61aeb64566ee3e213affc0226310.pnj')  # url do icone

    # url do thumbnail
    embed.set_thumbnail(
        url='https://static.wikia.nocookie.net/digimonat/images/d/d1/Gabumon_b.jpg/revision/latest?cb=20140419005946&path-prefix=pt')

#  embed.set_image(url='https://.jpg')#url do thumbnail

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Azure Lane'))
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


client.run('TOKEN')
