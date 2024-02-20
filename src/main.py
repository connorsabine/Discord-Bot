# IMPORT
import hikari
import lightbulb
import os


# EXTENSIONS
bot = lightbulb.BotApp(token=os.getenv("BOT_TOKEN"), intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MEMBERS)
bot.load_extensions("ext.ai.chatbot")
bot.load_extensions("ext.games.wordle")
bot.load_extensions("ext.games.tictactoe")
bot.load_extensions("ext.games.coinflip")
bot.load_extensions("ext.extras.music")


# Ping Message
@bot.command
@lightbulb.command("ping", "Sends Pong!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")
 

# RUN BOT
activity = hikari.Activity(name="Under Development", type=hikari.ActivityType.PLAYING) 
bot.run(status=hikari.Status.ONLINE, activity=activity)
