import lightbulb
import hikari
import random as rand
from constants import BOT_UID, SUCCESS_COLOR, NORMAL_COLOR, FAILED_COLOR, EMOJI_CODES
import re
from typing import List, Optional
from datetime import datetime, date

# INIT
plugin = lightbulb.Plugin("wordle")
popularWords = open("src/ext/games/wordle/dict-popular.txt").read().splitlines()
allWords = set(word.strip() for word in open("src/ext/games/wordle/dict-sowpods.txt"))

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# LISTENERS
@plugin.listener(hikari.MessageCreateEvent)
async def message(event):
    try:
      await processGuess(event.message)
    except:
      return

# COMMANDS
@plugin.command
@lightbulb.command("wordle", "Play Wordle on Discord")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def wordle(ctx: lightbulb.Context) -> None:
    await ctx.respond("Wordle Invoked")

@wordle.child
@lightbulb.command("random", "Starts a Random Game of Wordle")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def random(ctx: lightbulb.Context) -> None:
    id = rand.randint(0, len(popularWords) - 1)
    embed = generatePuzzleEmbed(ctx.author, id)
    await ctx.respond(embed=embed)

@wordle.child
@lightbulb.option("id", "The ID of the Game")
@lightbulb.command("id", "Starts a Game of Wordle Based on ID")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def byid(ctx: lightbulb.Context) -> None:
    id = ctx.options.id
    if id > 2990 or id < 0:
        await ctx.respond("Please Enter a Valid ID (0-2990)")
    else:
        embed = generatePuzzleEmbed(ctx.author, id)
        await ctx.respond(embed=embed)

@wordle.child
@lightbulb.command("daily", "Starts Daily Game of Wordle")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def daily(ctx: lightbulb.Context) -> None:
    id = datetime.now().timetuple().tm_yday
    embed = generatePuzzleEmbed(ctx.author, id)
    await ctx.respond(embed=embed)

def generateColoredWord(guess: str, answer: str) -> str:
    coloredWord = [EMOJI_CODES["gray"][letter] for letter in guess]
    guessLetters: List[Optional[str]] = list(guess)
    answerLetters: List[Optional[str]] = list(answer)

    for i in range(len(guessLetters)):
        if guessLetters[i] == answerLetters[i]:
            coloredWord[i] = EMOJI_CODES["green"][guessLetters[i]]
            answerLetters[i] = None
            guessLetters[i] = None
    for i in range(len(guessLetters)):
        if guessLetters[i] is not None and guessLetters[i] in answerLetters:
            coloredWord[i] = EMOJI_CODES["yellow"][guessLetters[i]]
            answerLetters[answerLetters.index(guessLetters[i])] = None
    return "".join(coloredWord)


def generatePuzzleEmbed(user: hikari.User, puzzleid: int) -> hikari.Embed:
    embed = hikari.Embed(title=f"Wordle (ID: {puzzleid})", description="\n".join(["\N{WHITE LARGE SQUARE}" * 5] * 6))
    embed.color = NORMAL_COLOR
    embed.set_author(name=user.username, icon=user.display_avatar_url)
    embed.set_footer(text="To Play, Use the Command /WORDLE!\nTo Guess, Reply to this Message with a Word")
    return embed


def updateEmbed(embed: hikari.Embed, guess: str) -> hikari.Embed:
    puzzle_id = int(embed.title.split()[2].strip(")"))
    answer = popularWords[puzzle_id]
    coloredWord = generateColoredWord(guess, answer)
    emptySlot = "\N{WHITE LARGE SQUARE}" * 5

    embed.description = embed.description.replace(emptySlot, coloredWord, 1)

    numEmptySlots = embed.description.count(emptySlot)
    if guess == answer:
        if numEmptySlots == 0:
            embed.description += "\n\nPhew!"
        if numEmptySlots == 1:
            embed.description += "\n\nGreat!"
        if numEmptySlots == 2:
            embed.description += "\n\nSplendid!"
        if numEmptySlots == 3:
            embed.description += "\n\nImpressive!"
        if numEmptySlots == 4:
            embed.description += "\n\nMagnificent!"
        if numEmptySlots == 5:
            embed.description += "\n\nGenius!"
        embed.color = SUCCESS_COLOR
    elif numEmptySlots == 0:
        embed.description += f"\n\nThe Answer was {answer.upper()}!"
        embed.color = FAILED_COLOR
    return embed


def isValidWord(word: str) -> bool:
    return word in allWords


def isGameOver(embed: hikari.Embed) -> bool:
    return "\n\n" in embed.description


async def processGuess(message: hikari.Message) -> bool:
    ref = message.referenced_message
    if ref == None:
        return

    if ref.author.id != BOT_UID:
        return

    if not ref.embeds:
        return

    embed = ref.embeds[0]
    guess = message.content.lower()
    guess = re.sub(r"<@!?\d+>", "", guess).strip()

    if (embed.author.name != message.author.username or embed.author.icon != message.author.display_avatar_url):
        await message.respond(embed=hikari.Embed(title="Start a new Game with /WORDLE!", color=FAILED_COLOR))
        await message.delete()
        return

    if isGameOver(embed):
        await message.respond(embed=hikari.Embed(title="This Game Ended, Start a new Game with /WORDLE", color=FAILED_COLOR))
        await message.delete()
        return

    if len(guess.split()) > 1:
        await message.respond(embed=hikari.Embed(title="Please Respond with One 5-Letter Word", color=FAILED_COLOR))
        await message.delete()
        return

    if not isValidWord(guess):
        await message.respond(embed=hikari.Embed(title=('"' + guess.upper() + '" is not a Valid Word'), color=FAILED_COLOR))
        await message.delete()
        return

    embed = updateEmbed(embed, guess)
    await ref.delete()
    await message.respond(embed)
    await message.delete()
    return