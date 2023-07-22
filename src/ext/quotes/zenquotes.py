from constants import QUOTE_COLOR
import lightbulb
import hikari
import requests
import json

# INIT
plugin = lightbulb.Plugin("zenquotes")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.command("zenquote", "Gives a Random Quote from ZenQuotes API")
@lightbulb.implements(lightbulb.SlashCommand)
async def zenquotes(ctx: lightbulb.Context) -> None:
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = data[0]['q']
    author = "- " + data[0]['a']
    await ctx.respond(embed=hikari.Embed(title = quote, description = author, color = QUOTE_COLOR))