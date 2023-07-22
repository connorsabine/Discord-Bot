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


@plugin.listener(hikari.GuildJoinEvent)
async def join(event: hikari.GuildJoinEvent):
  db["GUILD_DATA"] = {
    str(event.guild_id): {
      "SETTINGS": {
        "AI_ALWAYS_ON": False
      }
    }
  }
