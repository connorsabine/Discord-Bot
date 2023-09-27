import lightbulb
import hikari
import requests
import json

# INIT
plugin = lightbulb.Plugin("giphy")


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


# COMMANDS
@plugin.command
@lightbulb.command("giphy", "Giphy Command")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def giphy(ctx: lightbulb.Context) -> None:
    await ctx.respond("Giphy Invoked")

@giphy.child
@lightbulb.command("random", "Random Gif")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def random(ctx: lightbulb.Context) -> None:
    response = requests.get("https://api.giphy.com/v1/gifs/random?api_key=V8EcP2RhawlD7tONCNrefxxes4AYBUt0&tag=&rating=r")
    data = json.loads(response.text)
    embed = hikari.Embed(title="Random Giphy")
    embed.set_image(data["data"]['url'])
    await ctx.respond(embed)

@giphy.child
@lightbulb.option("query", "The Giphy Query")
@lightbulb.command("search", "Searched Gif")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def search(ctx: lightbulb.Context) -> None:
    response = requests.get("https://api.giphy.com/v1/gifs/search?api_key=V8EcP2RhawlD7tONCNrefxxes4AYBUt0&q=" + ctx.options.query + "&limit=1&offset=0&rating=r&lang=en")
    data = json.loads(response.text)
    embed = hikari.Embed(title=("Giphy Search"))
    embed.set_image(data["data"][0]['url'])
    await ctx.respond(embed)

