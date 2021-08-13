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
    @commands.command()
    @commands.has_permissions(manage_messages=True) #verifica permissao
    async def kick(self, ctx, member : discord.Member, *, reason=None):
      print(f'{member} foi kickado.')
      await member.kick(reason=reason)
    @kick.error
    async def kick_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

    #ban
    @commands.command()
    @commands.has_permissions(manage_messages=True) #verifica permissao
    async def ban(self, ctx, member : discord.Member, *, reason=None):
      print(f'{member} foi banido.')
      await member.ban(reason=reason)
      await ctx.send(f'Banido {member.mention}')
    @ban.error
    async def ban_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

    #unban
    @commands.command()
    @commands.has_permissions(manage_messages=True) #verifica permissao
    async def unban(self, ctx, *, member):
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
    async def unban_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para isso.')

  #Fim-----------Comandos ADM-------------

def setup(client):
  client.add_cog(Adm(client))