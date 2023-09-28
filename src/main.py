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


# bot.load_extensions("db.appenduser")
# bot.load_extensions("db.appendguild")

# bot.load_extensions("ext.ai.imagine")
# bot.load_extensions("ext.ai.chatbot-new")

# bot.load_extensions("ext.extras.help")
# # bot.load_extensions("ext.extras.music")
# bot.load_extensions("ext.extras.color")
# bot.load_extensions("ext.extras.giphy")

# # bot.load_extensions("ext.members.join")
# # bot.load_extensions("ext.members.leave")

# # bot.load_extensions("ext.admin.logging")
# # bot.load_extensions("ext.admin.moderation")
# # bot.load_extensions("ext.admin.configure")

# # bot.load_extensions("ext.quotes.quotes")
# bot.load_extensions("ext.quotes.zenquotes")

# # bot.load_extensions("ext.games.rpg")

# Ping Message
@bot.command
@lightbulb.command("ping", "Sends Pong!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")
 

# RUN BOT
activity = hikari.Activity(name="Under Development", type=hikari.ActivityType.PLAYING) 
bot.run(status=hikari.Status.ONLINE, activity=activity)
