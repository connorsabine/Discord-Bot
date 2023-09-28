import lightbulb
import hikari
import random
from constants import NORMAL_COLOR

# INIT
plugin = lightbulb.Plugin("coinflip")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# COMMANDS
@plugin.command
@lightbulb.command("coinflip", "Flip a Coin!")
@lightbulb.implements(lightbulb.SlashCommand)
async def coinflip(ctx: lightbulb.Context) -> None:
    if random.randrange(0, 2) == 1: 
        embed = hikari.Embed(title="The Coin Landed on Heads!", color = NORMAL_COLOR)
        embed.set_image('graphics/coinflip/heads.png')
        await ctx.respond(embed = embed)
    else:
        embed = hikari.Embed(title="The Coin Landed on Tails!", color = NORMAL_COLOR)
        embed.set_image('graphics/coinflip/tails.png')
        await ctx.respond(embed = embed)