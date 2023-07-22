from afinn import Afinn
import lightbulb
import hikari
import sqlite3
from constants import SUCCESS_COLOR, FAILED_COLOR, NORMAL_COLOR

# INIT
plugin = lightbulb.Plugin("join")
database = sqlite3.connect("bot.db")
cursor = database.cursor()
afinn = Afinn(language="en", emoticons=True)

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
 
# EVENTS
@plugin.listener(hikari.events.message_events.MessageCreateEvent)
async def message(event):
    try:
        score = afinn.score(event.content)/10
        if score != 0:
            data = cursor.execute("SELECT * FROM USERDATA WHERE userid={}".format(event.author_id)).fetchone()
            if data != None:
                cursor.execute("UPDATE USERDATA SET sentiment = sentiment + {} WHERE userid = {} ".format(score, event.author_id))
            else:
                cursor.execute("INSERT INTO USERDATA (userid, sentiment, currentrole) VALUES({}, {}, 0)".format(event.author_id, score))
            database.commit()
        
        roles = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
        sentData = cursor.execute("SELECT * FROM USERDATA WHERE userid={}".format(event.author_id)).fetchone()
        try:
            await plugin.app.rest.remove_role_from_member(user=event.author, guild=event.guild_id, role=sentData[2])
        except:
            pass

        if sentData[1] > 1:
            await plugin.app.rest.add_role_to_member(user=event.author, guild=event.guild_id, role=roles[11])
            cursor.execute("UPDATE USERDATA SET currentrole = {} WHERE userid = {} ".format(roles[11], event.author_id))
        elif sentData[1] < -1:
            await plugin.app.rest.add_role_to_member(user=event.author, guild=event.guild_id, role=roles[13])
            cursor.execute("UPDATE USERDATA SET currentrole = {} WHERE userid = {} ".format(roles[13], event.author_id))
        else:
            await plugin.app.rest.add_role_to_member(user=event.author, guild=event.guild_id, role=roles[12])
            cursor.execute("UPDATE USERDATA SET currentrole = {} WHERE userid = {} ".format(roles[12], event.author_id))
        
        database.commit()

    except:
        pass

@plugin.command
@lightbulb.option("user", "The User of the Sentiment You Want to Get (Leave Blank to See Your Own)", type=hikari.Member)
@lightbulb.command("sentiment", "Get Your Sentiment Score")
@lightbulb.implements(lightbulb.SlashCommand)
async def sentiment(ctx: lightbulb.Context) -> None:
    if ctx.options.user.id != None:
        user = ctx.options.user
    else:
        user = ctx.author
    
    try:
        data = cursor.execute("SELECT * FROM USERDATA WHERE userid={}".format(user.id)).fetchone()

        if data[1] > 1:
            embed = hikari.Embed(title=user.username + " Sentiment:", description=str(round(data[1], 2)), color=SUCCESS_COLOR)
        elif data[1] < -1:
            embed = hikari.Embed(title=user.username + " Sentiment:", description= str(data[1]), color=FAILED_COLOR)
        else:
            embed = hikari.Embed(title=user.username + " Sentiment:", description=str(round(data[1], 2)), color=NORMAL_COLOR)
    
    except:
        embed = hikari.Embed(title=(user.username + " Sentiment not Set"), color=FAILED_COLOR)

    await ctx.respond(embed=embed)