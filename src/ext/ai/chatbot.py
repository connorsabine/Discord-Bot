import hikari
import lightbulb
import os
import openai
from replit import db
from constants import BOT_UID

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
    db["GUILD_DATA"][str(ctx.guild_id)]["CONTEXT_HISTORY"] = []
    await ctx.respond("Chatbot Reset!")

@chatbot.child
@lightbulb.option("prompt", "The Question")
@lightbulb.command("ask", "Asks a Question to the Chatbot")
@lightbulb.implements(lightbulb.SlashCommand)
async def ask(ctx: lightbulb.Context) -> None:
    response = openai.Completion.create(engine="text-davinci-003", prompt=ctx.options.prompt, max_tokens=200, temperature=0)
    await ctx.respond(response.choices[0].text.strip())

@chatbot.child
@lightbulb.option("prompt", "The Prompt")
@lightbulb.command("image", "Creates a Drawing of your Prompt")
@lightbulb.implements(lightbulb.SlashCommand)
async def image(ctx: lightbulb.Context) -> None:
    await ctx.respond("Thinking...")
    response = openai.Image.create(prompt=ctx.options.prompt, n=1, size="256x256")
    await ctx.edit_last_response(response['data'][0]['url'])

  
@plugin.listener(hikari.MessageCreateEvent)
async def message_event(event):
    if event.author_id == BOT_UID:
        return
      
    if event.content != None and f"<@{BOT_UID}> " in event.content:
        content = event.content.replace(f"<@{BOT_UID}> ", "")
        thread = plugin.app.cache.get_thread(event.channel_id)
        if thread != None:
            try:
                db["CHANNEL_DATA"][str(event.channel_id)].append({"role":"user", "content":content})
            except:
                db["CHANNEL_DATA"][str(event.channel_id)] = [{"role":"user", "content":content}]

            db["CHANNEL_DATA"][str(event.channel_id)] = [{"role":"user", "content":content}]

            context = []
            for dict in db["CHANNEL_DATA"].value[str(event.channel_id)].value:
                newDict = {}
                for key in dict:
                    newDict[key] = dict[key]
                context.append(newDict)
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=context, max_tokens=5000)
                await plugin.app.rest.create_message(event.channel_id, response.choices[0].message.content.strip())
                db["CHANNEL_DATA"][str(event.channel_id)].append({"role":"assistant", "content":response.choices[0].message.content.strip()})
            except:
                await plugin.app.rest.create_message(event.channel_id, "To Avoid Large API Fees, Chatter Bot will Restart this Thread with no Historical Context. (Err: MAX-TOKEN-REACHED)")
                db["CHANNEL_DATA"][str(event.channel_id)] = []

      
        else:
            try:
                db["GUILD_DATA"][str(event.guild_id)]["CONTEXT_HISTORY"].append({"role":"user", "content":content})
            except:
                db["GUILD_DATA"][str(event.guild_id)]["CONTEXT_HISTORY"] = [{"role":"user", "content":content}]
  
            context = []
            for dict in db["GUILD_DATA"].value[str(event.guild_id)].value["CONTEXT_HISTORY"].value:
                newDict = {}
                for key in dict:
                    newDict[key] = dict[key]
                context.append(newDict)
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=context, max_tokens=5000)
                await plugin.app.rest.create_message(event.channel_id, response.choices[0].message.content.strip())
                db["GUILD_DATA"][str(event.guild_id)]["CONTEXT_HISTORY"].append({"role":"assistant", "content":response.choices[0].message.content.strip()})
            except:
                await plugin.app.rest.create_message(event.channel_id, "To Avoid Large API Fees, Chatter Bot will Restart with no Historical Context. (Err: MAX-TOKEN-REACHED)")
                db["GUILD_DATA"][str(event.guild_id)]["CONTEXT_HISTORY"] = []
                  