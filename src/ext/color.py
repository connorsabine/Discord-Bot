import lightbulb
import hikari
from constants import SUCCESS_COLOR, FAILED_COLOR, VALID_COLORS
# INIT
plugin = lightbulb.Plugin("color")


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


# COLORS DICT

# COMMANDS
@plugin.command
@lightbulb.option("name", "The Color Name", type=str)
@lightbulb.command("color", "Change Your Display Name to a New Color")
@lightbulb.implements(lightbulb.SlashCommand)
async def color(ctx):

    # Check if Color Input Valid
    if ctx.options.name not in VALID_COLORS:
        await ctx.respond(embed=hikari.Embed(title="Please Enter a Valid Color", description="All Valid Colors Can Be Found at: https://www.w3schools.com/colors/colors_names.asp", color = FAILED_COLOR))

    else:
        # Gets all Guild & User Role IDs
        guildRoleIDs = ctx.app.cache.get_roles_view_for_guild(ctx.guild_id)
        userRoleIDS = ctx.member.role_ids

        # Removes Users Other Color Roles
        for roleid in guildRoleIDs:
            roleName = plugin.app.cache.get_role(roleid)
            for key in VALID_COLORS.keys():
                if key == str(roleName):
                    if roleid in userRoleIDS:
                        await plugin.app.rest.remove_role_from_member(user=ctx.author, guild=ctx.guild_id, role=roleid)
                

        # If Color Role Already Created, Apply Role
        for roleid in guildRoleIDs:
            roleName = plugin.app.cache.get_role(roleid)
            if str(roleName) == ctx.options.name:
                await plugin.app.rest.add_role_to_member(user=ctx.author, guild=ctx.guild_id, role=roleid)
                await ctx.respond(embed=hikari.Embed(title="Color Role Applied.", color = SUCCESS_COLOR))
                return None
    

        # Create Color Role if Not Already Existing
        createdRole = await plugin.app.rest.create_role(ctx.guild_id, name=ctx.options.name, color=VALID_COLORS[ctx.options.name])

        # Add Created Role to User
        await plugin.app.rest.add_role_to_member(user=ctx.author, guild=ctx.guild_id, role=createdRole.id)

        # Reply That Color Role was Created
        await ctx.respond(embed=hikari.Embed(title="Color Role Has Been Created and Applied.", color=SUCCESS_COLOR))
