# IMPORT
import hikari
import lightbulb
import os


# EXTENSIONS
bot = lightbulb.BotApp(token=os.getenv("BOT_TOKEN"), intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MEMBERS)

bot.load_extensions("ext.ai.text")
bot.load_extensions("ext.ai.image")

bot.load_extensions("ext.help")
# bot.load_extensions("ext.music")
bot.load_extensions("ext.color")
# bot.load_extensions("ext.onbotjoin")
bot.load_extensions("ext.sentiment")
bot.load_extensions("ext.giphy")

# bot.load_extensions("ext.members.join")
# bot.load_extensions("ext.members.leave")

# bot.load_extensions("ext.admin.logging")
# bot.load_extensions("ext.admin.moderation")
# bot.load_extensions("ext.admin.configure")

# bot.load_extensions("ext.quotes.quotes")
# bot.load_extensions("ext.quotes.fortunes")
bot.load_extensions("ext.quotes.zenquotes")

bot.load_extensions("ext.games.rolldie")
bot.load_extensions("ext.games.coinflip")
# bot.load_extensions("ext.games.count")
bot.load_extensions("ext.games.tictactoevs")
bot.load_extensions("ext.games.tictactoeai")
bot.load_extensions("ext.games.rockpaperscissors")
bot.load_extensions("ext.games.anagrams")
# bot.load_extensions("ext.games.rpg")
bot.load_extensions("ext.games.wordle")

# Ping Message
@bot.command
@lightbulb.command("ping", "Sends Pong!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")
 

# RUN BOT
activity = hikari.Activity(name="Under Development", type=hikari.ActivityType.PLAYING) 
bot.run(status=hikari.Status.ONLINE, activity=activity)
