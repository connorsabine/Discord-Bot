import lightbulb
import hikari
import random
import sqlite3
from constants import QUOTE_COLOR

# INIT
plugin = lightbulb.Plugin("fortunes")
database = sqlite3.connect("bot.db")
cursor = database.cursor()

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.command("fortune", "Gives a Random Fortune")
@lightbulb.implements(lightbulb.SlashCommand)
async def fortune(ctx: lightbulb.Context) -> None:
    rows = cursor.execute("SELECT COUNT(*) FROM FORTUNES").fetchone()
    data = cursor.execute("SELECT * FROM FORTUNES WHERE rowid={}".format(random.randint(0, rows[0]))).fetchone()
    await ctx.respond(embed=hikari.Embed(title = data[0], color = QUOTE_COLOR))
