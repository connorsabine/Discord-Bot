import lightbulb
import hikari
import random
from constants import FAILED_COLOR, SUCCESS_COLOR, NORMAL_COLOR
# INIT
plugin = lightbulb.Plugin("rockpaperscissors")


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


# COMMANDS
@plugin.command
@lightbulb.option("selection", "Pick Rock, Paper or Scissors", choices=["Rock", "Paper", "Scissors"])
@lightbulb.command("rps", "Play Rock Paper Scissors")
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context) -> None:
    choices = ["Rock", "Paper", "Scissors"]
    ai = choices[random.randint(0, 2)]
    pl = ctx.options.selection

    if ai == pl:
        winner = None
    elif ai == "Rock" and pl == "Paper":
        winner = "pl"
    elif ai == "Rock" and pl == "Scissors":
        winner = "ai"
    elif ai == "Scissors" and pl == "Paper":
        winner = "ai"
    elif ai == "Scissors" and pl == "Rock":
        winner = "pl"
    elif ai == "Paper" and pl == "Scissors":
        winner = "pl"
    elif ai == "Paper" and pl == "Rock":
        winner = "ai"

    if winner == None:
        embed = hikari.Embed(title=":rock::newspaper::scissors: - Tie!",description="Both :computer: and :person_standing:: " + ai, color=NORMAL_COLOR)
    elif winner == "ai":
        embed = hikari.Embed(title=":rock::newspaper::scissors: - :computer: Wins!",description=":computer:: " + ai + "\n :person_standing:: " + pl, color=FAILED_COLOR)
    elif winner == "pl":
        embed = hikari.Embed(title=":rock::newspaper::scissors: - :person_standing: Wins!",description=":computer: : " + ai + "\n :person_standing:: " + pl, color=SUCCESS_COLOR)
    
    await ctx.respond(embed=embed)


