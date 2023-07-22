import lightbulb
import hikari
import sqlite3
from constants import SUCCESS_COLOR, FAILED_COLOR, NORMAL_COLOR



# INIT
plugin = lightbulb.Plugin("moderation")
database = sqlite3.connect("bot.db")
cursor = database.cursor()



# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)



# ADMIN COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(perm1=hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("moderation", "Moderation Commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def moderation(ctx: lightbulb.Context) -> None:
    await ctx.respond("Invoked Admin")



# QUOTE COMMAND GROUP
@moderation.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(perm1=hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("quote", "Quote Admin Commands", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubGroup)
async def quoteAdmin(ctx: lightbulb.Context) -> None:
    await ctx.respond("Invoked Quote Admin")


@quoteAdmin.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(perm1=hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("list", "Lists all Quotes and Indexes", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.Context):
    msg = ""
    data = cursor.execute("SELECT *, rowid FROM QUOTEDATA{}".format(ctx.guild_id)).fetchall()
    for row in data:
        if len(msg) > 1750:
            await ctx.respond(msg)
            msg = ""
        msg += "\n " + str(row[2]) + ' - "' + row[1] + '" - ' + row[0]
    if len(data) == 0:
        await ctx.respond("No Quotes")
    else:
        await ctx.respond(msg)

@quoteAdmin.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(perm1=hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("index", "Index of Quote to be Deleted")
@lightbulb.command("delete", "Deletes a Quote by Index", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def delete(ctx: lightbulb.Context):
    cursor.execute("DELETE FROM QUOTEDATA{} WHERE rowid = {}".format(ctx.guild_id, ctx.options.index))
    database.commit()
    if (cursor.rowcount > 0):
        await ctx.respond("Quote Deleted")
    else:
        await ctx.respond("Quote Doesn't Exist")



# BAN/UNBAN/KICK/OP/DEOP
@moderation.child
@lightbulb.option("user", "The User to Ban", type = hikari.Member)
@lightbulb.command("ban", "Bans a User", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ban(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title = "Banned " + ctx.options.user.mention, color = SUCCESS_COLOR)
    await ctx.respond(embed=embed)
    await plugin.app.rest.ban_user(ctx.guild_id, ctx.options.user.id)

@moderation.child
@lightbulb.option("user", "The User ID to Unban")
@lightbulb.command("unban", "Unbans a User", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def unban(ctx: lightbulb.Context) -> None:
    await plugin.app.rest.unban_user(ctx.guild_id, ctx.options.user)
    embed = hikari.Embed(title = "Unbanned User", color = SUCCESS_COLOR)
    await ctx.respond(embed=embed)

@moderation.child
@lightbulb.option("user", "The User to Kick", type = hikari.Member)
@lightbulb.command("kick", "Kicks a User", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def kick(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title = "Kicked " + ctx.options.user.mention, color = SUCCESS_COLOR)
    await ctx.respond(embed=embed)
    await plugin.app.rest.kick_user(ctx.guild_id, ctx.options.user.id)

@moderation.child
@lightbulb.option("user", "The User", type = hikari.Member)
@lightbulb.command("op", "Gives Admin to a User", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def op(ctx: lightbulb.Context) -> None:
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(ctx.guild_id)).fetchone()
    try:
        await plugin.app.rest.add_role_to_member(user=ctx.options.user.id, guild=ctx.guild_id,role=data[1])
        embed = hikari.Embed(title = "Admin Applied", color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)
    except:
        embed = hikari.Embed(title = "Error", description = "Admin Not Set to a Valid Role", color = FAILED_COLOR)
        await ctx.respond(embed=embed)
      
@moderation.child
@lightbulb.option("user", "The User", type = hikari.Member)
@lightbulb.command("deop", "Takes Admin From a User", ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def deop(ctx: lightbulb.Context) -> None:
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(ctx.guild_id)).fetchone()
    try:
        await plugin.app.rest.remove_role_from_member(user=ctx.options.user.id, guild=ctx.guild_id,role=data[1])
        embed = hikari.Embed(title = "Admin Applied", color = SUCCESS_COLOR)
        await ctx.respond(embed=embed)
    except:
        embed = hikari.Embed(title = "Error", description = "Admin Not Set to a Valid Role", color = FAILED_COLOR)
        await ctx.respond(embed=embed)

