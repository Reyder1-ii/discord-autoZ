import discord
from discord.ext import commands
from aiohttp import web
import asyncio
import os

discord.VoiceClient.warn_nacl = False

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def replace_letters(text: str) -> str:
    if not text:
        return text
    text = text.replace('S', 'Z').replace('s', 'Z')
    text = text.replace('С', 'Z').replace('с', 'Z')
    text = text.replace('C', 'Z').replace('C', 'Z')
    return text

async def check_and_rename(member: discord.Member):
    current_name = member.display_name
    new_name = replace_letters(current_name)
    
    if current_name != new_name:
        try:
            await member.edit(nick=new_name)
        except:
            pass

@bot.event
async def on_ready():
    # check all players
    for guild in bot.guilds:
        async for member in guild.fetch_members(limit=None):
            await check_and_rename(member)

@bot.event
async def on_member_join(member):
    await check_and_rename(member)

@bot.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        await check_and_rename(after)

async def handle(request):
    return web.Response(text="OK")

async def start_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    async with bot:
        bot.loop.create_task(start_server())
        token = os.environ.get("DISCORD_TOKEN")
        if token:
            await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
