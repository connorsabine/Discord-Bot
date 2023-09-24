import lightbulb
import hikari
from replit import db

# INIT
plugin = lightbulb.Plugin("appenduser")


# REQUIRED FUNCTIONS
def load(bot):
  bot.add_plugin(plugin)


def unload(bot):
  bot.remove_plugin(plugin)

# reset all 
# for key in db["USER_DATA"].keys():
#   db["USER_DATA"][key] = {"SENTIMENT": 0,"RPG": None}

@plugin.listener(hikari.MessageCreateEvent)
async def message(event: hikari.MessageCreateEvent):
  try:
    db["USER_DATA"][str(event.author_id)]
  except:
    db["USER_DATA"][str(event.author_id)] =  {
        "SENTIMENT": 0,
        "RPG": None
      }
