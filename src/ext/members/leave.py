import lightbulb
import hikari
import sqlite3

# INIT
plugin = lightbulb.Plugin("leave")
database = sqlite3.connect("bot.db")
cursor = database.cursor()

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# EVENTS
@plugin.listener(hikari.MemberDeleteEvent)
async def memberLeave(event: hikari.MemberDeleteEvent):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[2] in channels:
        message = data[4].replace("<USER>", event.user.mention)
        await plugin.app.rest.create_message(data[2], message)