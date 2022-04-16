import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands import has_role
import os
import sys
import random
from resprocess import getvalues, gettreevalues
from readtax import readtax
from readtax import readtreasure
from tiers import tier0
from tiers import readtier
from upgrades import upgradelist as listofupgrades
from upgrades import purchaseupgrade, whathaveupg
from mining import minemultiplier, lumbermultiplier
from directional import enterdungeon
from misc import writewallet, readwallet
from creators import createclass, createenemy, createdungeon

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
dirr = sys.path[0]

wb = bot.create_group('wb', 'World Builder command prefix.')


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(f"Py-Cord version: {discord.__version__}")
    await bot.change_presence(activity=discord.Game('Powered by NLS: https://www.nitelifesoftware.com'))


@bot.event
async def on_guild_join(guild):
    if not os.path.exists(f"{dirr}/World/{str(guild.id)}"):  # Creates server folders if they do not exist already.
        os.mkdir(f"{dirr}/World/{str(guild.id)}")
        os.mkdir(f"{dirr}/World/{str(guild.id)}/upgrades")
        os.mkdir(f"{dirr}/World/{str(guild.id)}/Players")
        os.mkdir(f"{dirr}/World/{str(guild.id)}/inventory")
        with open(f"{dirr}/World/{str(guild.id)}/treasury.txt", "w+") as f:
            f.write(str(10000))
            f.close()
        with open(f"{dirr}/World/{str(guild.id)}/taxrate.txt", "w+") as f:
            f.write(str(0.25))
            f.close()
        tier0(f"{dirr}/World/{str(guild.id)}")


testing = [904120920862519396]
Support = [904120920862519396]


@wb.command(description="Command for miners to gather minerals, stone, iron, gold, etc.")
@commands.cooldown(rate=1, per=3600, type=commands.BucketType.member)
async def mine(ctx):
    guildid = str(ctx.guild.id)
    memberid = str(ctx.user.id)
    if not os.path.exists(f"{dirr}/World/{guildid}/Players/{memberid}"):
        os.mkdir(f"{dirr}/World/{guildid}/Players/{memberid}")
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "w+") as f:
            f.write(str(250))  # Starting currency number will be customizable.
            f.close()
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/name.txt", "w+") as f:
            f.write(ctx.user.name)
            f.close()
    taxrate = float(readtax(f"{dirr}/World/{guildid}/taxrate.txt"))
    taxratepercent = round(taxrate * 100)
    resources, values = getvalues()  # will be replaced with something more complex.
    roll = random.randint(-10, 50)
    res = random.randint(0, len(resources) - 1)
    with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "r") as f:
        currency = f.read()
        f.close()
    if roll < 0:
        value = values[res]
        vaftertax = (round(float(value)) * round(float(roll)))
        fpay = round(vaftertax)
        totalcurr = str(round(float(currency) + fpay))
        streas = readtreasure(f"{dirr}/World/{guildid}/treasury.txt")
        with open(f"{dirr}/World/{guildid}/treasury.txt", "w+") as treas:
            treas.write(str(float(streas) + (fpay * -1)))
            treas.close()
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "w+") as f:
            f.write(totalcurr)
            f.close()
        if not os.path.exists(
                f"{dirr}/World/{guildid}/Players/{memberid}/inventory"):  # Creates inventory folder if it does not
            # exist
            os.mkdir(f"{dirr}/World/{guildid}/Players/{memberid}/inventory")
        await ctx.respond(
            f"While mining, a tunnel collapsed. While you narrowly escaped, you must pay the kingdom your losses. "
            f"Losses: {fpay}. Your current currency: {totalcurr}")
    else:
        resourcename = resources[res].replace(".txt", "")
        value = values[res]
        taxvalue = (round(float(value)) * round(float(roll))) * taxrate
        fpay = ((round(float(value)) * round(float(roll))) - taxvalue) * float(
            minemultiplier(f"{dirr}/World/{guildid}"))
        totalcurr = str(round((float(currency) + float(fpay))))
        streas = readtreasure(f"{dirr}/World/{guildid}/treasury.txt")
        with open(f"{dirr}/World/{guildid}/treasury.txt", "w+") as treas:
            treas.write(str(float(streas) + fpay))
            treas.close()
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "w+") as f:
            f.write(totalcurr)
            f.close()

        if os.path.exists(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt"):
            with open(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt", "r") as f:
                line = f.readline()
                f.close()

            with open(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt", "w") as f:
                f.write(str(int(line) + roll))
                f.close()
        else:
            with open(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt", "w+") as f:
                f.write(str(roll))
                f.close()
        await ctx.respond(
            f"You have collected {roll} {resourcename}. You have earned {fpay} currency after tax, {round(float(value)) * round(float(roll))} before tax. Current tax rate is {taxratepercent}% and the current mining multiplier is {float(minemultiplier(f'{dirr}/World/{guildid}'))}x. Your current currency: {totalcurr}")



@wb.command(description="Command for Lumberjacks to gather wood.")
@commands.cooldown(rate=1, per=3600, type=commands.BucketType.member)
async def lumber(ctx):
    guildid = str(ctx.guild.id)
    memberid = str(ctx.user.id)
    if not os.path.exists(f"{dirr}/World/{guildid}/Players/{memberid}"):
        os.mkdir(f"{dirr}/World/{guildid}/Players/{memberid}")
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "w+") as f:
            f.write(str(250))  # Starting currency number will be customizable.
            f.close()
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/name.txt", "w+") as f:
            f.write(ctx.user.name)
            f.close()
    if not os.path.exists(
            f"{dirr}/World/{guildid}/Players/{memberid}/inventory"):  # Creates inventory folder if it does not exist
        os.mkdir(f"{dirr}/World/{guildid}/Players/{memberid}/inventory")
    taxrate = float(readtax(f"{dirr}/World/{guildid}/taxrate.txt"))
    taxratepercent = round(taxrate * 100)
    resources, values = gettreevalues()  # will be replaced with something more complex.
    roll = random.randint(-25, 50)
    res = random.randint(0, len(resources) - 1)
    with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "r") as f:
        currency = f.read()
        f.close()
    if roll < 0:
        value = values[res]
        vaftertax = (round(float(value)) * round(float(roll)))
        fpay = round(vaftertax)
        totalcurr = str(round(float(currency) + fpay))
        streas = readtreasure(f"{dirr}/World/{guildid}/treasury.txt")
        with open(f"{dirr}/World/{guildid}/treasury.txt", "w+") as treas:
            treas.write(str(float(streas) + (fpay * -1)))
            treas.close()
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "w+") as f:
            f.write(totalcurr)
            f.close()
        await ctx.respond(
            f"While chopping a tree, a squirrel attacked you. Losses: {fpay}. Your current currency: {totalcurr}")
    else:
        resourcename = resources[res].replace(".txt", "")
        value = values[res]
        taxvalue = (round(float(value)) * round(float(roll))) * taxrate
        fpay = ((round(float(value)) * round(float(roll))) - taxvalue) * float(
            lumbermultiplier(f"{dirr}/World/{guildid}"))
        totalcurr = str(round((float(currency) + float(fpay))))
        streas = readtreasure(f"{dirr}/World/{guildid}/treasury.txt")
        with open(f"{dirr}/World/{guildid}/treasury.txt", "w+") as treas:
            treas.write(str(float(streas) + fpay))
            treas.close()
        with open(f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt", "w+") as f:
            f.write(totalcurr)
            f.close()
        if os.path.exists(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt"):
            with open(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt", "r") as f:
                line = f.readline()
                f.close()

            with open(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt", "w") as f:
                f.write(str(int(line) + roll))
                f.close()
        else:
            with open(f"{dirr}/World/{guildid}/inventory/{resourcename}.txt", "w+") as f:
                f.write(str(roll))
                f.close()

        await ctx.respond(
            f"You have chopped {roll} {resourcename}. You have earned {fpay} currency after tax, {round(float(value)) * round(float(roll))} before tax. Current tax rate is {taxratepercent}% and the current lumber multiplier is {float(lumbermultiplier(f'{dirr}/World/{guildid}'))}x. Your current currency: {totalcurr}")


@wb.command(description="Command for the Accountant to change the server tax rate.")
@has_role("Accountant")
async def taxrate(ctx):
    def is_auth(m):
        return m.author == ctx.author

    await ctx.respond("Please type the tax rate you would like. ie 42%")
    taxratemsg = await bot.wait_for('message', check=is_auth, timeout=300)
    tax = taxratemsg.content.replace("%", "")
    tax = int(tax) / 100
    guildid = str(ctx.guild.id)
    with open(f"{dirr}/World/{guildid}/taxrate.txt", "w+") as f:
        f.write(str(tax))
        f.close()
    await ctx.respond(f"Tax rate has been set to {taxratemsg.content}")



@wb.command(description="Command to get a list of upgrades.")
async def upgradelist(ctx):
    def is_auth(m):
        return m.author == ctx.author

    upg = listofupgrades(f'{dirr}/globals/', f'{dirr}/World/{str(ctx.guild.id)}')
    await ctx.respond(
        f"Here is your list of upgrades in tier {readtier(f'{dirr}/World/{str(ctx.guild.id)}')} \n \n" + '\n'.join(upg))



@wb.command(guild_ids=Support, description="Command to get upgrades")
@has_role("Design Lead")
async def upgradecreator(ctx):
    def is_auth(m):
        return m.author == ctx.author

    uname = Button(label="Upgrade Name", style=discord.ButtonStyle.primary)
    stats = Button(label="Stats", style=discord.ButtonStyle.primary)
    tier = Button(label="Tier", style=discord.ButtonStyle.primary)
    write = Button(label="Finish", style=discord.ButtonStyle.green)
    view = View()
    view.add_item(uname)
    view.add_item(stats)
    view.add_item(tier)
    view.add_item(write)

    await ctx.respond("Welcome to the upgrade maker!", view=view)

    async def upnamecallback(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("Type the name of this upgrade.")
            rval = await bot.wait_for('message', check=is_auth, timeout=300)
            uname.label = f"{rval.content}"
            await interaction.followup.send("Updated content:", view=view)

    async def statnamecallback(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(
                "Type the file name that this upgrade pertains to, and the multiplier, ie minemultiply 1.25. Only one "
                "stat should be changed with this upgrade.")
            cate = await bot.wait_for('message', check=is_auth, timeout=300)
            stats.label = f"{cate.content}"
            await interaction.followup.send("Updated content:", view=view)

    async def tiercallback(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(
                "What tier does this upgrade go in? Just type the number. ie, 2")
            tiername = await bot.wait_for('message', check=is_auth, timeout=300)
            tier.label = f"{tiername.content}"
            await interaction.followup.send("Updated content:", view=view)

    async def writecallback(interaction):
        if interaction.user == ctx.author:
            if os.path.exists(f"{dirr}/globals/upgrades/tier{str(tier.label)}"):
                os.chdir(f"{dirr}/globals/upgrades/tier{str(tier.label)}")
                try:
                    f = open(f"{uname.label}.txt", 'w+')
                    f.write(f"{stats.label} \n")
                    f.close()
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Upgrade {uname.label} has been created!")
                except:
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Something went wrong creating the upgrade {uname.label}.")
            else:
                os.mkdir(f"{dirr}/globals/upgrades/tier{str(tier.label)}")
                os.chdir(f"{dirr}/globals/upgrades/tier{str(tier.label)}")
                try:
                    f = open(f"{uname.label}.txt", 'w+')
                    f.write(f"{stats.label} \n")
                    f.close()
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Upgrade {uname.label} has been created!")
                except:
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Something went wrong creating the upgrade {uname.label}.")

    uname.callback = upnamecallback
    stats.callback = statnamecallback
    write.callback = writecallback
    tier.callback = tiercallback


@wb.command(description="Command to get upgrades")
async def purchaseupg(ctx):
    def is_auth(m):
        return m.author == ctx.author

    un, unn, upg = purchaseupgrade(f'{dirr}/globals/', f'{dirr}/World/{str(ctx.guild.id)}')
    await ctx.respond(
        f"Here is your list of upgrades in tier {readtier(f'{dirr}/World/{str(ctx.guild.id)}')}")
    await ctx.respond('\n'.join(upg))
    rname = await bot.wait_for('message', check=is_auth, timeout=300)
    rname = rname.content
    alreadyhave = whathaveupg(f'{dirr}/World/{str(ctx.guild.id)}/upgrades')
    if str(int(rname) - 1) in unn:
        if un[(int(rname) - 1)] + ".txt" in alreadyhave:
            await ctx.respond("Upgrade was already purchased.")
        else:
            await ctx.respond(f"Upgrade {un[(int(rname) - 1)]} has been purchased.")
            if not os.path.exists(f'{dirr}/World/{str(ctx.guild.id)}/upgrades'):
                os.mkdir(f'{dirr}/World/{str(ctx.guild.id)}/upgrades')
            os.chdir(f'{dirr}/World/{str(ctx.guild.id)}/upgrades')
            with open(f"{un[(int(rname) - 1)]}.txt", "w+") as f:
                f.close()
            with open(
                    f"{dirr}/globals/upgrades/tier{readtier(f'{dirr}/World/{str(ctx.guild.id)}')}/{un[(int(rname) - 1)]}.txt",
                    'r') as f:
                line = f.readline()
                line = line.split(" ")
                f.close()
            with open(f'{dirr}/World/{str(ctx.guild.id)}/{line[0]}.txt', "w+") as f:
                f.write(str(line[1]))
                f.close()



@wb.command(guild_ids=Support, description="Admin command to create resources.")
@has_role("Design Lead")
async def resourcecreator(ctx):
    def is_auth(m):
        return m.author == ctx.author

    resname = Button(label="Resource name", style=discord.ButtonStyle.primary)
    value = Button(label="Resource value", style=discord.ButtonStyle.primary)
    category = Button(label="Category", style=discord.ButtonStyle.primary)
    write = Button(label="Finish", style=discord.ButtonStyle.green)
    view = View()
    view.add_item(resname)
    view.add_item(value)
    view.add_item(category)
    view.add_item(write)
    await ctx.respond("Welcome to the resource creator.", view=view)

    async def resourcenamecallback(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("Type the name of the resource.")
            rname = await bot.wait_for('message', check=is_auth, timeout=300)
            resname.label = f"{rname.content}"
            await interaction.followup.send("Updated content:", view=view)

    async def valuecallback(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("Type the value of one of this resource.")
            rval = await bot.wait_for('message', check=is_auth, timeout=300)
            value.label = f"Value: {rval.content}"
            await interaction.followup.send("Updated content:", view=view)

    async def categorycallback(interaction):
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(
                "Enter the category(s) that you want this resource to be in. ie mine, wood, or none")
            cate = await bot.wait_for('message', check=is_auth, timeout=300)
            category.label = f"type: {cate.content}"
            await interaction.followup.send("Updated content:", view=view)

    async def writecallback(interaction):
        if interaction.user == ctx.author:
            if os.path.exists(f"{dirr}/globals/items"):
                os.chdir(f"{dirr}/globals/items")
                try:
                    f = open(f"{resname.label}.txt", 'w+')
                    f.write(f"{value.label} \n")
                    f.write(f"{category.label}")
                    f.close()
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Resource {resname.label} has been created!")
                except:
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Something went wrong creating the resource {resname.label}.")

    resname.callback = resourcenamecallback
    value.callback = valuecallback
    write.callback = writecallback
    category.callback = categorycallback


@wb.command(guild_ids=Support, description="Admin command to create Items.")
@has_role("Design Lead")
async def itemcreator(ctx):
    itemname = ""
    itemvalue = ""
    itemtype = ""

    def is_auth(m):
        return m.author == ctx.author

    resname = Button(label="Item name", style=discord.ButtonStyle.primary)
    value = Button(label="Item value", style=discord.ButtonStyle.primary)
    category = Button(label="Type", style=discord.ButtonStyle.primary)
    write = Button(label="Finish", style=discord.ButtonStyle.green)
    view = View()
    view.add_item(resname)
    view.add_item(value)
    view.add_item(category)
    view.add_item(write)
    await ctx.respond("Welcome to the Item creator.", view=view)

    async def resourcenamecallback(interaction):
        nonlocal itemname
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("Type the name of the Item.")
            rname = await bot.wait_for('message', check=is_auth, timeout=300)
            itemname = f"{rname.content}"
            await interaction.followup.send(f"Your Item's name is {itemname}", view=view)

    async def valuecallback(interaction):
        nonlocal itemvalue
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("Type the value of one of this Item.")
            rval = await bot.wait_for('message', check=is_auth, timeout=300)
            itemvalue = f"Value: {rval.content}"
            await interaction.followup.send(f"Your Item's value is {itemvalue}", view=view)

    async def categorycallback(interaction):
        nonlocal itemtype
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(
                "Enter the type you want this item to have. ie weapon, shield, armor, or none")
            cate = await bot.wait_for('message', check=is_auth, timeout=300)
            itemtype = f"type: {cate.content}"
            await interaction.followup.send(f"Your Item's type(s) is {itemtype}", view=view)

    async def writecallback(interaction):
        nonlocal itemname
        nonlocal itemvalue
        nonlocal itemtype
        if interaction.user == ctx.author:
            await interaction.response.edit_message(view=None)
            if os.path.exists(f"{dirr}/globals/items"):
                os.chdir(f"{dirr}/globals/items")
                try:
                    f = open(f"{itemname}.txt", 'w+')
                    f.write(f"{itemvalue} \n")
                    f.write(f"{itemtype} \n")
                    await interaction.followup.send(f"Is this item craftable? (y/n)")
                    iscraftable = await bot.wait_for('message', check=is_auth, timeout=300)
                    if iscraftable.content == "y":
                        await interaction.followup.send(f"What is the recipe? (Cloth,Iron,Stone) < Must match the "
                                                        f"case of the resource, Usually uppercase as shown.")
                        recipe = await bot.wait_for('message', check=is_auth, timeout=300)
                        recipe = recipe.content.replace(" ", "").lower()
                        recipe = "recipe: " + recipe
                        f.write(f"{recipe} \n")
                    if "weapon" in itemtype:
                        await interaction.followup.send(
                            f"How much damage will this item do? (this is a multiplier, usually over 1.0)")
                        dam = await bot.wait_for('message', check=is_auth, timeout=300)
                        damage = str(dam.content)
                        damage = "damage: " + damage
                        f.write(f"{damage}")
                        await interaction.followup.send(
                            f"Does this weapon have any special damage types? (poison, fire, freezing, explosive)")
                        eff = await bot.wait_for('message', check=is_auth, timeout=300)
                        effect = str(eff.content)
                        effect = "effect: " + effect
                        f.write(f"{effect}")
                    if "shield" in itemtype:
                        await interaction.followup.send(
                            f"How much defense does this item have? (this is a multiplier, usually over 1.0)")
                        defe = await bot.wait_for('message', check=is_auth, timeout=300)
                        defense = str(defe.content)
                        defense = "defense: " + defense
                        f.write(f"{defense}")
                    if "armor" in itemtype:
                        await interaction.followup.send(
                            f"How much defense does this item have? (this is a multiplier, usually over 1.0)")
                        defe = await bot.wait_for('message', check=is_auth, timeout=300)
                        defense = str(defe.content)
                        defense = "defense: " + defense
                        f.write(f"{defense}")

                    f.close()
                    await interaction.followup.send(
                        f"Item {itemname} has been created!")
                except:
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send(
                        f"Something went wrong creating the item {itemname}.")

    resname.callback = resourcenamecallback
    value.callback = valuecallback
    write.callback = writecallback
    category.callback = categorycallback


@wb.command(description="Command to list current server information.")
async def serverinfo(ctx):
    servstats = []
    os.chdir(f"{dirr}/World/{str(ctx.guild.id)}")
    playernum = os.listdir(os.getcwd() + "/Players")
    upgrades = os.listdir(os.getcwd() + "/upgrades")
    servstats.append("Number of players: " + str(len(playernum)))
    servstats.append("Number of upgrades: " + str(len(upgrades)))
    if os.path.exists("minemultiply.txt"):
        with open("minemultiply.txt", "r") as f:
            servstats.append(f"Mining Multiplier: {str(float(f.readline()))}x")
            f.close()
    if os.path.exists("lumbermultiply.txt"):
        with open("lumbermultiply.txt", "r") as f:
            servstats.append(f"Lumber Multiplier: {str(float(f.readline()))}x")
            f.close()
    if os.path.exists("taxrate.txt"):
        with open("taxrate.txt", "r") as f:
            servstats.append(f"Tax Rate: {(str(round(float(f.readline()) * 100)))}%")
            f.close()
    if os.path.exists("tier.txt"):
        with open("tier.txt", "r") as f:
            servstats.append("Server Tier: " + f.readline())
            f.close()
    if os.path.exists("treasury.txt"):
        with open("treasury.txt", "r") as f:
            servstats.append("Server treasury: " + f'{str(format(float(f.readline()), ","))}')
            f.close()
    await ctx.respond(f"**Server information for {ctx.guild.name}:** \n \n" + "\n".join(servstats))


@wb.command(description="Command to repair damaged weapons.")
async def repair(ctx):
    items = []
    durr = []
    idx = []
    allitems = []
    it = []

    def is_auth(m):
        return m.author == ctx.author

    if not os.path.exists(f"{dirr}/World/{str(ctx.guild.id)}/Players/{str(ctx.user.id)}/inventory"):
        os.mkdir(f"{dirr}/World/{str(ctx.guild.id)}/Players/{str(ctx.user.id)}/inventory")

    pitems = os.listdir(f"{dirr}/World/{str(ctx.guild.id)}/Players/{str(ctx.user.id)}/inventory")
    for a in pitems:
        with open(f"{dirr}/World/{str(ctx.guild.id)}/Players/{str(ctx.user.id)}/inventory/{a}", "r") as f:
            lines = f.readlines()
            durability = [i for i in lines if "durability" in i]
            if durability:
                dur = durability[0].split(" ")[1]
                if int(dur) < 100:
                    items.append(a.replace(".txt", ""))
                    durr.append(durability[0])

    if len(items) == 0:
        await ctx.respond("No repairable items.")
    else:

        for a, b in enumerate(items):
            idx.append(a)

            allitems.append(f"{b}")
            it.append(f"{a + 1} {b}")
        await ctx.respond(f"Which item would you like to repair?\n" + '\n'.join(it))
        itemselection = await bot.wait_for('message', check=is_auth, timeout=300)
        itemselection = itemselection.content
        if int(int(itemselection) - 1) in idx:
            with open(f"{dirr}/globals/items/{allitems[int(int(itemselection) - 1)]}.txt", "r") as item:
                lin = item.readlines()
            value = [i for i in lin if "Value" in i]
            if value:
                value = value[0].split(" ")[1]
                c = round((100 - int(durr[int(int(itemselection) - 1)].split(' ')[1])) / 100, 1)
                cost = int(value) * c
            else:
                cost = 100
            await ctx.respond(
                f"You chose {allitems[int(int(itemselection) - 1)]}, Current durability: {int(durr[int(int(itemselection) - 1)].split(' ')[1])} Cost to repair to full: {cost}. Do you want to repair? (y or n)")
            yorn = await bot.wait_for('message', check=is_auth, timeout=300)
            yorn = yorn.content
            if yorn == "y":
                with open(
                        f"{dirr}/World/{str(ctx.guild.id)}/Players/{str(ctx.user.id)}/inventory/{allitems[int(int(itemselection) - 1)]}.txt",
                        "r") as item:
                    lines = item.readlines()
                quantity = [i for i in lines if "quantity" in i]
                with open(
                        f"{dirr}/World/{str(ctx.guild.id)}/Players/{str(ctx.user.id)}/inventory/{allitems[int(int(itemselection) - 1)]}.txt",
                        "w") as item:
                    item.write(quantity[0])
                    item.write(f"durability: 100")

                await ctx.respond(
                    f"Item {allitems[int(int(itemselection) - 1)]} has been repaired for {cost}. Old Balance: {readwallet(str(ctx.guild.id), str(ctx.user.id))}, New Balance: {writewallet(str(ctx.guild.id), str(ctx.user.id), cost * -1)}")
            else:
                await ctx.respond(f"Item {allitems[int(int(itemselection) - 1)]} has not been repaired.")
        else:
            await ctx.respond(f"That selection is not in the list of repairable items.")


@wb.command(guild_ids=Support, description="Dungeon Crawler start command.")
async def dc(ctx):
    id = ctx.author.id
    await enterdungeon(ctx, bot, ctx.author, id)


@wb.command(guild_ids=Support)
@has_role("Design Lead")
async def classcreator(ctx):
    await createclass(ctx, bot)


@wb.command(guild_ids=Support)
@has_role("Design Lead")
async def enemycreator(ctx):
    await createenemy(ctx, bot)


@wb.command(guild_ids=Support)
@has_role("Design Lead")
async def dungeoncreator(ctx):
    await createdungeon(ctx, bot)


bot.run("OTM3NTQ2NTI3NDY1OTYzNTkw.YfdUPg.EIaW-h0t1qDZLr0nDgJgwJbXRa0")
