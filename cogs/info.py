import discord
import datetime

from discord.ext import commands


class Info(commands.Cog):
    #inicialization
    def __init__(self, bot: commands.Bot):
        self.bot = bot

     #comando de ping
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Obtem a latência do bot."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms") 
          
    #comando de olá
    @commands.command()
    async def ola(self, ctx: commands.Context):
      """Apresentação"""
      await ctx.send(f'Olá, {ctx.author} tudo bem? Meu prefixo por padrão é "."')    

    #comando de ajuda
    @commands.command()
    async def ajuda(self, ctx):
      embed = discord.Embed(
      #  title = 'AJUDA',
        description = 'BOT em criação, aprecie todas as usabilidades dele, não se esqueça que o comando prefixo neste canal é o "="',
        colour = 6666111 #cor em decimal
      )
      embed.set_author(name='AJUDA', icon_url='https://64.media.tumblr.com/1e98a29e32a889552ca8f50ccd525d7d/135a1fac54a6e0a4-67/s128x128u_c1/e906c205d04f61aeb64566ee3e213affc0226310.pnj') #url do icone

      embed.set_thumbnail(url='https://static.wikia.nocookie.net/digimonat/images/d/d1/Gabumon_b.jpg/revision/latest?cb=20140419005946&path-prefix=pt')#url do thumbnail
    #  embed.set_image(url='https://4.bp.blogspot.com/-9JXkNq-2Hkg/WLNhFZYz7qI/AAAAAAAAcfU/5w0avymCZN8kDjuIV0bFYpZxXR7_x7IagCLcB/s1600/Digimon%2B01%2B-%2B2%2B-%2BGabumon.jpg')#url do thumbnail

      embed.set_footer(text='Qualquer duvida pode me chamar no privado')

    # embed.add_field(name='Nome do Field1', value='Valor do Field1', inline=False)
    # embed.add_field(name='Nome do Field2', value='Valor do Field2', inline=True)
    # embed.add_field(name='Nome do Field3', value='Valor do Field3', inline=True)

      await ctx.send(embed = embed)

    @commands.command()
    async def info(self, ctx):
      embed = discord.Embed(title=f'{ctx.guild.name}', description=' ', timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
      embed.add_field(name ='Servidor criado no dia', value = ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline = False)
      embed.add_field(name='Dono do servidor', value=f'{ctx.guild.owner}')
      embed.add_field(name='Região do servidor', value=f'{ctx.guild.region}')
      embed.add_field(name='Servidor ID', value=f'{ctx.guild.id}')
      embed.set_thumbnail(url =f'{ctx.guild.icon_url}')
      embed.set_footer(icon_url = f'{ctx.author.avatar_url}', text = f'Solicitado por: {ctx.author.name}')
      await ctx.send(embed=embed) 
def setup(client):
  client.add_cog(Info(client))