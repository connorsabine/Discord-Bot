import lightbulb
import hikari
import lavaplay
import miru
import asyncio
from constants import FAILED_COLOR, NORMAL_COLOR, BOT_UID

# INIT
plugin = lightbulb.Plugin("music")

# node CONNECT
# lavalink = lavaplay.Lavalink()
# node = lavalink.create_node(
#     # host="node.nicksabine.com",
#     # port=443,
#     # password="root",
#     # ssl=True,
#     # user_id=0
# )

lavalink = lavaplay.Lavalink()
node = lavalink.create_node(
    host="narco.buses.rocks",
    port=2269,
    password="glasshost1984",
    ssl=False,
    user_id=0
)

# LISTENERS
@plugin.listener(hikari.StartedEvent)
async def started_event(event):
    # miru.install(plugin.app)
    node.user_id = plugin.app.get_me().id
    node.connect()
    # node.set_event_loop(asyncio.get_event_loop())

@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent):
    player = node.create_player(event.guild_id)
    # player = node.get_player(event.guild_id)
    await player.raw_voice_state_update(event.state.user_id, event.state.session_id, event.state.channel_id)

@plugin.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent):
    # player = node.get_player(event.guild_id)
    player = node.create_player(event.guild_id)
    await player.raw_voice_server_update(event.raw_endpoint, event.token)


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

class SelectMenu(miru.View):
    global result, GID

    @miru.button(emoji="1️⃣")
    async def play1Button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        player = node.get_player(GID)
        await player.play(GID, result[0])

    @miru.button(emoji="2️⃣")
    async def play2Button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await node.play(GID, result[1])

    @miru.button(emoji="3️⃣")
    async def play3Button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await node.play(GID, result[2])

    @miru.button(emoji="4️⃣")
    async def play4Button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await node.play(GID, result[3])

    @miru.button(emoji="❌", style=hikari.ButtonStyle.DANGER)
    async def stopButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.stop()
        embed = hikari.Embed(title = "Menu Closed", color = FAILED_COLOR)
        await ctx.edit_response(embed=embed, components=None) 


class ControlsMenu(miru.View):
    paused = False

    async def updateEmbed(self, ctx):
        queue = await node.queue(ctx.guild_id)
        count = 1
        title = "Queue: "
        description = ""
        for song in queue:
            description += str(count) + ":  " + str(song) + "\n\n"
            count += 1
        if self.paused == True:
            title = "Queue (Paused): "

        await ctx.edit_response(
            embed=hikari.Embed(title=title, description=description, color = NORMAL_COLOR)
        )


    @miru.button(emoji="⏭")
    async def skipButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await node.skip(ctx.guild_id)
        await self.updateEmbed(ctx)

    @miru.button(emoji="🔀")
    async def shuffleButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await node.shuffle(ctx.guild_id)
        await self.updateEmbed(ctx)

    @miru.button(emoji="⏯")
    async def pauseButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        if self.paused == True:
            await node.pause(ctx.guild_id, False)
            self.paused = False
        else:
            await node.pause(ctx.guild_id, True)
            self.paused = True

        await self.updateEmbed(ctx)

    @miru.button(emoji="❌", style=hikari.ButtonStyle.DANGER)
    async def stopButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await node.stop(ctx.guild_id)
        await plugin.app.update_voice_state(ctx.guild_id, None)
        embed = hikari.Embed(title="Menu Closed", color = FAILED_COLOR)
        await ctx.edit_response(embed=embed, components=None)


# MUSIC COMMAND
@plugin.command
@lightbulb.command("menu", "Opens Music Commands Menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def menu(ctx: lightbulb.Context) -> None:
    try:
        queue = await node.queue(ctx.guild_id)
        count = 1
        description = ""
        for song in queue:
            description += str(count) + ":  " + str(song) + "\n\n"
            count += 1
        controlsMenu = ControlsMenu()
        message = await ctx.respond(embed=hikari.Embed(title="Queue: ", description=description, color=NORMAL_COLOR), components=controlsMenu)
        await controlsMenu.wait(120)
        embed = hikari.Embed(title = "Menu Timed Out", color = FAILED_COLOR)
        await message.edit_last_response(embed=embed, components=None)


    except:
        await ctx.respond(embed=hikari.Embed(title="Error", description="No Music in Queue, Add Music to Queue Before Attempting to Access Menu", color = FAILED_COLOR))


# MUSIC COMMAND GROUP
@plugin.command
@lightbulb.command("music", "Music Commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def music(ctx: lightbulb.Context) -> None:
    await ctx.respond("Invoked Music")


# MUSIC COMMANDS
@music.child
@lightbulb.option("query", "The Name of The Song", required=True)
@lightbulb.command("queue", "Add Song to Queue")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def queue(ctx: lightbulb.Context) -> None:
    global GID, result
    GID = ctx.guild_id
    state = plugin.app.cache.get_voice_state(ctx.guild_id, ctx.author)
    if state == None:
        embed = hikari.Embed(title = "Error", description = "You are not in a Voice Channel", color = FAILED_COLOR)
        return await ctx.edit_response(embed=embed, components=None)

    await plugin.app.update_voice_state(ctx.guild_id, state.channel_id, self_deaf=False)
    result = await node.auto_search_tracks(ctx.options.query)
    selectMenu = SelectMenu()
    try:
        selectDescription = ("1️⃣:  "+ str(result[0])+ "\n\n 2️⃣:  "+ str(result[1])+ "\n\n 3️⃣:  "+ str(result[2])+ "\n\n 4️⃣:  "+ str(result[3]))
    except:
        embed = hikari.Embed(title="Error", description="- No Songs Found\n - Use a Broader Search", color=FAILED_COLOR)
        return await ctx.respond(embed=embed)

    message = await ctx.respond(hikari.Embed(title=(ctx.options.query.upper() + " Search Results:") , description=selectDescription, color = NORMAL_COLOR), components=selectMenu)

    await selectMenu.start(message)
    await selectMenu.wait_for_input()
    selectMenu.stop()
    controlsMenu = ControlsMenu()
    await controlsMenu.start(message)

    player = node.get_player(ctx.guild_id)
    print(player)
    queue = await player.queue(ctx.guild_id)
    count = 1
    controlsDescription = ""
    for song in queue:
        controlsDescription += str(count) + ":  " + str(song) + "\n\n"
        count += 1

    await ctx.edit_last_response(embed=hikari.Embed(title="Queue: ", description=controlsDescription, color = NORMAL_COLOR), components=controlsMenu)
    await controlsMenu.wait()
    embed = hikari.Embed(title="Menu Timed Out", color = FAILED_COLOR)
    await ctx.edit_last_response(embed=embed, components=None)



@music.child
@lightbulb.command("skip", "Skip Current Song")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def skip(ctx: lightbulb.Context) -> None:
    await node.skip(ctx.guild_id)
    embed = hikari.Embed(title="Music Skipped", color = NORMAL_COLOR)
    await ctx.respond(embed=embed)

@music.child
@lightbulb.command("stop", "Stops Music and Kicks Bot From Channel")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def stop(ctx: lightbulb.Context) -> None:
    await node.stop(ctx.guild_id)
    await plugin.app.update_voice_state(ctx.guild_id, None)
    embed = hikari.Embed(title="Music Stopped", color = FAILED_COLOR)
    await ctx.respond(embed=embed)

@music.child
@lightbulb.command("shuffle", "Shuffles the Queue")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def shuffle(ctx: lightbulb.Context) -> None:
    await node.shuffle(ctx.guild_id)
    embed = hikari.Embed(title="Music Shuffled", color = NORMAL_COLOR)
    await ctx.respond(embed = embed)

@music.child
@lightbulb.option("track", "The Position in Queue")
@lightbulb.command("remove", "Remove a Track from Queue")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.Context) -> None:
    await node.remove(ctx.guild_id, int(ctx.options.track)-1)
    embed = hikari.Embed(title="Track Removed", color = FAILED_COLOR)
    await ctx.respond(embed = embed)

# @music.child
# @lightbulb.options("playlist" "Name of Playlist")
# @lightbulb.command("save", "Saves Song to Playlist")
# @lightbulb.implements(lightbulb.SlashSubCommand)
# async def save(ctx: lightbulb.Context) -> None:
    
#     embed = hikari.Embed(title="Music Shuffled", color = NORMAL_COLOR)
#     await ctx.respond(embed = embed)