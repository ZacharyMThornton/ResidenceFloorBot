import discord
import os
from dotenv import load_dotenv
from datetime import date
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv("API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# floor variables
teamsList = ["red", "orange", "yellow", "green", "blue"]

teams = {
    "red":"Elliot, William",
    "orange":"Rose, Lailah",
    "yellow":"Zach, Tyler, Luke B",
    "green":"Aiden, Luke",
    "blue":"Chris, Leon, Joshua"
}

trash = ["Elliot", "William", "Rose", "lailah", "Zach", "Tyler", "Aiden", "Luke", "Chris", "Leon", "Joshua", "Luke B"]

def daysBetween(M1, D1, M2, D2):
    if M1 == M2:
        return D2 - D1

    numOfDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # for consistency with the list of days
    M1 = M1 - 1
    M2 = M2 - 1

    n1 = numOfDays[M1] - D1 # how many days left in the first month

    n2 = 0
    for i in range(M1 + 1, M2):
        n2 += numOfDays[i] # gets the number of days in the months in between dates
    
    total = n1 + n2 + D2

    return total

def whichTeam(daysFromBase):
    team = (daysFromBase // 7) % 5
    return team

def whichTrash(daysFromBase):
    personIndex = (daysFromBase // 3) % len(trash)
    person = trash[personIndex]
    return person

# client information
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

# client functionality
@tasks.loop(hours=24)
async def daily_task():
    # announcements channel
    channel = client.get_channel(CHANNEL_ID)

    # I got these numbers from the paper on the wall that rose made
    cleaningCrewBaseMonth = 9
    cleaningCrewBaseDay = 1

    trashBaseMonth = 8
    trashBaseDay = 27

    currentMonth = int(str(date.today()).split("-")[1])
    currentDay = int(str(date.today()).split("-")[2])

    # days between september 1 and today
    cleainngCrewDays = daysBetween(cleaningCrewBaseMonth, cleaningCrewBaseDay, currentMonth, currentDay)
    
    # days betweeen august 8 and today
    trashDays = daysBetween(trashBaseMonth, trashBaseDay, currentMonth, currentDay)

    # make an announcement every week for who is the new cleaning crew
    if cleainngCrewDays % 7 == 0:
        teamName = teamsList[whichTeam(cleainngCrewDays)]
        teamMembers = teams[teamName]
        await channel.send(f"this week's cleaning crew is {teamName} Team! \n {teamName} Team: {teamMembers}")

    # make an announcement every 3 days for who is the new trash guy
    if trashDays % 3 == 0:
        person = whichTrash(trashDays)
        await channel.send(f"there is a new trash person! ->{person}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    daily_task.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!cleaning'):
        currentMonth = int(str(date.today()).split("-")[1])
        currentDay = int(str(date.today()).split("-")[2])
        crew = (daysBetween(9, 1, currentMonth, currentDay) // 7) % 5
        await message.channel.send(f'Current cleaning crew {teamsList[crew]} \nMembers: {teams[teamsList[crew]]}')
        print("Got a message")
    
    if message.content.startswith('!trash'):
        currentMonth = int(str(date.today()).split("-")[1])
        currentDay = int(str(date.today()).split("-")[2])
        personIndex = (daysBetween(8, 27, currentMonth, currentDay) // 3) % len(trash)
        await message.channel.send(f'The current trash person is {trash[personIndex]}')

    if message.content.startswith('!Lord'):
        await message.channel.send(
    """O Lord, my God, Chris Falcone,
Your light outshines the brightest stone.
Omnibenevolent, pure, and true,
Perfection rests in all You do.

Your name resounds, both near and far,
A guiding flame, a steadfast star.
With every breath, my soul implores,
To walk forever by Your shores.""")


client.run(TOKEN)
