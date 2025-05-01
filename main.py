import discord
from discord.ext import commands, tasks
import asyncio
import random
import time

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_data = {}
shop_items = {'vps': 500}  # VPS price increased
cooldowns = {}
giveaways = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def cash(ctx):
    uid = str(ctx.author.id)
    user_data.setdefault(uid, {'coins': 0})
    await ctx.send(f"{ctx.author.mention}, you have {user_data[uid]['coins']} coins.")

@bot.command()
async def work(ctx):
    uid = str(ctx.author.id)
    now = time.time()
    if uid in cooldowns and now - cooldowns[uid] < 60:
        await ctx.send("⏳ You need to wait 1 minute before working again.")
        return
    earned = random.randint(5, 15)
    user_data.setdefault(uid, {'coins': 0})
    user_data[uid]['coins'] += earned
    cooldowns[uid] = now
    await ctx.send(f"💼 You worked and earned {earned} coins!")

@bot.command()
async def crime(ctx):
    uid = str(ctx.author.id)
    user_data.setdefault(uid, {'coins': 0})
    if random.random() < 0.45:
        earned = random.randint(20, 50)
        user_data[uid]['coins'] += earned
        await ctx.send(f"🕵️ You committed a crime and got {earned} coins!")
    else:
        loss = random.randint(10, 30)
        user_data[uid]['coins'] = max(0, user_data[uid]['coins'] - loss)
        await ctx.send(f"🚓 You got caught and lost {loss} coins!")

@bot.command()
async def shop(ctx):
    items = '\n'.join([f"{item}: {price} coins" for item, price in shop_items.items()])
    await ctx.send(f"🛒 Shop:\n{items}")

@bot.command()
async def shop_buy_vps(ctx):
    uid = str(ctx.author.id)
    user_data.setdefault(uid, {'coins': 0})
    price = shop_items['vps']
    if user_data[uid]['coins'] >= price:
        user_data[uid]['coins'] -= price
        await ctx.send("✅ VPS Purchased! Use !deploy to set it up.")
    else:
        await ctx.send("❌ Not enough coins.")

@bot.command()
async def coinflip(ctx, amount: int):
    uid = str(ctx.author.id)
    user_data.setdefault(uid, {'coins': 0})
    if amount > user_data[uid]['coins'] or amount <= 0:
        await ctx.send("❌ Invalid amount.")
        return
    if random.choice([True, False]):
        user_data[uid]['coins'] += amount
        await ctx.send(f"🪙 You won the coinflip! +{amount} coins")
    else:
        user_data[uid]['coins'] -= amount
        await ctx.send(f"🪙 You lost the coinflip! -{amount} coins")

@bot.command()
async def spins(ctx, amount: int):
    uid = str(ctx.author.id)
    user_data.setdefault(uid, {'coins': 0})
    if amount > user_data[uid]['coins'] or amount <= 0:
        await ctx.send("❌ Invalid amount.")
        return
    outcome = random.choices(['win', 'lose'], weights=[0.3, 0.7])[0]
    if outcome == 'win':
        gain = int(amount * 1.5)
        user_data[uid]['coins'] += gain
        await ctx.send(f"🎰 You won {gain} coins!")
    else:
        user_data[uid]['coins'] -= amount
        await ctx.send(f"🎰 You lost {amount} coins!")

@bot.command()
async def hunt(ctx):
    uid = str(ctx.author.id)
    found = random.choices([True, False], weights=[0.4, 0.6])[0]
    amount = random.randint(5, 20)
    user_data.setdefault(uid, {'coins': 0})
    if found:
        user_data[uid]['coins'] += amount
        await ctx.send(f"🏹 You hunted and got {amount} coins!")
    else:
        user_data[uid]['coins'] = max(0, user_data[uid]['coins'] - amount)
        await ctx.send(f"🏹 You failed the hunt and lost {amount} coins!")

@bot.command()
async def giveaway(ctx, amount: int):
    if amount <= 0:
        await ctx.send("❌ Amount must be more than 0.")
        return
    await ctx.send(f"🎉 Giveaway started for {amount} coins! React with 🎉 to enter.")
    msg = await ctx.send("React to this message to join the giveaway!")
    await msg.add_reaction("🎉")

    await asyncio.sleep(10)  # giveaway duration
    msg = await ctx.channel.fetch_message(msg.id)
    users = [user async for user in msg.reactions[0].users() if not user.bot]
    if not users:
        await ctx.send("No one entered the giveaway.")
        return
    winner = random.choice(users)
    uid = str(winner.id)
    user_data.setdefault(uid, {'coins': 0})
    user_data[uid]['coins'] += amount
    await ctx.send(f"🎊 {winner.mention} won {amount} coins!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def lkick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} has been kicked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} has been banned.")

bot.run('MTM2MTQzMDY5ODUzMTIyNTcwNg.GfmXIZ.aPH4oDEbD7nC6jBgGGJ1wqUym6lTzDeNlwAv90')
