import discord
import random
import requests
from discord.ext import commands
from discord import app_commands

#----------------------------------------------------

#TOKEN
TOKEN = "TOKEN"

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up !!!",
    "Hang in there.",
    "You are a great person / bot!!",
    "Be strong.",
    "Look on the bright side.",
    "Every cloud has a silver lining.",
    "Don’t give up.",
    "It’s gonna be ok.",
    "You’ll get through this.",
]

menu = ['Rice congee', 'Braised pork leg on rice', 'Omelette', 'Thai chicken biryani'
        , 'Chicken rice', 'Crispy pork on rice', 'Freid rice', 'Noodle', 'Thai suki'
        , 'Green curry', 'Red curry', 'Tom yum soup']

#-----------------------------------------------------
#function
def get_dog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    image_link = response.json()["message"]
    return image_link

def get_quotes(category):
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': '5bBIThquN+dWIKtAzpMw5Q==JPbAhwl3r3p1mZUh'})
    if response.status_code == requests.codes.ok:
        quotes = response.json()
    return quotes
#-----------------------------------------------------
bot = commands.Bot(command_prefix='*',intents=discord.Intents.all())

#start -------------------------------------------------
@bot.event
async def on_ready():
    print("Bot Online!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")


#in & out server ----------------------------------------
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(696914894142046221)#Channel ID
    text = f"Welcome to the server, {member.mention}"
    await channel.send(text) #send text

    emmbed = discord.Embed(title = 'Welcome to Chabee Server!',
                        description = text,
                        color = 0x5865F2)
    await channel.send(embed=emmbed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(696914894142046221)#Channel ID
    text = f"{member.mention} has left to server!"
    await channel.send(text) #send text

#on message ----------------------------------------------
@bot.event
async def on_message(message):
    mes = message.content
    if any(word in mes for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

    elif mes == 'hi bot':
        await message.channel.send("Hello, " + str(message.author.name))

    await bot.process_commands(message)

#command -> test -----------------------------------------
@bot.command()
async def test(ctx, arg): 
    await ctx.send(arg)

#slash cammand ><><><><><><><><><><><><><><><><><><><><><><>
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

@bot.tree.command(name='name')
@app_commands.describe(name = "What's your name?")
async def namecommand(interaction, name : str):
    await interaction.response.send_message(f"Hello {name}")

@bot.tree.command(name='random-menu', description='Random menu for you')
async def random_menu(interaction):
    menu_choice = random.choice(menu)
    await interaction.response.send_message(f"Your menu is {menu_choice}")

@bot.tree.command(name='dog-img', description="Replies cute dog image")
async def dog_img(interaction):
    dog_link = get_dog()
    await interaction.response.send_message(dog_link)

@bot.tree.command(name='quote', description='Random quote')
async def random_quote(interaction, name: str):
    quotes = get_quotes(category=name)
    ans_quote = quotes[0]["quote"]
    ans_author = quotes[0]["author"]
    ans_category = quotes[0]["category"]
    emmbed = discord.Embed(title='Quote',
                        description='This is your quote.',
                        color=0x66FFFF,
                        timestamp=discord.utils.utcnow())
    emmbed.add_field(name='quote :',value=f'{ans_quote}', inline=False)
    emmbed.add_field(name='author :',value=f'{ans_author}')
    emmbed.add_field(name='category',value=f'{ans_category}')
    await interaction.response.send_message(embed=emmbed)

bot.run(TOKEN)