import discord

from discord.ext import commands


class Adm(commands.Cog):
    #inicialization
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#----------------------------------Comandos ADM--------------------------------------------
  #clear
    @commands.command()
    @commands.has_permissions(manage_messages=True) #verifica permissao
    async def clear(self, ctx, amount=10):
      await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')


    #kick
    
    #softban

    #ban
    
    #unban
    
  #Fim-----------Comandos ADM-------------

def setup(client):
  client.add_cog(Adm(client))