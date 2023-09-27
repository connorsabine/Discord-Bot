import hikari
import lightbulb
from constants import NORMAL_COLOR

# INIT
plugin = lightbulb.Plugin("help")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


# COMMANDS
@plugin.command
@lightbulb.command("help", "Displays Help Menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Help Menu", description="All Susiety Supporter Commands and Descriptions", color = NORMAL_COLOR
    )

    embed.add_field(name="Ping", value="Responds with Pong!")

    embed.add_field(name="Texting AI", value="In a Discord Thread, You can have Conversations with Historical Context. Mention Chatter Bot with a Question in a Thread to Test it Out!")

    embed.add_field(name="Fortune", value="Replies with a Random Fortune")

    embed.add_field(name="Quote", value="Displays a Random Quote from Server Quotes List")

    # embed.add_field(name="AddQuote", value="Adds Quote to Server Quotes List")

    embed.add_field(name="Color", value="Changes Display Name to Given Color")

    embed.add_field(name="RollDice", value="Rolls a Dice with the Number of Sides Given")

    embed.add_field(name="Coinflip", value="Flips a Coin")

    embed.add_field(name="Menu", value="Brings up Music Menu")

    embed.add_field(name="Queue", value="Queues Music")

    await ctx.respond(embed=embed)
