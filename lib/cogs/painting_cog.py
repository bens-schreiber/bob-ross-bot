from discord.ext import commands
from discord.ext.commands import Context
from painter.painter import *
from no_sql.no_sql import find_user_color, find_user_coordinates, set_user_coordinates


class PaintingCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def paint(self, ctx: Context, direction: str = "up", length: int = 10):
        item = find_user_color(ctx.author.id)
        if item is None:
            await ctx.send("You do not have a color! Use `colorme` to get one!")
            return
        if direction not in ["up", "down", "left", "right"]:
            await ctx.send("Invalid direction! Use `up`, `down`, `left`, or `right`.")
            return

        coordinates = find_user_coordinates(ctx.author.id)

        # draw line returns the new coordinates.
        # python can't pass in None as a value to get the default value, so we have to do this crap
        coordinates = draw_line_on_image(color=Color(
            f"#{item['color']}"), direction=direction, length=length) \
            if coordinates is None else draw_line_on_image(color=Color(
                f"#{item['color']}"), direction=direction, length=length, start=coordinates)

        set_user_coordinates(ctx.author.id, coordinates)

        embed, file = await get_discord_embed()
        await ctx.send(embed=embed, file=file)


async def setup(client):
    await client.add_cog(PaintingCog(client))
