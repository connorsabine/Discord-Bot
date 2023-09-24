import hikari
import lightbulb
import os
import openai
from replit import db
from constants import BOT_UID, OPENAI_TOKEN_LIMIT

# INIT
plugin = lightbulb.Plugin("imagine")
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# db management
@plugin.command
@lightbulb.option("prompt", "The Prompt")
@lightbulb.command("imagine", "Creates a Drawing of your Prompt")
@lightbulb.implements(lightbulb.SlashCommand)
async def imagine(ctx: lightbulb.Context) -> None:
    await ctx.respond("Thinking...")
    response = openai.Image.create(prompt=ctx.options.prompt, n=1, size="256x256")
    await ctx.edit_last_response(ctx.options.prompt, attachment=response['data'][0]['url'])

