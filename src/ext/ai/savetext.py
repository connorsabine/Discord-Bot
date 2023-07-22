import hikari
import lightbulb
import os
import openai

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
@lightbulb.option("prompt", "The Prompt to ask OpenAI")
@lightbulb.command("ask", "Gets a Text Response from OpenAI")
@lightbulb.implements(lightbulb.SlashCommand)
async def text(ctx: lightbulb.Context) -> None:
    response = openai.Completion.create(engine="text-davinci-003", prompt=ctx.options.prompt, max_tokens=50, temperature=0)
    await ctx.respond(response.choices[0].text.strip())