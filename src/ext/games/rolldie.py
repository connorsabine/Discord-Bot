import lightbulb
import hikari
import random
from constants import NORMAL_COLOR

# INIT
plugin = lightbulb.Plugin("rolldie")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# COMMANDS
@plugin.command
@lightbulb.command("rolldice", "Flips a Coin")
@lightbulb.implements(lightbulb.SlashCommand)
async def rolldice(ctx: lightbulb.Context) -> None:
    roll = str(random.randrange(0, 7))
    embed = hikari.Embed(title="You rolled a " + roll + "!", color = NORMAL_COLOR)
    await ctx.respond(embed = embed)