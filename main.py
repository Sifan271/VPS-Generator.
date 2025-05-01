import discord
from discord.ext import commands, tasks
import os
import random
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_balances = {}
user_cooldowns = {}
vps_price = 500

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def cash(ctx):
    coins = user_balances.get(ctx.author.id, 0)
    await ctx.send(f"💰 You have {coins} coins.")

@bot.command()
async def work(ctx):
    user_id = ctx.author.id
    if user_id in user_cooldowns and asyncio.get_event_loop().time() - user_cooldowns[user_id] < 60:
        await ctx.send("⏳ You need to wait 1 minute before working again.")
        return
    user_cooldowns[user_id] = asyncio.get_event_loop().time()
    earnings = random.randint(10, 20)
    user_balances[user_id] = user_balances.get(user_id, 0) + earnings
    await ctx.send(f"👷 You worked hard and earned {earnings} coins!")

@bot.command()
async def crime(ctx):
    user_id = ctx.author.id
    outcome = random.choices(["win", "lose"], weights=[45, 55])[0]
    if outcome == "win":
        earnings = random.randint(50, 150)
        user_balances[user_id] = user_balances.get(user_id, 0) + earnings
        await ctx.send(f"🕵️ You succeeded in a crime and stole {earnings} coins!")
    else:
        loss = random.randint(30, 100)
        user_balances[user_id] = max(user_balances.get(user_id, 0) - loss, 0)
        await ctx.send(f"🚨 You got caught and lost {loss} coins!")

@bot.command()
async def shop(ctx):
    await ctx.send(f"🛒 VPS Shop:\n- VPS: {vps_price} coins\nUse `!shop_buy_vps` to purchase.")

@bot.command(name="shop_buy_vps")
async def shop_buy_vps(ctx):
    user_id = ctx.author.id
    if user_balances.get(user_id, 0) >= vps_price:
        user_balances[user_id] -= vps_price
        await ctx.send("✅ You bought a VPS!")
    else:
        await ctx.send("❌ Not enough coins!")

@bot.command()
async def coinflip(ctx, bet: int):
    user_id = ctx.author.id
    if user_balances.get(user_id, 0) < bet:
        await ctx.send("❌ Not enough coins to bet.")
        return
    result = random.choice(["heads", "tails"])
    if result == "heads":
        user_balances[user_id] += bet
        await ctx.send(f"🎉 You won! (+{bet})")
    else:
        user_balances[user_id] -= bet
        await ctx.send(f"😢 You lost! (-{bet})")

@bot.command()
async def spins(ctx, bet: int):
    user_id = ctx.author.id
    if user_balances.get(user_id, 0) < bet:
        await ctx.send("❌ Not enough coins to spin.")
        return
    prize = random.choices([0, bet * 2], weights=[60, 40])[0]
    user_balances[user_id] = user_balances.get(user_id, 0) - bet + prize
    if prize > 0:
        await ctx.send(f"🎰 Lucky spin! You won {prize} coins!")
    else:
        await ctx.send("🎰 Unlucky spin. You got nothing.")

@bot.command()
async def hunt(ctx, bet: int):
    user_id = ctx.author.id
    if user_balances.get(user_id, 0) < bet:
        await ctx.send("❌ Not enough coins to hunt.")
        return
    prize = random.choices([0, bet * 3], weights=[70, 30])[0]
    user_balances[user_id] = user_balances.get(user_id, 0) - bet + prize
    if prize > 0:
        await ctx.send(f"🏹 You hunted a big animal and earned {prize} coins!")
    else:
        await ctx.send("🏹 Hunt failed. No coins for you.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member.mention}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member.mention}")

@bot.command()
async def giveaway(ctx, amount: int):
    await ctx.send(f"🎁 A giveaway has started! React with 🎉 to enter. Prize: {amount} coins!")
    msg = await ctx.send("🎉 React here to join the giveaway!")
    await msg.add_reaction("🎉")

    await asyncio.sleep(10)  # 10 seconds for testing
    msg = await ctx.channel.fetch_message(msg.id)
    users = await msg.reactions[0].users().flatten()
    users = [user for user in users if not user.bot]

    if users:
        winner = random.choice(users)
        user_balances[winner.id] = user_balances.get(winner.id, 0) + amount
        await ctx.send(f"🎉 Congratulations {winner.mention}, you won {amount} coins!")
    else:
        await ctx.send("😢 No one entered the giveaway.")

import os
from dotenv import load_dotenv
load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
