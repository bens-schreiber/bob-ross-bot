import os
import discord
from discord.ext import commands

async def load_cogs(bot):
    """Load all cogs from the cogs directory."""

    for cog in os.listdir('./lib/cogs'):
        if cog.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{cog[:-3]}')
                print(f'Loaded cog {cog}')
            except Exception as e:
                print(f'Failed to load cog {cog}: {e}')

async def on_ready(bot):
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    async with bot := commands.Bot():
        await load_cogs(bot)
        await bot.add_listener(on_ready)
        await bot.start(os.environ["PYTHON_BOT_TOKEN"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
