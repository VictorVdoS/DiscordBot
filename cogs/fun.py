import discord
import random

from discord.ext import commands


class Jogos(commands.Cog):
    #inicialization
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #events
    @commands.Cog.listener()
    async def on_ready(self):
      print('O BOT está online')

    #comando 8ball
    @commands.command(aliases=['8ball', 'test'])
    async def _8ball(self, ctx, *, pergunta):
      resposta = ["Sim.",
      "Sem sombra de dúvidas.",
      "Obvio.",
      "Definitiviamente sim.",
      "Você pode contar com ele.",
      "A meu ver, sim.",
      "Provavelmente.",
      "Parace bom.",
      "Sinais apontam que sim.",
      "Resposta nebulosa, tente novamente.",
      "Pergunte novamente mais tarde.",
      "Melhor não te dizer agora.",
      "Não posso prever agora.",
      "Concentre-se e pergunte novamente.",
      "Não conte com isso.",
      "Minha resposta é não.",
      "Minhas fontes dizem não.",
      "Parece que não é tão bom.",
      "Muito duvidoso."]
      await ctx.send(f'Pergunta: {pergunta}\n Resposta: {random.choice(resposta)}')

    #comando de erro do 8ball
    @_8ball.error
    async def _8ball_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Você tem que digitar uma pergunta.')

    #comando de dado
    @commands.command()
    async def roll(self, ctx: commands.Context, dice: str):
      """Joga um Dado"""
      try:
        rolls = ""
        amount, die = dice.split("d")
        for _ in range(int(amount)):
          roll = random.randint(1, int(die))
          rolls += f"{roll}, "
        await ctx.send( rolls)
      except ValueError:
        await ctx.send("O dado tem que ser no formato _d_(exemplo: 2d6)")

    @roll.error
    async def roll_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Você tem que digitar o dado no segunte formato (exemplo: 2d6).')

def setup(client):
  client.add_cog(Jogos(client))