import discord
from urllib import parse, request
import re

from discord.ext import commands


class Midia(commands.Cog):
    #inicialization
    def __init__(self, bot: commands.Bot):
        self.bot = bot

 #comando de procurar no youtube
    @commands.command()
    async def youtube(self, ctx, *, search):
      query_string = parse.urlencode({'search_query': search})
      html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
      # print(html_content.read().decode())
      search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
      print(search_results)
      # I will put just the first result, you can loop the response to show more results
      await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])      

def setup(client):
  client.add_cog(Midia(client))