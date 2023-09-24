import lightbulb
import hikari
import enum
import random
import sys
from copy import deepcopy
from constants import FAILED_COLOR, SUCCESS_COLOR, NORMAL_COLOR, RPG_INVENTORY, RPG_ENEMY_TO_LOOT
from replit import db

# INIT
plugin = lightbulb.Plugin("rpg")


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


def strToClass(classname):
    return getattr(sys.modules[__name__], classname)

def loadCharacter(userid):
    data = db["USER_DATA"][str(userid)]["RPG"]
    return Character(data["name"], data["hp"], data["maxhp"], data["hunger"], data["attack"], data["defense"], data["critchance"], data["level"], data["xp"], data["xpmult"], data["gold"], data["goldmult"], data["mode"], data["inventory"], data["enemy"], userid)

class GameMode(enum.IntEnum):
    ADVENTURE = 1
    BATTLE = 2

class Actor:
    def __init__(self, name, hp, maxhp, attack, defense, critchance, xp, gold):
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.attack = attack
        self.defense = defense
        self.critchance = critchance
        self.xp = xp
        self.gold = gold

    def fight(self, other):
        defense = min(other.defense, 19)
        missChance = random.randint(0, 20)
        critChance = random.randint(0, 100)
        crit = True if critChance < self.critchance else False

        if missChance < 20-defense: 
            damage = self.attack
            if crit:
                damage *= 1.25

        else:
            damage = 0
        other.hp -= damage

        return (damage, other.hp <= 0, crit)


class Character(Actor):
    levelCap = 10

    def __init__(self, name, hp, maxhp, hunger, attack, defense, critchance, level, xp, xpmult, gold, goldmult, mode, inventory, enemy, userid):
        super().__init__(name, hp, maxhp, attack, defense, critchance, xp, gold)
        self.level = level
        self.mode = mode
        self.inventory = inventory
        self.hunger = hunger
        self.xpmult = xpmult
        self.goldmult = goldmult

        try:
            enemyClass = strToClass(enemy["enemy"])
            self.enemy = enemyClass()
            self.enemy.rehydrate(**enemy)
        except:
            self.enemy = None
        self.userid = userid
      

    def saveToDatabase(self):
        character = deepcopy(vars(self))
        if self.enemy != None:
            character["inventory"] = deepcopy(self.inventory)
            character["enemy"] = deepcopy(vars(self.enemy))
            db["USER_DATA"][str(character["userid"])]["RPG"] = {"name":character['name'],"hp":character['hp'],"maxhp":character['maxhp'],"hunger":character['hunger'],"attack":character['attack'],"defense":character['defense'],"critchance":character['critchance'],"level":character['level'],"xp":character['xp'],"xpmult":character['xpmult'],"gold":character['gold'],"goldmult":character['goldmult'],"mode":character['mode'],"inventory":character["inventory"],"enemy":character["enemy"]}
        else:
            character["inventory"] = deepcopy(self.inventory)
            db["USER_DATA"][str(character["userid"])]["RPG"] = {"name":character['name'],"hp":character['hp'],"maxhp":character['maxhp'],"hunger":character['hunger'],"attack":character['attack'],"defense":character['defense'],"critchance":character['critchance'],"level":character['level'],"xp":character['xp'],"xpmult":character['xpmult'],"gold":character['gold'],"goldmult":character['goldmult'],"mode":character['mode'],"inventory":character["inventory"],"enemy":None}

    def hunt(self):
        while True:
            enemyType = random.choice(Enemy.__subclasses__())
            if enemyType.minLevel <= self.level:
                break

        enemy = enemyType()
        self.mode = GameMode.BATTLE
        self.enemy = enemy
        self.saveToDatabase()
        return enemy

    def action(self):
        if self.hunger > 3:
            self.hunger -= .5
            embed = None
        elif self.hunger > 0:
            self.hunger -= .5
            embed = hikari.Embed(title=f"{self.name} is Close to Starving", description=f"**HP:**    {self.hp}/{self.maxhp}\n**HUNGER:**    {self.hunger}/10", color=FAILED_COLOR)
        else:
            self.hp -= 1
            embed = hikari.Embed(title=f"{self.name} is Starving", description=f"**HP:**    {self.hp}/{self.maxhp}\n**HUNGER:**    {self.hunger}/10", color=FAILED_COLOR)
       
        self.saveToDatabase()
        return embed 

    def fight(self, enemy):
        outcome = super().fight(enemy)
        self.saveToDatabase()
        return outcome

    def flee(self, enemy):
        if random.randint(0,1+self.defense):
            damage = 0
        else:
            damage = self.enemy.attack/2
            self.hp -= damage

        self.enemy = None
        self.mode = GameMode.ADVENTURE
        self.saveToDatabase()

        return (damage, self.hp <= 0)

    def loot(self, enemy):
        lootType = RPG_ENEMY_TO_LOOT[enemy.enemy]
        lootCount = random.randint(0, 3)
        self.inventory[lootType] += lootCount
        self.saveToDatabase()
        return lootType, lootCount

    def defeat(self, enemy):
        if self.level < self.levelCap:
            self.xp += enemy.xp * self.xpmult

        self.gold += enemy.gold * self.goldmult
        self.enemy = None
        self.mode = GameMode.ADVENTURE
        ready, _ = self.readyToLevelUp()

        self.saveToDatabase()
        return (enemy.xp, enemy.gold, ready)
    
    def scavenge(self):
        items = ["Wood", "Wood", "Rock", "Rock", "String", "Coal", "Berries", "Berries", "Meat", "Meat"]
        randomCount = random.randint(1, 3)
        itemsFound = []

        while len(itemsFound) < randomCount:
            randomItem = items[random.randint(0, len(items)-1)]
            if randomItem == "Wood":
                self.inventory["wood"] += 1
                itemsFound.append("Wood")
                
            elif randomItem == "Rock":
                self.inventory["rock"] += 1
                itemsFound.append("Rock")
                
            elif randomItem == "String":
                self.inventory["string"] += 1
                itemsFound.append("String")

            elif randomItem == "Coal":
                self.inventory["coal"] += 1
                itemsFound.append("Coal")
                
            elif randomItem == "Berries":
                self.inventory["berries"] += 3
                itemsFound.append("Berries")

            elif randomItem == "Meat":
                self.inventory["meat"] += 1
                itemsFound.append("Meat")

        self.saveToDatabase()
        return itemsFound

    def readyToLevelUp(self):
        if self.level == self.levelCap:
            return (False, 0)
            
        xpNeeded = (self.level)*10
        return (self.xp >= xpNeeded, xpNeeded-self.xp)


    def levelUp(self, increase):
        ready, _ = self.readyToLevelUp()
        if not ready:
            return (False, self.level)
            
        self.level += 1
        setattr(self, increase, getattr(self, increase)+1)
        self.hp = self.maxhp
        self.hunger = 10
        self.xp = 0
        
        self.saveToDatabase()
        return (True, self.level)

    def die(self, userid):
        db["USER_DATA"][str(userid)]["RPG"] = None
      

class Enemy(Actor):
    def __init__(self, name, maxhp, attack, defense, critchance, xp, gold):
        super().__init__(name, maxhp, maxhp, attack, defense, critchance, xp, gold)
        self.enemy = self.__class__.__name__
      
    def rehydrate(self, name, hp, maxhp, attack, defense, critchance, xp, gold, enemy):
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.attack = attack
        self.defense = defense
        self.critchance = critchance
        self.xp = xp
        self.gold = gold
        self.enemy = enemy
      

# NAME, HP, ATTACK, DEFENSE, CRITCHANCE, XP, GOLD
class Scorpion(Enemy):
    minLevel = 1
    def __init__(self):
        super().__init__("🦂 Scorpion", 2, 1, 1, 10, 1, 1)
        
class Snake(Enemy):
    minLevel = 1
    def __init__(self):
        super().__init__('🐍 Snake', 3, 2, 1, 10, 1, 2)
        
class Zombie(Enemy):
    minLevel = 1
    def __init__(self):
        super().__init__('🧟‍♂️ Zombie', 4, 2, 1, 10, 2, 1)
        
class Ghost(Enemy):
    minLevel = 2
    def __init__(self):
        super().__init__('👻 Ghost', 5, 3, 1, 15, 2, 2)
        
class Wolf(Enemy):
    minLevel = 2
    def __init__(self):
        super().__init__('🐺 Wolf', 6, 3, 2, 15, 2, 2)
        
class Vampire(Enemy):
    minLevel = 3
    def __init__(self):
        super().__init__('🧛‍♂️ Vampire', 7, 4, 1, 15, 3, 3)
        
class Yeti(Enemy):
    minLevel = 3
    def __init__(self):
        super().__init__('❄️ Yeti', 8, 4, 2, 15, 3, 3)
        
class Cyborg(Enemy):
    minLevel = 4
    def __init__(self):
        super().__init__('🤖 Cyborg', 9, 5, 1, 2, 4, 4)

class Dragon(Enemy):
    minLevel = 5
    def __init__(self):
        super().__init__('🐉 Dragon', 10, 6, 2, 2, 5, 5)



def statusEmbed(ctx, character, createdNow):
    if character.mode == GameMode.BATTLE:
        modeText = f"Currently Battling a {character.enemy.name}"
        color = FAILED_COLOR
    elif character.mode == GameMode.ADVENTURE:
        modeText = "Currently Adventuring"
        color = NORMAL_COLOR

    if createdNow == True:
        title = f"Character {character.name} Created!"
    elif createdNow == False:
        title = f"Character {character.name} Already Exists!"
    else:
        title = f"{character.name} Stats:"

    embed = hikari.Embed(title=title, description=modeText, color=color)

    _, xpNeeded = character.readyToLevelUp()

    embed.add_field(name="Stats", value=f"""
**HP:**    {character.hp}/{character.maxhp}
**HUNGER:**    {character.hunger}/10
**ATTACK:**   {character.attack}
**DEFENSE:**   {character.defense}
**CRIT CHANCE:**   {character.critchance}%
**LEVEL:** {character.level}
**XP:**    {character.xp}/{character.xp+xpNeeded}
    """, inline=True)

    descriptionOne = f"Gold: {character.gold}"
    descriptionTwo = ""

    if character.inventory["berries"] > 0:
        descriptionOne += f"\n Berries: {character.inventory['berries']}"
    if character.inventory["meat"] > 0:
        descriptionOne += f"\n Meat: {character.inventory['meat']}"
    if character.inventory["cookedmeat"] > 0:
        descriptionOne += f"\n Cooked Meat: {character.inventory['cookedmeat']}"
    if character.inventory["wood"] > 0:
        descriptionOne += f"\n Wood: {character.inventory['wood']}"
    if character.inventory["string"] > 0:
        descriptionOne += f"\n String: {character.inventory['string']}"
    if character.inventory["coal"] > 0:
        descriptionOne += f"\n Coal: {character.inventory['coal']}"

    if character.inventory["stinger"] > 0:
        descriptionTwo += f"\n Scorpion Stinger: {character.inventory['stinger']}"
    if character.inventory["venom"] > 0:
        descriptionTwo += f"\n Snake Venom: {character.inventory['venom']}"
    if character.inventory["heart"] > 0:
        descriptionTwo += f"\n Zombie Heart: {character.inventory['heart']}"
    if character.inventory["essence"] > 0:
        descriptionTwo += f"\n Ghost Essence: {character.inventory['essence']}"
    if character.inventory["bone"] > 0:
        descriptionTwo += f"\n Wolf Bone: {character.inventory['bone']}"
    if character.inventory["fang"] > 0:
        descriptionTwo += f"\n Vampire Fang: {character.inventory['fang']}"
    if character.inventory["hide"] > 0:
        descriptionTwo += f"\n Yeti Hide: {character.inventory['hide']}"
    if character.inventory["metalshard"] > 0:
        descriptionTwo += f"\n Metal Shard: {character.inventory['metalshard']}"
    if character.inventory["dragonscale"] > 0:
        descriptionTwo += f"\n Dragon Scale: {character.inventory['dragonscale']}"
        
        


    embed.add_field(name="Items:", value=descriptionOne, inline=True)
    if descriptionTwo != "":
        embed.add_field(name="Enemy Drops:", value=descriptionTwo, inline=True)
    # embed.add_field(name="Upgrades", value=f"**XP MULT**: {character.xpmult}\n **GOLD MULT:**  {character.goldmult}")

    return embed 

def huntEmbed(ctx, enemy, character):
    embed = hikari.Embed(title=f"You Encountered a  {enemy.name}", color=FAILED_COLOR)
    embed.add_field(name="Stats:", value=f"""
**HP:**    {enemy.hp}
**ATTACK:**   {enemy.attack}
**DEFENSE:**   {enemy.defense}
**XP ON KILL:**    {enemy.xp * character.xpmult}
**GOLD ON KILL:**    {enemy.gold * character.goldmult}
    """)

    embed.add_field(name="**Do You:**", value="**/rpg fight** or **/rpg flee**")
    return embed 

def scavengeEmbed(ctx, item):
    embed = hikari.Embed(title=f"You Found {item}!", color=SUCCESS_COLOR)
    return embed 



# RPG COMMANDS
@plugin.command
@lightbulb.command("rpg", "RPG Base Command")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def rpg(ctx: lightbulb.Context) -> None:
    await ctx.respond("Invoked RPG")



@rpg.child
@lightbulb.option(name="name", description="Name of Character", required=False)
@lightbulb.command(name="create", description="Creates a Character")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def create(ctx: lightbulb.Context, name = None):
    player = db["USER_DATA"][str(ctx.author.id)]["RPG"]
    if player == None:
        if ctx.options.name == None:
            name = ctx.author.username
        else:
            name = ctx.options.name

        character = Character(**{
            "name": name,
            "hp": 20,
            "maxhp": 20,
            "hunger":10,
            "attack": 2,
            "defense": 1,
            "critchance": 10,   
            "level": 1,
            "xp": 0,
            "xpmult": 1,
            "gold": 0,
            "goldmult": 1, 
            "mode": GameMode.ADVENTURE,
            "inventory": RPG_INVENTORY,
            "enemy": None,
            "userid": ctx.author.id
        })

        db["USER_DATA"][str(ctx.author.id)]["RPG"] = {"name":name,"hp":20,"maxhp":20,"hunger":10,"attack":2,"defense":1,"critchance":10,"level":1,"xp":0,"xpmult":1,"gold":0,"goldmult":1,"mode":GameMode.ADVENTURE,"inventory":RPG_INVENTORY,"enemy":None}

        embed = statusEmbed(ctx, character, True)
        await ctx.respond(embed=embed)
    else:
        character = loadCharacter(ctx.author.id)
        embed = statusEmbed(ctx, character, False)
        await ctx.respond(embed=embed)



@rpg.child
@lightbulb.command(name="stats", description="Get Character Stats")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def stats(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    embed = statusEmbed(ctx, character, None)
    await ctx.respond(embed=embed)



@rpg.child
@lightbulb.command(name="hunt", description="Look for an Enemy to Fight")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hunt(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if character.mode != GameMode.ADVENTURE:
        embed = hikari.Embed(title="You Must be Outside of a Battle to Call this Command", color=NORMAL_COLOR)
        await ctx.respond(embed)
        return
    
    character.action()
    enemy = character.hunt()
    embed = huntEmbed(ctx, enemy, character)
    await ctx.respond(embed=embed)



@rpg.child
@lightbulb.command(name="fight", description="Fight the Enemy")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def fight(ctx):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if character.mode != GameMode.BATTLE:
        embed = hikari.Embed(title="This Command can Only be Called in Battle", color=NORMAL_COLOR)
        await ctx.respond(embed=embed)
        return
    
    enemy = character.enemy

    damage, killed, crit = character.fight(enemy)
    if damage > 0:
        if crit:
            embed = hikari.Embed(title="Battle in Progress...", description=f"**CRITICAL HIT!**\n{character.name} Attacks {enemy.name} Dealing {damage} Damage!", color=FAILED_COLOR)
            embed.add_field(name="Stats:", value=f"**{enemy.name} HP:**    {enemy.hp}/{enemy.maxhp} \n**{character.name} HP:**    {character.hp}/{character.maxhp}")
            await ctx.respond(embed=embed)
        else:
            embed = hikari.Embed(title="Battle in Progress...", description=f"{character.name} Attacks {enemy.name} Dealing {damage} Damage!", color=FAILED_COLOR)
            embed.add_field(name="Stats:", value=f"**{enemy.name} HP:**    {enemy.hp}/{enemy.maxhp} \n**{character.name} HP:**    {character.hp}/{character.maxhp}")
            await ctx.respond(embed=embed)

    else:
        embed = hikari.Embed(title="Battle in Progress...", description=f"{character.name} Attacks {enemy.name} but Misses!", color=FAILED_COLOR)
        embed.add_field(name="Stats:", value=f"**{enemy.name} HP:**    {enemy.hp}/{enemy.maxhp} \n**{character.name} HP:**    {character.hp}/{character.maxhp}")
        await ctx.respond(embed=embed)

    if killed:
        xp, gold, readyToLevelUp = character.defeat(enemy)
        lootType, lootCount = character.loot(enemy)
        embed = hikari.Embed(title=f"{enemy.name} Defeated!", color=SUCCESS_COLOR)
        value = f"**XP:**    {xp} \n**GOLD:**    {gold}"
        if lootCount > 0:
            value += f"\n**{lootType.upper()}:**    {lootCount}"
        embed.add_field(name="Loot:", value=value)
        embed.add_field(name="Stats:", value=f"**HP:**    {character.hp}/{character.maxhp}")
        
        if readyToLevelUp:
            embed.add_field(name=f"{character.name} has Earned Enough XP to Advance to Level {character.level+1}", value="Run '/rpg levelup' With the Stat (HP, ATTACK, DEFENSE) you Would Like to Increase")
        await plugin.app.rest.create_message(ctx.channel_id, embed=embed)
        return


    damage, killed, crit = enemy.fight(character)
    if damage > 0:
        if crit:
            embed = hikari.Embed(title="Battle in Progress...", description=f"**CRITICAL HIT!**\n{enemy.name} Attacks {character.name} Dealing {damage} Damage! \n**Enemy HP:**    {enemy.hp}/{enemy.maxhp} \n**{character.name} HP:**    {character.hp}/{character.maxhp}", color=FAILED_COLOR)
            await plugin.app.rest.create_message(ctx.channel_id, embed=embed)
        else:
            embed = hikari.Embed(title="Battle in Progress...", description=f"{enemy.name} Attacks {character.name} Dealing {damage} Damage! \n**Enemy HP:**    {enemy.hp}/{enemy.maxhp} \n**{character.name} HP:**    {character.hp}/{character.maxhp}", color=FAILED_COLOR)
            await plugin.app.rest.create_message(ctx.channel_id, embed=embed)

    else:
        embed = hikari.Embed(title="Battle in Progress...", description=f"{enemy.name} Attacks {character.name} but Misses \n**Enemy HP:**    {enemy.hp}/{enemy.maxhp} \n**{character.name} HP:**    {character.hp}/{character.maxhp}", color=FAILED_COLOR)
        await plugin.app.rest.create_message(ctx.channel_id, embed=embed)


    embed = character.action()
    if embed != None:
        await plugin.app.rest.create_message(ctx.channel_id, embed=embed)
    character.saveToDatabase()


    if killed:
        character.die(ctx.author.id)
        
        embed = hikari.Embed(title=f"{character.name} Died in the Hands of a {enemy.name}", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return

    embed = hikari.Embed(title="The Battle Continues!", description="Do You **/rpg fight** or **/rpg flee**", color=NORMAL_COLOR)
    await plugin.app.rest.create_message(ctx.channel_id, embed=embed)



@rpg.child
@lightbulb.command(name="flee", description="Flee from the Enemy")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def flee(ctx):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if character.mode != GameMode.BATTLE:
        embed = hikari.Embed(title="This Command can Only be Called in Battle", color=NORMAL_COLOR)
        await ctx.respond(embed=embed)
        return

    enemy = character.enemy
    damage, killed = character.flee(enemy)

    if killed:
        character.die(ctx.author.id)
        embed = hikari.Embed(title=f"{character.name} Died in the Hands of a {enemy.name} While Fleeing", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
    elif damage:
        embed = hikari.Embed(title=f"{character.name} Flees the {enemy.name} Taking {damage} Damage \nHP: {character.hp}/{character.maxhp}", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
    else:
        embed = hikari.Embed(title=f"{character.name} Flees the {enemy.name} with Their Life \nHP: {character.hp}/{character.maxhp}", color=FAILED_COLOR)
        await ctx.respond(embed=embed)

    embed = character.action()
    if embed != None:
        await plugin.app.rest.create_message(ctx.channel_id, embed=embed)
    character.saveToDatabase()



@rpg.child
@lightbulb.option(name="stat", description="The Stat to Increase", choices=["HP", "ATTACK", "DEFENSE"])
@lightbulb.command(name="levelup", description="Pick a Stat to Increase (HP, ATTACK, DEFENSE)")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def levelup(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return

    if character.mode != GameMode.ADVENTURE:
        embed = hikari.Embed(title="This Command can't be Called in Battle", color=NORMAL_COLOR)
        await ctx.respond(embed=embed)
        return

    ready, xpNeeded = character.readyToLevelUp()
    if not ready:
        embed = hikari.Embed(title=f"You Need {xpNeeded} More XP to Advance to Level {character.level+1}", color=NORMAL_COLOR)
        await ctx.respond(embed=embed)
        return
    

    increase = ctx.options.stat.lower()
    if increase == "hp":
        increase = "maxhp"

    success, newLevel = character.levelUp(increase)
    if success:
        embed = hikari.Embed(title=f"{character.name} Advanced to Level {newLevel}, Gaining 1 {increase.upper()}", color=SUCCESS_COLOR)
        await ctx.respond(embed=embed)
    else:
        embed = hikari.Embed(title=f"{character.name} Failed to Level Up", color=FAILED_COLOR)
        await ctx.respond(embed=embed)



@rpg.child
@lightbulb.command(name="shop", description="Opens Shop")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def shop(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    embed = hikari.Embed(title="Shop", description=f"Current Gold: {character.gold}", color=NORMAL_COLOR)
    embed.add_field(name="**BANDAID:**", value="HEALS 5 HP\n5 GOLD", inline=True)
    embed.add_field(name="**HEALTH POTION:** ", value="HEALLS FULLY\n10 GOLD", inline=True)
    embed.add_field(name="**HP BOOST:**", value="+1 HP\n15 GOLD", inline=True)
    embed.add_field(name="**DEFENSE BOOST:**", value="+1 DEFENSE\n15 GOLD", inline=True)
    embed.add_field(name="**ATTACK BOOST:**", value="+1 ATTACK\n15 GOLD", inline=True)
    embed.add_field(name="**XP MULTIPLIER:**", value="+50% XP ON KILL\n20 GOLD", inline=True)
    embed.add_field(name="**GOLD MULTIPLIER:**", value="+50% GOLD ON KILL\n20 GOLD", inline=True)
    await ctx.respond(embed=embed)



@rpg.child
@lightbulb.option(name="item", description="The Item to Buy", choices=["BANDAID", "HEALTH POTION", "HP BOOST", "DEFENSE BOOST", "ATTACK BOOST", "XP MULTIPLIER", "GOLD MULTIPLIER"])
@lightbulb.command(name="buy", description="Buy Item From Shop")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def buy(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if ctx.options.item == "BANDAID" and character.gold >= 5:
        if character.hp + 5 > 20:
            character.hp = 20
        else:
            character.hp += 5
        character.gold -= 5

    elif ctx.options.item == "HEALTH POTION" and character.gold >= 10:
        character.hp = 20
        character.gold -= 10

    elif ctx.options.item == "HP BOOST" and character.gold >= 15:
        character.maxhp += 1
        character.gold -= 15

    elif ctx.options.item == "DEFENSE BOOST" and character.gold >= 15:
        character.defense += 1
        character.gold -= 15

    elif ctx.options.item == "ATTACK BOOST" and character.gold >= 15:
        character.attack += 1
        character.gold -= 15

    elif ctx.options.item == "XP MULTIPLIER" and character.gold >= 20:
        character.xpmult += .5
        character.gold -= 20

    elif ctx.options.item == "GOLD MULTIPLIER" and character.gold >= 20:
        character.goldmult += .5
        character.gold -= 20

    else:
        embed = hikari.Embed(title=f"{character.name} Doesn't Have Enough Gold to Buy {ctx.options.item}", color=NORMAL_COLOR)
        await ctx.respond(embed=embed)
        return
    
    character.saveToDatabase()
    embed = hikari.Embed(title=f"{character.name} Purchased {ctx.options.item}", color=NORMAL_COLOR)
    await ctx.respond(embed=embed)
    embed = statusEmbed(ctx, character, None)
    await plugin.app.rest.create_message(ctx.channel_id, embed=embed)



@rpg.child
@lightbulb.command(name="reset", description="Delete Current Character")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def die(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    character.die(ctx.author.id)
    embed = hikari.Embed(title=f"Character {character.name} Deleted", color=FAILED_COLOR)
    await ctx.respond(embed=embed)



@rpg.child
@lightbulb.command(name="scavenge", description="Scavenge Through the Wilderness for Extra Resources")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def scavenge(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if character.mode != GameMode.ADVENTURE:
        embed = hikari.Embed(title="You Must be Outside of a Battle to Call this Command", color=NORMAL_COLOR)
        await ctx.respond(embed)
        return

    if random.randint(0, 8) == 1:
        enemy = character.hunt()
        embed = huntEmbed(ctx, enemy, character)
        await ctx.respond(embed=embed)
    else:
        items = character.scavenge()
        embed = scavengeEmbed(ctx, items[0])
        await ctx.respond(embed=embed)
        items.pop(0)
        while len(items) > 0:
            embed = scavengeEmbed(ctx, items[0])
            await plugin.app.rest.create_message(ctx.channel_id, embed=embed)
            items.pop(0)

    embed = character.action()
    if embed != None:
        await plugin.app.rest.create_message(ctx.channel_id, embed=embed)



@rpg.child
@lightbulb.option(name="food", description="The Food to Eat (Berries = +0.5 Hunger, Meat = +2 Hunger)", choices=["BERRIES", "MEAT"])
@lightbulb.command(name="eat", description="Eat Food")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def eat(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if character.mode != GameMode.ADVENTURE:
        embed = hikari.Embed(title="You Must be Outside of a Battle to Call this Command", color=NORMAL_COLOR)
        await ctx.respond(embed)
        return

    if ctx.options.food == "BERRIES":
        berryCount = character.inventory["berries"]
        if berryCount <= 0:
            embed = hikari.Embed(title=f"{character.name} Has No Berries to Eat", color=NORMAL_COLOR)
            await ctx.respond(embed)
            return
        else:
            numEaten = 0
            while character.hunger < 10 and character.inventory["berries"] > 0:
                character.hunger += .5
                numEaten += 1
                character.inventory["berries"] -= 1
            embed = hikari.Embed(title=f"{character.name} ate {numEaten} Berries", color=NORMAL_COLOR)
            await ctx.respond(embed)

    else:
        if character.inventory["cookedmeat"] == 0:
            if character.inventory["meat"] == 0:
                embed = hikari.Embed(title=f"{character.name} has no Cooked Meat to Eat", color=NORMAL_COLOR)
                await ctx.respond(embed)
                return
            else:
                embed = hikari.Embed(title=f"{character.name} Can't Eat Uncooked Meat!\n Run **/rpg cook**", color=NORMAL_COLOR)
                await ctx.respond(embed)
                return
        else:
            numEaten = 0
            while character.hunger < 10:
                character.hunger += 2
                numEaten += 1
            character.inventory["cookedmeat"] -= numEaten
            embed = hikari.Embed(title=f"{character.name} ate {numEaten} Cooked Meats", color=NORMAL_COLOR)
            await ctx.respond(embed)

    if character.hunger > 10:
        character.hunger = 10

    character.saveToDatabase()



@rpg.child
@lightbulb.option(name="fuel", description="The Type of Fuel to Use (2 Wood or 1 Coal for Each Meat)", choices=["WOOD", "COAL"])
@lightbulb.command(name="cook", description="Cooks Food")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def cook(ctx: lightbulb.Context):
    try:
        character = loadCharacter(ctx.author.id)
    except:
        embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    
    if character.inventory["meat"] <= 0:
        embed = hikari.Embed(title=f"{character.name} has no Meat to Cook", color=FAILED_COLOR)
        await ctx.respond(embed=embed)
        return
    else:
        if ctx.options.fuel == "WOOD":
            if character.inventory["wood"]-2 < 0:
                embed = hikari.Embed(title=f"{character.name} Doesn't Have Enough Wood to Cook With", color=FAILED_COLOR)
                await ctx.respond(embed=embed)
                return
            else:
                numCooked = 0
                while character.inventory["meat"] > 0 and character.inventory["wood"]-1 > 0:
                    character.inventory["wood"] -= 2
                    character.inventory["meat"] -= 1
                    character.inventory["cookedmeat"] += 1
                    numCooked += 1
                
                embed = hikari.Embed(title=f"{character.name} Cooked {numCooked} Meat", color=NORMAL_COLOR)
                await ctx.respond(embed=embed)

        else:
            if character.inventory["coal"] > 0:
                embed = hikari.Embed(title=f"{character.name} Doesn't Have Enough Coal to Cook With", color=FAILED_COLOR)
                await ctx.respond(embed=embed)
                return
            else:
                numCooked = 0
                while character.inventory["meat"] > 0 and character.inventory["wood"] > 0:
                    character.inventory["coal"] -= 1
                    character.inventory["meat"] -= 1
                    character.inventory["cookedmeat"] += 1
                    numCooked += 1
                
                embed = hikari.Embed(title=f"{character.name} Cooked {numCooked} Meat", color=NORMAL_COLOR)
                await ctx.respond(embed=embed)

    character.saveToDatabase()

# @rpg.child
# @lightbulb.command(name="craft", description="Crafts Items", choices=["WOOD SWORD", "IRON SWORD"])
# @lightbulb.implements(lightbulb.SlashSubCommand)
# async def craft(ctx: lightbulb.Context):
#     try:
#         character = loadCharacter(ctx.author.id)
#     except:
#         embed = hikari.Embed(title="Character not Created Yet", description="Run **/rpg create** to Start Your Adventure!", color=FAILED_COLOR)
#         await ctx.respond(embed=embed)
#         return

#     embed = hikari.Embed(title=f"Crafting Not Yet Implemented", color=FAILED_COLOR)
#     await ctx.respond(embed=embed)

