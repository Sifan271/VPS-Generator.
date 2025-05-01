import discord
from discord.ext import commands, tasks
import docker
import random
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
client = docker.from_env()
user_specs = {}
user_balances = {}

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def deploy(ctx, ram: str, cpu: int):
    user_id = str(ctx.author.id)
    if user_balances.get(user_id, 0) < 500:
        await ctx.send("❌ Not enough coins. VPS costs 500 coins.")
        return
    
    container_name = f"vps_{ctx.author.id}_{random.randint(1000,9999)}"
    try:
        container = client.containers.run(
            "ubuntu", 
            name=container_name,
            command="sleep infinity",
            detach=True,
            tty=True
        )
        user_specs[user_id] = user_specs.get(user_id, []) + [container.name]
        user_balances[user_id] -= 500
        await ctx.send(f"✅ VPS Created!\nName: {container.name}\nID: {container.id[:12]}")
    except Exception as e:
        await ctx.send(f"❌ Error creating VPS: {str(e)}")

@bot.command()
async def remove(ctx, container_name):
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
        await ctx.send(f"✅ Removed container: {container_name}")
    except:
        await ctx.send("❌ Could not remove container.")

@bot.command()
async def remove_all(ctx):
    containers = client.containers.list()
    for container in containers:
        container.remove(force=True)
    await ctx.send("✅ All containers removed.")

@bot.command()
async def clear_specs(ctx):
    user_id = str(ctx.author.id)
    user_specs[user_id] = []
    await ctx.send("✅ Specs cleared.")

@bot.command()
async def balance(ctx):
    coins = user_balances.get(str(ctx.author.id), 0)
    await ctx.send(f"💰 You have {coins} coins.")

@bot.command()
async def work(ctx):
    user_id = str(ctx.author.id)
    earnings = random.randint(10, 30)
    user_balances[user_id] = user_balances.get(user_id, 0) + earnings
    await ctx.send(f"💼 You worked and earned {earnings} coins!")
    await asyncio.sleep(60)

@bot.command()
async def crime(ctx):
    user_id = str(ctx.author.id)
    chance = random.randint(1, 100)
    if chance <= 45:
        earnings = random.randint(10, 40)
        user_balances[user_id] = user_balances.get(user_id, 0) + earnings
        await ctx.send(f"🔫 Crime success! You stole {earnings} coins!")
    else:
        loss = random.randint(5, 20)
        user_balances[user_id] = max(0, user_balances.get(user_id, 0) - loss)
        await ctx.send(f"🚨 You got caught and lost {loss} coins!")

@bot.command()
async def giveaway(ctx, amount: int):
    if amount <= 0:
        await ctx.send("❌ Amount must be positive.")
        return
    winner = random.choice(ctx.guild.members)
    if winner.bot:
        await ctx.send("⚠️ Rerolling... winner was a bot.")
        return
    user_balances[str(winner.id)] = user_balances.get(str(winner.id), 0) + amount
    await ctx.send(f"🎉 {winner.mention} won the giveaway and received {amount} coins!")

bot.run("YOUR_DISCORD_BOT_TOKEN")
