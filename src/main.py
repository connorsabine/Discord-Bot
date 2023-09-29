# IMPORT
import hikari
import lightbulb
from secret import get_secret


# EXTENSIONS
bot = lightbulb.BotApp(token=get_secret("BOT_TOKEN"), intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MEMBERS)
bot.load_extensions("ext.ai.chatbot")
bot.load_extensions("ext.games.wordle")
bot.load_extensions("ext.games.tictactoe")
bot.load_extensions("ext.games.coinflip")

# bot.load_extensions("db.adduser")
# bot.load_extensions("ext.ai.images")
# bot.load_extensions("ext.extras.help")
# bot.load_extensions("ext.extras.music")
# bot.load_extensions("ext.extras.color")
# bot.load_extensions("ext.games.rpg")

# Ping Message
@bot.command
@lightbulb.command("ping", "Sends Pong!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")
 

# RUN BOT
activity = hikari.Activity(name="Under Development", type=hikari.ActivityType.PLAYING) 
bot.run(status=hikari.Status.ONLINE, activity=activity)
