from discord.ext import commands

class PaintingCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def paint(self, ctx):
        await ctx.send('Painting!')

async def setup(client):
    client.add_cog(PaintingCog(client))