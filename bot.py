import discord
from discord.ext import commands
from discord.utils import get
import random
import os
import youtube_dl
from datetime import datetime
import sympy
from sympy.solvers import solve
from sympy import *

client = commands.Bot(command_prefix= '.', case_insensitive=True)
players = {}
#sp.init_session()

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')
    not_muted = get(member.guild.roles, name="not muted")
    await member.add_roles(not_muted)


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

@client.event
async def on_message(message):
    print(f'{message.author}: {message.content}')
    await client.process_commands(message)

@client.command(help = 'This command returns the latency')
async def ping(ctx):
    embedVar = discord.Embed(title=f'{round(client.latency * 1000)}ms', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(aliases = ['8ball','eightball'],help = 'Ask the Magic 8-Ball a question')
async def _8ball(ctx,*,question):
    responses = [
        "It is certain",
        "Without a doubt",
        "You may rely on it",
        "Yes definitely",
        "It is decidedly so",
        "As I see it, yes",
        "Most likely",
        "Yes",
        "Outlook good",
        "Signs point to yes",
        "Reply hazy try again",
        "Better not tell you now",
        "Ask again later",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "Outlook not so good",
        "My sources say no",
        "Very doubtful",
        "My reply is no",
        "No You"
    ]
    embedVar = discord.Embed(title=f'{random.choice(responses)}' , color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(aliases = ['cls', 'clearchat'], help = 'Clears the chat')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=10):
	await ctx.message.delete()
	await ctx.channel.purge(limit=amount)

@client.command(help = 'Displays the current time: Day/Month/Year Hour/Minute/Second ')
async def time(ctx):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    embedVar = discord.Embed(title=f'{dt_string}', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(help = 'Ban a user')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member,*,reason=None):
    await member.ban(reason=reason)
    embedVar = discord.Embed(title=f'User {member} has been banned', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(help = 'Kick a user')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member,*, reason=None):
    await member.kick(reason=reason)
    embedVar = discord.Embed(title=f'User {member} has been kicked', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(aliases = ['dice'],help = 'Roll a dice')
async def roll(ctx, sides=6):
    roll = random.randint(1, int(sides))
    embedVar = discord.Embed(title="DICE", description=f'You rolled a {roll}', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(help = 'Unban a banned user')
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator == member_name, member_discriminator):
            await ctx.guild.unban(user)
            embedVar = discord.Embed(title=f'User {user} has been unbanned', color=15105570)
            await ctx.channel.send(embed=embedVar)


@client.command(help = 'Mute a user')
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    role = get(member.guild.roles, name="Muted")
    not_muted = get(member.guild.roles, name="not muted")
    await member.add_roles(role)
    await member.remove_roles(not_muted)
    embedVar = discord.Embed(title=f'User {member} has been muted', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(help = 'Unmute a user')
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    role = get(member.guild.roles, name="Muted")
    not_muted = get(member.guild.roles, name="not muted")
    await member.remove_roles(role)
    await member.add_roles(not_muted)
    embedVar = discord.Embed(title=f'User {member} has been unmuted', color=15105570)
    await ctx.channel.send(embed=embedVar)

@client.command(aliases = ['rr','russian', 'roulette'],help ='Anatol-oele Coene-ene inspired Russian Roulette game')
async def russianroulette(ctx, *, n="6"):
    n = eval(str(n))
    if n == 1:
        raise
    messenger = ctx.author
    print(messenger)
    number_to_roll = random.randint(1,n)
    while True:
        number_to_kick = random.randint(1, n)
        if number_to_kick != number_to_roll:
            break
    print(f'Number to win: {number_to_roll}\nNumber to lose: {number_to_kick}')
    embedVar = discord.Embed(title='Russian Roulette',description=f'Choose a number between 1 and {n}', color=15105570)
    await ctx.channel.send(embed=embedVar)
    def check(author):
        def inner_check(message):
            if message.author != author:
                return False
            try:
                int(message.content)
                return True
            except ValueError:
                return False
        return inner_check
    guess = await client.wait_for('message', check=check(messenger))
    guess = int(guess.content)
    if guess == number_to_roll:
        embedVar = discord.Embed(title=f'good', color=15105570)
        await ctx.channel.send(embed=embedVar)
    elif guess == number_to_kick:
        link = await ctx.channel.create_invite(max_age=300)
        await messenger.send(f'You lost the russian roulette 😦\n You can rejoin the server with this link: {link}')
        await messenger.kick()
        embedVar = discord.Embed(title=f'User {messenger} has been kicked, Correct Answer was {number_to_roll}', color=15105570)
        await ctx.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title=f'The answer to win was {number_to_roll}\nThe answer to lose was {number_to_kick}',color=15105570)
        await ctx.channel.send(embed=embedVar)


@client.command(help = 'Says a message through DeltaV')
@commands.has_permissions(administrator=True)
async def say(ctx, *,  text):
    await clear(ctx, amount=0)
    await ctx.send(text)

@client.command(help = 'Invite DeltaV to your VC')
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command(help = 'Remove DeltaV from your VC')
async def leave(ctx):
    await ctx.voice_client.disconnect() 


# @client.command()
# async def dm(ctx,  member: discord.Member, *, message):
#     print(member)
#     await member.send(message)

@client.command(help = 'spams')
@commands.has_permissions(administrator=True)
async def spam(ctx, *, n="5"):
    n = eval(str(n))
    for i in range(n):
        await ctx.send(i+1)

@client.command(help = 'Solves algebra', aliases = ['solve'])
async def solveequa(ctx, *, equa):
    eq = str(equa).replace('\*','*')
    eq = sympy.sympify(eq)
    x = sympy.Symbol('x')
    solutions = solve(eq, x)
    for solution in solutions:
        preview(solution, viewer="file", filename="test.png",dvioptions=['-D', '600'],euler = False)
        await ctx.send(file=discord.File('test.png'))



@client.command(help = 'Solves derivatives', aliases = ['diff'])
async def differentiate(ctx, *, equa):
    eq = str(equa)
    eq = sympy.sympify(eq)
    x = sympy.Symbol('x')
    solution = diff(eq, x)
    print(solution)
    preview(solution, viewer="file", filename="test.png", dvioptions=['-D', '600'], euler=False)
    await ctx.send(file=discord.File('test.png'))

@client.command(help = 'Solves indefinite integrals', aliases = ['int'])
async def indeff_integrate(ctx, *, equa):
    eq = str(equa)
    eq = sympy.sympify(eq)
    x = sympy.Symbol('x')
    solution = integrate(eq, x)
    print(solution)
    preview(solution, viewer="file", filename="test.png", dvioptions=['-D', '600'], euler=False)
    await ctx.send(file=discord.File('test.png'))

@client.command(help = 'Solves definite integrals')
async def defint(ctx, *, equa):
    x = sympy.Symbol('x')
    lower_bound = str(equa).split(',')[1]
    upper_bound =str(equa).split(',')[2]
    equa = str(equa).split(',')[0]
    solution = integrate(equa,(x,lower_bound,upper_bound))
    preview(solution, viewer="file", filename="test.png", dvioptions=['-D', '600'], euler=False)
    await ctx.send(file=discord.File('test.png'))

@client.command(help = 'Embeds a message through DeltaV')
@commands.has_permissions(administrator=True)
async def embed(ctx, *,  text):
    await clear(ctx, amount=0)
    embedVar = discord.Embed(title=f'{text}', color=15105570)
    await ctx.channel.send(embed=embedVar)


client.run('')
