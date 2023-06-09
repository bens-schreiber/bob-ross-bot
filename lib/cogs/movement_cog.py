from discord.ext import commands
from discord.ext.commands import Context
from no_sql.no_sql import set_user_coordinates, find_user_coordinates


class MovementCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def move(self, ctx: Context, direction: str = "up", length: int = 10):
        """Move in a direction. Valid directions are `up`, `down`, `left`, and `right`. Length is default 10"""

        if (direction not in ["up", "down", "left", "right"]):
            await ctx.send("Invalid direction! Use `up`, `down`, `left`, or `right`.")
            return

        coordinates = find_user_coordinates(ctx.author.id)

        # Define the dictionary mapping direction values to operations
        direction_dict = {
            "up": lambda x, y, length: (x, y - length),
            "down": lambda x, y, length: (x, y + length),
            "left": lambda x, y, length: (x - length, y),
            "right": lambda x, y, length: (x + length, y)
        }

        coordinates = direction_dict[direction](
            coordinates[0], coordinates[1], length) if coordinates is not None else direction_dict[direction](0, 0, length)

        set_user_coordinates(ctx.author.id, coordinates)

        await ctx.send(f"Moved to {coordinates}!")

    @commands.command()
    async def where(self, ctx: Context):
        """Get your current coordinates."""
        coordinates = find_user_coordinates(ctx.author.id)
        if coordinates is None:
            await ctx.send("You have not moved yet!")
            return

        await ctx.send(f"Your current coordinates are {coordinates}!")
    
    @commands.command()
    async def reset(self, ctx: Context):
        """Reset your coordinates to (0,0)"""
        set_user_coordinates(ctx.author.id, (0, 0))
        await ctx.send("Your coordinates have been reset to (0, 0)!")


async def setup(client):
    await client.add_cog(MovementCog(client))
