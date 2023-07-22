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


@plugin.listener(hikari.MessageCreateEvent)
async def message(event: hikari.MessageCreateEvent):
  db["USER_DATA"] = {
    str(event.author_id): {
      "SENTIMENT": 0
    }
  }
