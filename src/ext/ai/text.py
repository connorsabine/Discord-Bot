import hikari
import lightbulb
import os
import openai
from replit import db
from constants import BOT_UID

# INIT
plugin = lightbulb.Plugin("text")
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.command("toggleai", "Toggles if AI Text Responses are On")
@lightbulb.implements(lightbulb.SlashCommand)
async def toggleai(ctx: lightbulb.Context) -> None:
    try:
      if db["GUILD_DATA"][str(ctx.guild_id)]["SETTINGS"]["AI_ALWAYS_ON"] == True:
          db["GUILD_DATA"][str(ctx.guild_id)]["SETTINGS"]["AI_ALWAYS_ON"] = False
          await ctx.respond("AI Responses Toggled to Off.")
      else:
          db["GUILD_DATA"][str(ctx.guild_id)]["SETTINGS"]["AI_ALWAYS_ON"] = True
          await ctx.respond("AI Responses Toggled to On.")
    except:
        db["GUILD_DATA"][str(ctx.guild_id)]["SETTINGS"]["AI_ALWAYS_ON"] = True
        await ctx.respond("AI Responses Toggled to On.")

@plugin.listener(hikari.MessageCreateEvent)
async def message_event(event):
    if event.author_id == BOT_UID:
        return

    if event.content != None:
        if db["GUILD_DATA"][str(event.guild_id)]["SETTINGS"]["AI_ALWAYS_ON"] == True:
          response = openai.Completion.create(engine="text-davinci-003", prompt=event.content, max_tokens=100, temperature=0)
          await plugin.app.rest.create_message(event.channel_id, response.choices[0].text.strip())