import lightbulb
import hikari

# INIT
plugin = lightbulb.Plugin("adduser")


# REQUIRED FUNCTIONS
def load(bot):
  bot.add_plugin(plugin)

def unload(bot):
  bot.remove_plugin(plugin)


# find a way to add all curent users in every server to database

# on user join guild, add them to the database if not already there
  # would their discord id be the primary key?
  
