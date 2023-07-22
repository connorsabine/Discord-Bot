import lightbulb
import hikari
import sqlite3
from datetime import datetime
import pytz 

# INIT
plugin = lightbulb.Plugin("logging")
database = sqlite3.connect("bot.db")
cursor = database.cursor()
est = pytz.timezone('America/New_York') 

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# LISTENERS
# LISTENERS
# LISTENERS


# Things to Fix / Add
# - Log Bot Actions (Quote Create / Delete)

# Channel Create / Delete / Update
@plugin.listener(hikari.events.channel_events.GuildChannelCreateEvent)
async def channelCreate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Channel Created")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="Channel ID:", value=str(event.channel_id))
        embed.add_field(name="Channel Name:", value=str(event.channel))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.channel_events.GuildChannelDeleteEvent)
async def channelDelete(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Channel Deleted")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="Channel ID:", value=str(event.channel_id))
        embed.add_field(name="Channel Name:", value=str(event.channel))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.channel_events.GuildChannelUpdateEvent)
async def channelDelete(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    try:
        if data[5] in channels:
            embed = hikari.Embed(title="Channel Updated")
            embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
            embed.add_field(name="Channel ID:", value=str(event.channel_id))
            embed.add_field(name="Channel Name:", value=str(event.channel))
            if event.channel != event.old_channel:
                embed.add_field(name="Old Channel Name:", value=str(event.old_channel))
            await plugin.app.rest.create_message(data[5], embed=embed)
    except:
        pass


# Pin Update
@plugin.listener(hikari.events.channel_events.GuildPinsUpdateEvent)
async def pinUpdate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Pin Updated")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="Pin Channel ID:", value=str(event.get_channel()))
        await plugin.app.rest.create_message(data[5], embed=embed)


# # Thread Create / Delete / Update
# @plugin.listener(hikari.events.channel_events.GuildThreadCreateEvent)
# async def threadCreate(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="Thread Created")
#     
#     embed.add_field(name="Thread ID:", value=str(event.thread_id))

#     await plugin.app.rest.create_message(data[5], embed=embed)

# @plugin.listener(hikari.events.channel_events.GuildThreadDeleteEvent)
# async def threadDelete(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="Thread Deleted")
#     
#     embed.add_field(name="Thread ID:", value=str(event.thread_id))
#     await plugin.app.rest.create_message(data[5], embed=embed)

# @plugin.listener(hikari.events.channel_events.GuildThreadUpdateEvent)
# async def threadUpdate(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="Thread Updated")
#     
#     embed.add_field(name="Thread ID:", value=str(event.thread_id))
#     await plugin.app.rest.create_message(data[5], embed=embed)


# Invite Create / Delete
@plugin.listener(hikari.events.channel_events.InviteCreateEvent)
async def inviteCreate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Invite Created")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="Invite Code:", value=str(event.code))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.channel_events.InviteDeleteEvent)
async def inviteDelete(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Invite Deleted")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        await plugin.app.rest.create_message(data[5], embed=embed)


# Ban / Unban
@plugin.listener(hikari.events.guild_events.BanCreateEvent)
async def banCreate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="User Banned")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="User Banned:", value=str(event.user))
        embed.add_field(name="User ID Banned:", value=str(event.user_id))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.guild_events.BanDeleteEvent)
async def banDelete(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="User Unbanned")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="User UnBanned:", value=str(event.user))
        embed.add_field(name="User ID UnBanned:", value=str(event.user_id))
        await plugin.app.rest.create_message(data[5], embed=embed)



# Member Join / Leave / Update
@plugin.listener(hikari.events.member_events.MemberCreateEvent)
async def memberCreate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Member Joined")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="User:", value="<@{}>".format((event.user_id)))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.member_events.MemberDeleteEvent)
async def memberDelete(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Member Left")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="User:", value="<@{}>".format((event.user_id)))
        await plugin.app.rest.create_message(data[5], embed=embed)

# @plugin.listener(hikari.events.member_events.MemberUpdateEvent)
# async def memberUpdate(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="Member Updated")
#     embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
#     embed.add_field(name="User:", value="<@{}>".format((event.user_id)))
#     await plugin.app.rest.create_message(data[5], embed=embed)


# Message Create / Delete / Update
@plugin.listener(hikari.events.message_events.MessageCreateEvent)
async def messageCreate(event: hikari.events.message_events.MessageCreateEvent):
    try:
        data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
        channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
        if data[5] in channels and event.content != None:
            if event.author_id == 1019837498832203777:
                return
            embed = hikari.Embed(title="Message Created")
            embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
            embed.add_field(name="Message Author:", value=str(event.author))
            try:
                embed.add_field(name="Message Content:", value=str(event.content))
            except:
                embed.add_field(name="Message Content:", value="NoneType (Image or Embed)")

            embed.add_field(name="Message Channel:", value=str(event.channel_id))
            embed.add_field(name="Message ID:", value=str(event.message_id))
            await plugin.app.rest.create_message(data[5], embed=embed)
    except:
        pass

@plugin.listener(hikari.events.message_events.MessageDeleteEvent)
async def messageDelete(event):
    try:
        data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
        channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
        if data[5] in channels:
            data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
            embed = hikari.Embed(title="Message Deleted")
            embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
            embed.add_field(name="Message ID:", value=str(event.message_id))
            embed.add_field(name="Old Message Author:", value=str(event.old_message.author))
            embed.add_field(name="Old Message Content:", value=str(event.old_message.content))
            await plugin.app.rest.create_message(data[5], embed=embed)
    except:
        pass

# @plugin.listener(hikari.events.message_events.MessageUpdateEvent)
# async def messageUpdate(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="Message Updated")
#     embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
#     embed.add_field(name="Message Author:", value=str(event.author))
#     embed.add_field(name="Message Content:", value=str(event.content))
#     embed.add_field(name="Message Channel:", value=str(event.channel_id))
#     embed.add_field(name="Message ID:", value=str(event.message_id))
#     await plugin.app.rest.create_message(data[5], embed=embed)


# # Reaction Add / Delete All / Delete Emoji / Delete
# @plugin.listener(hikari.events.reaction_events.ReactionAddEvent)
# async def reactionAdd(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="")
#     
#     embed.add_field(name=":", value=str(event.))
#     await plugin.app.rest.create_message(data[5], embed=embed)

# @plugin.listener(hikari.events.reaction_events.ReactionDeleteAllEvent)
# async def reactionDeleteAll(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="")
#     
#     embed.add_field(name=":", value=str(event.))
#     await plugin.app.rest.create_message(data[5], embed=embed)

# @plugin.listener(hikari.events.reaction_events.ReactionDeleteEmojiEvent)
# async def reactionDeleteEmoji(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="")
#     
#     embed.add_field(name=":", value=str(event.))
#     await plugin.app.rest.create_message(data[5], embed=embed)

# @plugin.listener(hikari.events.reaction_events.ReactionDeleteEvent)
# async def reactionDelete(event):
#     data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
#     embed = hikari.Embed(title="")
#     
#     embed.add_field(name=":", value=str(event.))
#     await plugin.app.rest.create_message(data[5], embed=embed)


# Role Create / Delete / Update
@plugin.listener(hikari.events.role_events.RoleCreateEvent)
async def roleCreate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
        embed = hikari.Embed(title="Role Created")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="Role ID:", value=str(event.role_id))
        embed.add_field(name="Role Name:", value=str(event.role.name))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.role_events.RoleDeleteEvent)
async def roleDelete(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    if data[5] in channels:
        embed = hikari.Embed(title="Role Deleted")
        embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
        embed.add_field(name="Role ID:", value=str(event.old_role.role.id))
        embed.add_field(name="Role Name:", value=str(event.old_role.role.name))
        await plugin.app.rest.create_message(data[5], embed=embed)

@plugin.listener(hikari.events.role_events.RoleUpdateEvent)
async def roleUpdate(event):
    data = cursor.execute("SELECT * FROM GUILDDATA WHERE guildid={}".format(event.guild_id)).fetchone()
    channels = plugin.app.cache.get_guild_channels_view_for_guild(event.guild_id)
    try:
        if data[5] in channels:
            embed = hikari.Embed(title="Role Updated")
            embed.add_field(name="Time:", value=str(datetime.now(est).strftime("%H:%M:%S")))
            embed.add_field(name="Role ID:", value=str(event.role_id))
            embed.add_field(name="Role Name:", value=str(event.role.name))
            if event.role.name != event.old_role.role.name:
                embed.add_field(name="Old Role Name:", value=str(event.old_role.role.name))
            await plugin.app.rest.create_message(data[5], embed=embed)
    except:
        pass