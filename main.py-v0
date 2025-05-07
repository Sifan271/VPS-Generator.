import discord
from discord.ext import commands, tasks
import random
import asyncio
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

coins = {}
last_work_time = {}
vps_price = 500

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def get_coins(user_id):
    return coins.get(user_id, 0)

def add_coins(user_id, amount):
    coins[user_id] = get_coins(user_id) + amount

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def work(ctx):
    now = time.time()
    uid = ctx.author.id
    if uid in last_work_time and now - last_work_time[uid] < 60:
        await ctx.send("🕒 Cooldown: Try again in 1 minute.")
        return
    earned = random.randint(20, 50)
    add_coins(uid, earned)
    last_work_time[uid] = now
    await ctx.send(f"💼 You worked hard and earned {earned} coins!")

@bot.command()
async def crime(ctx):
    uid = ctx.author.id
    if random.random() < 0.45:
        earned = random.randint(50, 100)
        add_coins(uid, earned)
        await ctx.send(f"💰 Successful crime! You gained {earned} coins.")
    else:
        lost = min(get_coins(uid), random.randint(30, 70))
        coins[uid] -= lost
        await ctx.send(f"🚓 You got caught and lost {lost} coins.")

@bot.command()
async def shop(ctx):
    await ctx.send(f"🛒 VPS - {vps_price} coins\nUse `!buy-vps` to purchase.")

@bot.command()
async def buy_vps(ctx):
    uid = ctx.author.id
    if get_coins(uid) >= vps_price:
        coins[uid] -= vps_price
        await ctx.send("✅ VPS purchased!")
    else:
        await ctx.send("❌ Not enough coins.")

@bot.command()
async def coinflip(ctx, bet: int):
    uid = ctx.author.id
    if get_coins(uid) < bet:
        return await ctx.send("❌ Not enough coins.")
    if random.choice([True, False]):
        add_coins(uid, bet)
        await ctx.send(f"🪙 You won {bet} coins!")
    else:
        coins[uid] -= bet
        await ctx.send(f"😢 You lost {bet} coins.")

@bot.command()
async def hunt(ctx, bet: int):
    uid = ctx.author.id
    if get_coins(uid) < bet:
        return await ctx.send("❌ Not enough coins.")
    if random.random() < 0.5:
        reward = bet * 2
        add_coins(uid, reward)
        await ctx.send(f"🏹 You hunted and earned {reward} coins!")
    else:
        coins[uid] -= bet
        await ctx.send(f"🌲 You found nothing and lost {bet} coins.")

@bot.command()
async def spin(ctx, bet: int):
    uid = ctx.author.id
    if get_coins(uid) < bet:
        return await ctx.send("❌ Not enough coins.")
    outcome = random.choice(["win", "lose"])
    if outcome == "win":
        reward = int(bet * 1.5)
        add_coins(uid, reward)
        await ctx.send(f"🎰 Spin win! You gained {reward} coins.")
    else:
        coins[uid] -= bet
        await ctx.send(f"🎰 Spin lose! You lost {bet} coins.")

@bot.command()
async def giveaway(ctx, amount: int):
    if get_coins(ctx.author.id) < amount:
        return await ctx.send("❌ Not enough coins for giveaway.")
    coins[ctx.author.id] -= amount
    await ctx.send(f"🎉 Giveaway started for {amount} coins! React with 🎉 to join.")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member.mention}")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member.mention}")

@bot.command()
async def cash(ctx):
    await ctx.send(f"💰 You have {get_coins(ctx.author.id)} coins.")

bot.run("YOUR_TOKEN_HERE")
