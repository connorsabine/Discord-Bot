import lightbulb
import hikari
import random
import miru
from constants import FAILED_COLOR, SUCCESS_COLOR, NORMAL_COLOR

# INIT
plugin = lightbulb.Plugin("anagrams")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

words = ["centers", "starter"]
currentGames = {}

def getRandom():
    return words.index(random.choice(words))

def parseId(embed):
    return embed.description.split()

def getLetters(id):
    letters = []
    for letter in random.sample(words[id], len(words[id])):
        letters.append(letter.upper())
    return letters

def generateEmbed():
    id = getRandom()
    letters = getLetters(id)
    
    title = "Letters: **"
    description = f"ID: {id}"

    for letter in letters:
        title += letter + " "
    title += "**"

    embed = hikari.Embed(title=title, description=description, color = NORMAL_COLOR)
    return embed

def updateEmbed(id, scoredWords, totalScore):
    id = parseId()
    letters = getLetters(id)
    
    title = "Letters: **"
    description = f"ID: {id}"

    for letter in letters:
        title += letter + " "
    title += "**"
    
    if totalScore > 0:
        description = "** Score: " + str(totalScore) + "**"
        for word in scoredWords:
            description += "\n- " + word

    embed = hikari.Embed(title=title, description=description, color = NORMAL_COLOR)
    return embed
        

# COMMANDS
@plugin.command
@lightbulb.command("anagram", "Starts a Game of Anagrams")
@lightbulb.implements(lightbulb.SlashCommand)
async def anagram(ctx: lightbulb.Context) -> None:
    await ctx.respond(embed=generateEmbed())



