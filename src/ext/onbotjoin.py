import lightbulb
import hikari
import sqlite3
from constants import QUOTEDATA_TABLE
#import traceback  # For Detailed Error printing
#import sys        # For Detailed Error printing


# INIT
plugin = lightbulb.Plugin("onbotjoin")
database = sqlite3.connect("bot.db")
cursor = database.cursor()


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.listener(hikari.GuildJoinEvent)
async def botJoin(event: hikari.GuildJoinEvent):
    cursor.execute(QUOTEDATA_TABLE.format(guildid = event.guild_id))
    
    # Try to insert guild_id.  
    # If it already exists, the primary key violation will cause exception.
    try:
        #cursor.execute("INSERT INTO GUILDDATA VALUES ({}, 0, 0, 0, 0, 0, 0, 0, 'Not Set')".format(event.guild_id))
        cursor.execute("INSERT INTO GUILDDATA (guildid) VALUES({})".format(event.guild_id))
        database.commit()
    except sqlite3.Error as error:
        return
        # Print Detailed Error
        #print("Failed to insert data into sqlite table")
        #print("Exception class is: ", error.__class__)
        #print("Exception is", error.args)
        #print('Printing detailed SQLite exception traceback: ')
        #exc_type, exc_value, exc_tb = sys.exc_info()
        #print(traceback.format_exception(exc_type, exc_value, exc_tb))
