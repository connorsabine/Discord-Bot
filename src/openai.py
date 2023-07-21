import hikari
import lightbulb
import os
import openai

# INIT
plugin = lightbulb.Plugin("openai")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

@plugin.command
@lightbulb.option("prompt", "The Prompt to ask OpenAI")
@lightbulb.command("openai", "Gets a Response from OpenAI")
@lightbulb.implements(lightbulb.SlashCommand)
async def openai(ctx: lightbulb.Context) -> None:
    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=ctx.options.prompt, max_tokens=50)
    await ctx.respond(response.choices[0].text.strip())