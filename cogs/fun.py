import discord
import random
import time

from discord.ext import commands


class Funny(commands.Cog):
    # inicialization
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('O BOT está online')

    # comando de ping
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Obtem a latência do bot."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    # comando de olá
    @commands.command()
    async def ola(self, ctx: commands.Context):
        """Apresentação"""
        await ctx.send(f'Olá, {ctx.author} tudo bem? Meu prefixo por padrão é "."')

    # comando 8ball
    @commands.command(aliases=['8ball', 'test'])
    async def _8ball(self, ctx, *, question):
        responses = ["Sim.",
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
        await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

    # comando de erro do 8ball
    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Você tem que digitar uma pergunta.')


def setup(client):
    client.add_cog(Funny(client))
