import lightbulb
import hikari
import sqlite3
from constants import SUCCESS_COLOR, FAILED_COLOR, NORMAL_COLOR


# INIT
plugin = lightbulb.Plugin("configure")
database = sqlite3.connect("bot.db")
cursor = database.cursor()


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)



@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(perm1=hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("configure", "Configure Channel Commands", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def configure(ctx: lightbulb.Context) -> None:
    await ctx.respond("Invoked Configure")


@configure.child
@lightbulb.option("channel", "If Not Supplied Channel, The Current Channel Will be Used", required = False, type = hikari.GuildChannel)
@lightbulb.command("count", "Setup Counter Channel", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def count(ctx: lightbulb.Context) -> None:
    if ctx.options.channel != None:
        try:
            channel = ctx.options.channel.strip("<>#")
            channelObject = plugin.app.cache.get_guild_channel(channel)
        except:
            channelObject = ctx.options.channel
            channel = ctx.options.channel.id
        embed = hikari.Embed(title="Counter Set in " + channelObject.mention, color = SUCCESS_COLOR)
        await ctx.respond(embed = embed)
    else:
        channel = ctx.channel_id
        embed = hikari.Embed(title="Counting Set in Current Channel", color = SUCCESS_COLOR)
        await ctx.respond(embed = embed)

    cursor.execute("UPDATE GUILDDATA SET countchannel = {} WHERE guildid = {}".format(channel, ctx.guild_id))
    database.commit()


@configure.child
@lightbulb.option("channel", "If Not Supplied Channel, The Current Channel Will be Used", required = False, type = hikari.PartialChannel)
@lightbulb.command("joinandleave", "Setup Join and Leave Message Channel", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def joinandleave(ctx: lightbulb.Context) -> None:
    if ctx.options.channel != None:
        try:
            channel = ctx.options.channel.strip("<>#")
            channelObject = plugin.app.cache.get_guild_channel(channel)
        except:
            channelObject = ctx.options.channel
            channel = ctx.options.channel.id
        embed = hikari.Embed(title = "Join and Leave Notifications Set in " + channelObject.mention, color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)
    else:
        channel = ctx.channel_id
        embed = hikari.Embed(title = "Join and Leave Notifications Set in Current Channel", color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)

    cursor.execute("UPDATE GUILDDATA SET joinleavechannel = {} WHERE guildid = {}".format(channel, ctx.guild_id))
    database.commit()


@configure.child
@lightbulb.option("message", 'Use <USER> Where The User Should Be Mentioned in the Message', required = True)
@lightbulb.command("join", "Set the Message Sent on User Join", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def join(ctx: lightbulb.Context) -> None:
    if "<USER>" in ctx.options.message:
        example = "Example: " + ctx.options.message.replace("<USER>", ctx.author.mention)
        embed = hikari.Embed(title = "Join Message Set", description = example, color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)

        cursor.execute("UPDATE GUILDDATA SET joinmessage = {} WHERE guildid = {}".format(ctx.options.message, ctx.guild_id))
        database.commit()
    else:
        embed = hikari.Embed(title = "Error", description = "Use <USER> in Message", color = FAILED_COLOR)
        embed.add_field("Example: ", '"Welcome <USER>!" \n\n Displays as.. \n\n "Welcome ' + ctx.author.mention + '!"')
        await ctx.respond(embed=embed)

@configure.child
@lightbulb.option("message", 'Use <USER> Where The User Should Be Mentioned in the Message', required = True)
@lightbulb.command("leave", "Set the Message Sent on User Leave", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def leave(ctx: lightbulb.Context) -> None:
    if "<USER>" in ctx.options.message:
        example = "Example: " + ctx.options.message.replace("<USER>", ctx.author.mention)
        embed = hikari.Embed(title = "Leave Message Set", description = example, color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)

        cursor.execute("UPDATE GUILDDATA SET leavemessage = {} WHERE guildid = {}".format(ctx.options.message, ctx.guild_id))
        database.commit()
    else:
        embed = hikari.Embed(title = "Error", description = "Use <USER> in Message", color = FAILED_COLOR)
        embed.add_field("Example: ", '"<USER> has Left the Server." \n\n Displays as.. \n\n "' + ctx.author.mention + 'has Left the Server"')
        await ctx.respond(embed=embed)


@configure.child
@lightbulb.option("channel", "If Not Supplied Channel, The Current Channel Will be Used", required = False, type = hikari.PartialChannel)
@lightbulb.command("logs", "Setup Log Channel", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def logs(ctx: lightbulb.Context) -> None:
    if ctx.options.channel != None:
        try:
            channel = ctx.options.channel.strip("<>#")
            channelObject = plugin.app.cache.get_guild_channel(channel)
        except:
            channelObject = ctx.options.channel
            channel = ctx.options.channel.id
        embed = hikari.Embed(title = "Log Notifications Set in " + channelObject.mention, color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)
    else:
        channel = ctx.channel_id
        embed = hikari.Embed(title = "Log Notifications Set in Current Channel", color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)

    cursor.execute("UPDATE GUILDDATA SET logchannel = {} WHERE guildid = {}".format(channel, ctx.guild_id))
    database.commit()

@configure.child
@lightbulb.option("role", "The Admin Role", type = hikari.Role)
@lightbulb.command("admin", "Set Admin Role", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def welcome(ctx: lightbulb.Context) -> None:
    cursor.execute("UPDATE GUILDDATA SET adminrole = {} WHERE guildid = {}".format(ctx.options.role.id, ctx.guild_id))
    database.commit()
    embed = hikari.Embed(title = "Admin Role Set", color = SUCCESS_COLOR)
    await ctx.respond(embed=embed)

@configure.child
@lightbulb.option("good", "The Good Role", type = hikari.Role, required=False)
@lightbulb.option("neutral", "The Neutral Role", type = hikari.Role, required=False)
@lightbulb.option("bad", "The Bad Role", type = hikari.Role, required=False)
@lightbulb.command("autoroles", "Auto Good/Neutral/Bad Roles Using Sentiment Analysis", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def autoroles(ctx: lightbulb.Context) -> None:
    if ctx.options.good.id != None:
        cursor.execute("UPDATE GUILDDATA SET goodrole = {} WHERE guildid = {}".format(ctx.options.good.id, ctx.guild_id))
    if ctx.options.neutral.id != None:
        cursor.execute("UPDATE GUILDDATA SET neutralrole = {} WHERE guildid = {}".format(ctx.options.neutral.id, ctx.guild_id))
    if ctx.options.bad.id != None:
        cursor.execute("UPDATE GUILDDATA SET badrole = {} WHERE guildid = {}".format(ctx.options.bad.id, ctx.guild_id))
    database.commit()
    embed = hikari.Embed(title = "Role(s) Set", color = SUCCESS_COLOR)
    await ctx.respond(embed=embed)