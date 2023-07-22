from constants import QUOTE_COLOR, FAILED_COLOR
import lightbulb
import hikari
import random
import sqlite3


# INIT
plugin = lightbulb.Plugin("quotes")
database = sqlite3.connect("bot.db")
cursor = database.cursor()



# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)



# Quote Command Group
@plugin.command
@lightbulb.command("quote", "Quote Subgroup")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def quote(ctx: lightbulb.Context) -> None:
    await ctx.respond("Quote Invoked")


# Subcommands
@quote.child
@lightbulb.command("rand", "Sends a Random Quote from Someone in this Server")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def rand(ctx: lightbulb.Context) -> None:
    rows = cursor.execute("SELECT COUNT(*) FROM QUOTEDATA{}".format(ctx.guild_id)).fetchone()
    data = cursor.execute("SELECT * FROM QUOTEDATA{} WHERE rowid={}".format(ctx.guild_id, random.randint(0, rows[0]))).fetchone()
    if data != None:
        embed = hikari.Embed(title=data[1], description=" - " + data[0], color = QUOTE_COLOR)
        await ctx.respond(embed=embed)
    else:
        embed = hikari.Embed(title="Error", description="No Quotes", color = FAILED_COLOR)
        await ctx.respond(embed=embed)

@quote.child
@lightbulb.option("text", "The Quote You Want to Add", type=str)
@lightbulb.option("author", "The Author of the Quote", type=str)
@lightbulb.command("add", "Add To The Server Quotes")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx):
    if len(ctx.options.quote) > 170 or len(ctx.options.author) > 30:
        await ctx.respond("Quote Must Be Under 170 Characters and Author Name Must Be Under 30 Characters")
        return
    author = ctx.options.author.strip("'")
    text = ctx.options.quote.strip("'")
    cursor.execute("INSERT INTO QUOTEDATA{} VALUES ('{}', '{}')".format(ctx.guild_id, author, text))
    database.commit()
    await ctx.respond(embed=hikari.Embed(title = text, description=" - " + author, color = QUOTE_COLOR))