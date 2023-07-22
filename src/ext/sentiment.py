from afinn import Afinn
import lightbulb
import hikari
from constants import SUCCESS_COLOR, FAILED_COLOR, NORMAL_COLOR
from replit import db

# INIT
plugin = lightbulb.Plugin("sentiment")
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
            try:
                pastScore = db["USER_DATA"][str(event.author.id)]["SENTIMENT"]
                db["USER_DATA"][str(event.author.id)]["SENTIMENT"] = pastScore + score
            except:
                db["USER_DATA"][str(event.user.id)]["SENTIMENT"] = score
    except:
        pass

@plugin.command
@lightbulb.command("sentiment", "Get Your Sentiment Score")
@lightbulb.implements(lightbulb.SlashCommand)
async def sentiment(ctx: lightbulb.Context) -> None: 
    try:
        score = db["USER_DATA"][str(ctx.user.id)]["SENTIMENT"]
          
        if score > 1:
            embed = hikari.Embed(title=ctx.user.username.upper() + " Sentiment:", description=str(round(score, 2)), color=SUCCESS_COLOR)
        elif score < -1:
            embed = hikari.Embed(title=ctx.user.username.upper() + " Sentiment:", description= str(round(score, 2)), color=FAILED_COLOR)
        else:
            embed = hikari.Embed(title=ctx.user.username.upper() + " Sentiment:", description=str(round(score, 2)), color=NORMAL_COLOR)
    
    except:
        embed = hikari.Embed(title=(ctx.user.username.upper() + " Sentiment not Set"), color=FAILED_COLOR)
      
    await ctx.respond(embed=embed)