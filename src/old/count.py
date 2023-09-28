import lightbulb
import hikari
import sympy
import sqlite3
from constants import FAILED_COLOR, SUCCESS_COLOR, NORMAL_COLOR

# INIT
plugin = lightbulb.Plugin("count")
database = sqlite3.connect("bot.db")
cursor = database.cursor()

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


# LISTENERS
@plugin.listener(hikari.MessageCreateEvent)
async def message_event(event):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    try:
        data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
        countcid = int(data[6])
        count = int(data[7])
        lastCounter = int(data[8])
        highscore = int(data[9])
        highscoreHolder = data[10]

    except:
        return

    if event.channel_id != countcid:
        return

    try:
        msg = event.content
        if any(letter in msg for letter in letters):
            return
        if event.author_id == lastCounter and "@" not in event.content:
            await plugin.app.rest.delete_message(channel=event.channel_id, message=event.message_id)
            return None
            
        msgc = sympy.sympify(msg)

        if msgc == count + 1:
            count += 1
            lastCounter = event.author_id
            cursor.execute("UPDATE GUILDDATA SET currentcount = {}, currentcounter = {} WHERE guildid = {}".format(count, event.author_id, event.guild_id))
            database.commit()

            if count > highscore:
                cursor.execute("UPDATE GUILDDATA SET highcount = {}, highcountholder = '{}' WHERE guildid = {}".format(count, event.author, event.guild_id))
                database.commit()
                highscore = count

            await event.message.add_reaction("✅")
        else:
            cursor.execute("UPDATE GUILDDATA SET currentcount = 0, currentcounter = 0 WHERE guildid = {}".format(event.guild_id))
            database.commit()

            await event.message.add_reaction("❌")
            embed = hikari.Embed(
                title="Count Streak Ended", description="Here's your stats...", color = FAILED_COLOR
            )

            embed.add_field(
                name="High Score:", value=str(highscore) + " by " + highscoreHolder
            )

            embed.add_field(name="Score:", value=count)
            embed.add_field(name="Streak Ender:", value=event.author)
            await event.message.respond(embed=embed)

            count = 0

    except Exception as e:
        print(e)
        return