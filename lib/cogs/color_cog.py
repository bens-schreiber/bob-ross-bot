from discord.ext import commands
from discord.ext.commands import Context
from colour import Color
from no_sql.no_sql import colors_collection, UserColor

class ColorCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def colorme(self, ctx: Context, color: str = "#FFFFFF"):
        """Change your color to the given hex color code."""
        try:
            color: Color = Color(color)
        except ValueError:
            await ctx.send("Invalid color code!")
            return
        
        color_hex: int = color.hex.lstrip("#")
        
        colors_collection().update_one(
            {"user": ctx.author.id},
            {"$set": {"color": color_hex}},
            upsert=True
        )
        await ctx.send(f"Your color has been set to `{color.hex_l}`!")

    @commands.command()
    async def color(self, ctx: Context):
        """Get the color of a user."""
        item = colors_collection().find_one(UserColor(user=ctx.author.id))
        if item is None:
            await ctx.send("That user does not have a color!")
            return
        color = Color(f"#{item['color']}")
        
        await ctx.send(f"{ctx.author.mention}'s color is `{color}`")

async def setup(client):
    await client.add_cog(ColorCog(client))