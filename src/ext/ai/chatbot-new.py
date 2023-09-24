import hikari
import lightbulb
import os
import openai
from constants import BOT_UID, OPENAI_TOKEN_LIMIT

# INIT
plugin = lightbulb.Plugin("chatbot")
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.command
@lightbulb.command("chatbot", "Chatbot Base Command")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def chatbot(ctx: lightbulb.Context) -> None:
    await ctx.respond("Chatbot Invoked")

@chatbot.child
@lightbulb.command("reset", "Resets the Chatbot Outside of Threads")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def reset(ctx: lightbulb.Context) -> None:
    # reset chatbot db
    await ctx.respond("Chatbot Reset!")

@chatbot.child
@lightbulb.option("prompt", "The Question")
@lightbulb.command("ask", "Asks a Question to the Chatbot")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ask(ctx: lightbulb.Context) -> None:
    response = openai.Completion.create(engine="text-davinci-003", prompt=ctx.options.prompt, max_tokens=OPENAI_TOKEN_LIMIT, temperature=0)
    text = response.choices[0].text.strip()
    if len(text) > 1950:
        fileName = "src/ext/ai/txtdumps/" + ctx.options.prompt + ".txt"
        f = open(fileName, "w")
        f.write(text)
        f.close()
        await ctx.respond(hikari.File(fileName))
        os.remove(fileName)
    else:
        await ctx.respond(text)

  
@plugin.listener(hikari.MessageCreateEvent)
async def message_event(event):
    if event.author_id == BOT_UID:
        return

    # create message 

    if event.content != None and f"<@{BOT_UID}> " in event.content:
        content = event.content.replace(f"<@{BOT_UID}> ", "")
        
                  