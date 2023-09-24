import lightbulb
import hikari
from replit import db

# INIT
plugin = lightbulb.Plugin("appendguild")


# REQUIRED FUNCTIONS
def load(bot):
  bot.add_plugin(plugin)


def unload(bot):
  bot.remove_plugin(plugin)

# reset all
# for key in db["GUILD_DATA"].keys():
#   db["GUILD_DATA"][key] = {"CONTEXT_HISTORY": []}

@plugin.listener(hikari.GuildJoinEvent)
async def join(event: hikari.GuildJoinEvent):
  try:
      db["GUILD_DATA"][str(event.guild_id)]
  except:
      db["GUILD_DATA"][str(event.guild_id)] = {
          "CONTEXT_HISTORY": []
        }
