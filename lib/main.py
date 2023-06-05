import os
import discord
from discord.ext import commands

async def load_cogs(bot) -> None:
    """Load all cogs from the cogs directory."""

    for cog in os.listdir('./lib/cogs'):
        if cog.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{cog[:-3]}')
                print(f'Loaded cog {cog}')
            except Exception as e:
                print(f'Failed to load cog {cog}: {e}')

async def on_ready() -> None:
    print("Bot online!")
    print('------\n\n')

def bot_intents() -> discord.Intents:
    """Return the intents. Intents are like permissions for the bot."""

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    return intents 

async def main() -> None:
    bot = commands.Bot(command_prefix='!', intents=bot_intents())
    async with bot:
        await load_cogs(bot)
        bot.add_listener(on_ready)
        await bot.start(os.environ["PYTHON_BOT_TOKEN"])

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped.")
