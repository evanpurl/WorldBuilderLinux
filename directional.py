import os, sys, random
from Playerstats import Player, Enemy
import discord
from discord.ui import Button, View
from gendungeon import dunrooms
from AI import enemymove

dirr = sys.path[0]


async def enterdungeon(ctx, bot, user, id):
    def is_auth(m):
        return m.author == ctx.author

    enemylist = None
    enemyclass = None
    guildid = str(ctx.guild.id)
    maxrooms = random.randint(10, 25)
    llword = ["dark", "dimly lit", "moderately lit", "well lit", "bright"]
    enter = Button(label="Enter", style=discord.ButtonStyle.primary)
    turnback = Button(label="Turn Back", style=discord.ButtonStyle.danger)
    lhand = Button(label="Left Hand", style=discord.ButtonStyle.primary)
    rhand = Button(label="Right Hand", style=discord.ButtonStyle.primary)
    armor = Button(label="Armor", style=discord.ButtonStyle.primary)
    finish = Button(label="Finish", style=discord.ButtonStyle.primary)
    view = View()
    equip = View()
    equip.add_item(lhand)
    equip.add_item(rhand)
    equip.add_item(armor)
    equip.add_item(finish)
    view.add_item(enter)
    view.add_item(turnback)

    player = Player(guildid, str(id))

    await user.send("Equip yourself before entering the dungeon!", view=equip)
    await ctx.respond("Message Sent")

    async def lhandcallback(interaction):  # Shield Arm
        await interaction.response.edit_message(view=None)
        slist = []
        lhandshield = player.getitems("shield")
        if not lhandshield:
            lhand.label = "None"
            await user.send("Updated: ", view=equip)
        else:
            for a, b in enumerate(lhandshield):
                slist.append(f"{a + 1} {b}")
            await user.send('\n'.join(slist))
            await user.send("Please select which Shield you want, ie '1, 2, 3, 4' etc. Enter 0 to have no shield.")
            msg = await bot.wait_for('message', check=is_auth, timeout=300)
            s = msg.content
            if s == 0:
                lhand.label = "None"
            else:
                try:
                    s = int(s)
                    try:
                        weapon = lhandshield[s - 1]
                        player.shield = weapon
                        lhand.label = weapon
                        await user.send("Updated: ", view=equip)
                    except IndexError:
                        await user.send("That number is not available, try again.", view=equip)
                except ValueError:
                    await user.send("Input is not a number, please try again.", view=equip)

    async def rhandcallback(interaction):  # Weapon Arm
        await interaction.response.edit_message(view=None)
        wlist = []
        rhandweapon = player.getitems("weapon")
        if not rhandweapon:
            rhand.label = "None"
            await user.send("Updated: ", view=equip)
        else:
            for a, b in enumerate(rhandweapon):
                wlist.append(f"{a + 1} {b}")
            await user.send('\n'.join(wlist))
            await user.send("Please select which Weapon you want, ie '1, 2, 3, 4' etc. Enter 0 to have no weapon.")
            msgr = await bot.wait_for('message', check=is_auth, timeout=300)
            w = msgr.content
            if w == 0:
                rhand.label = "None"
            else:
                try:
                    w = int(w)
                    try:
                        weapon = rhandweapon[w - 1]
                        player.weapon = weapon
                        rhand.label = weapon
                        await user.send("Updated: ", view=equip)
                    except IndexError:
                        await user.send("That number is not available, try again.", view=equip)
                except ValueError:
                    await user.send("Input is not a number, please try again.", view=equip)

    async def armorcallback(interaction):  # Armor
        await interaction.response.edit_message(view=None)
        wlist = []
        armorr = player.getitems("armor")
        if not armorr:
            armor.label = "None"
            await user.send("Updated: ", view=equip)
        else:
            for a, b in enumerate(armorr):
                wlist.append(f"{a + 1} {b}")
            await user.send('\n'.join(wlist))
            await user.send("Please select which Armor Set you want, ie '1, 2, 3, 4' etc. Enter 0 to have no Armor.")
            msg = await bot.wait_for('message', check=is_auth, timeout=300)
            ar = msg.content
            if ar == 0:
                armor.label = "None"
            else:
                try:
                    ar = int(ar)
                    try:
                        weapon = armorr[ar - 1]
                        player.armor = weapon
                        armor.label = weapon
                        await user.send("Updated: ", view=equip)
                    except IndexError:
                        await user.send("That number is not available, try again.", view=equip)
                except ValueError:
                    await user.send("Input is not a number, please try again.", view=equip)

    async def finishcallback(interaction):  # Finish Button
        await interaction.response.edit_message(view=None)

        player.health = player.gethealth()
        player.xp = int(player.getxp())
        player.mana = player.getmana()
        player.level = player.getlevel()
        if player.getweapondamage(player.weapon) == 0:
            player.damage = player.getdamage()
        else:
            player.damage = player.getdamage() * player.getweapondamage(player.weapon)
        if player.getarmordef(player.armor) + player.getshielddef(player.shield) == 0:
            player.defense = player.getdefense()
        else:
            player.defense = player.getdefense() * (
                    player.getarmordef(player.armor) + player.getshielddef(player.shield))
        await user.send(
            f"**Level: {player.level} Health: {player.health} \n Mana: {player.mana} \n Weapon: {player.weapon} \n Damage: {player.damage} \n Shield: {player.shield} \n Defense: {player.defense} \n Armor Set: {player.armor}**")
        w = os.listdir(f"{dirr}/globals/dungeons/")
        r = random.randint(0, len(w) - 1)
        light = 0
        enemies = []

        inventory = player.totalinv()

        async def entercallback(interaction):
            await user.send(f"Choosing to enter, you make your way into the {dname}.", view=move)
            await interaction.response.edit_message(view=None)

        async def tbcallback(interaction):
            await user.send(f"You have turned back, ending Dungeon Crawler.")
            await interaction.response.edit_message(view=None)  # End of code

        with open(f"{dirr}/globals/dungeons/{w[r]}", "r") as f:
            dname = w[r].replace(".txt", "")
            lines = f.readlines()
            light = lines[0].replace("ll: ", "")
            enemies = lines[1].replace("enemies: ", "").replace("\n", "").split(",")
        nonlocal enemylist
        enemylist = enemies

        d1embed = discord.Embed(title="Dungeon Type: " + dname)
        embed = discord.Embed(
            title=f"You have come to the entrance of the {llword[int(light)]} {dname}, what would you like to do? 'Turn back' or 'Enter'?")
        embed.add_field(name="Light Level", value=light)
        embed.add_field(name="Enemies", value=str(enemies)[1:-1])
        await user.send("Welcome to Dungeon Crawler.", embed=d1embed)

        await user.send(embed=embed, view=view)

        enter.callback = entercallback
        turnback.callback = tbcallback

    lhand.callback = lhandcallback
    rhand.callback = rhandcallback
    armor.callback = armorcallback
    finish.callback = finishcallback

    left, front, right = dunrooms(maxrooms)  # Generated dungeon

    # Combat Section

    attack = Button(label=f"Attack", style=discord.ButtonStyle.primary)
    defend = Button(label=f"Defend", style=discord.ButtonStyle.green)
    heal = Button(label=f"Heal", style=discord.ButtonStyle.gray)
    retreat = Button(label="Retreat", style=discord.ButtonStyle.danger)

    combat = View()
    combat.add_item(attack)
    combat.add_item(defend)
    combat.add_item(heal)
    combat.add_item(retreat)

    async def attackcallback(interaction):
        nonlocal enemyclass
        await interaction.response.edit_message(view=None)
        if player.defmode is not None:
            player.defmode == None
            player.defense = player.defense / 2
        if player.mana < 5:
            await user.send(f"Not enough Mana. Go into defensive mode to regenerate.")
        else:
            damage = int(player.getdamage()) - (int(enemyclass.getdefense()) / 4)
            if damage <= 0:
                await user.send(f"You did no damage!")
            else:
                player.mana -= 5
                enemyclass.health -= damage
            await user.send(f"You attacked the {enemyclass.getname()}! **Their health: {enemyclass.health}**")  #
        if enemyclass.health <= 0:
            player.health = 100
            player.mana = 100
            xpgained = float(enemyclass.gethealth()) / 4
            await user.send(f"You have won the battle! **XP Gained: {xpgained}** where will you go next?", view=move)
            player.xp += xpgained

            if player.xp >= 100:
                player.levelup()
                await user.send(f"You have leveled up! **Level: {player.getlevel()}**")
            else:
                player.setxp(player.xp)

        else:
            enmove = enemymove(player.defmode)
            await user.send(f"The {enemyclass.getname()} will {enmove}!")
            if enmove == "attack":
                enemyclass.defmode == None
                damage = (int(enemyclass.getdamage()) - (int(player.defense) / 2))
                if damage <= 0:
                    await user.send(f"The {enemyclass.getname()} did no damage!", view=combat)
                else:
                    player.sethealth((damage * -1))
                    if player.health <= 0:
                        await user.send("You have perished in the heat of battle. Ending Dungeon Crawler.")
                        return
                    else:
                        await user.send(
                            f"The {enemyclass.getname()} did {damage} damage! **Your health: {player.health}**",
                            view=combat)
            else:
                await user.send(f"The {enemyclass.getname()} has went into defense mode, raising their defense!",
                                view=combat)
                enemyclass.defmode == True

    async def defensecallback(interaction):
        await interaction.response.edit_message(view=None)
        if player.defmode == None:
            player.defmode = True
            player.defense = player.defense * 2
        if player.mana < player.maxmana:
            player.mana += 25
            if player.mana > 100:
                player.mana = 100
            await user.send(f"Defense raised, some mana has been regenerated! **Mana: {player.mana}**")
        else:
            await user.send(f"Defense raised!", view=combat)
        enmove = enemymove(player.defmode)
        await user.send(f"The {enemyclass.getname()} will {enmove}!")
        if enmove == "attack":
            enemyclass.defmode == None
            damage = (int(enemyclass.getdamage()) - (int(player.defense) / 2))
            if damage <= 0:
                await user.send(f"The {enemyclass.getname()} did no damage!", view=combat)
            else:
                player.sethealth((damage * -1))
                if player.health <= 0:
                    await user.send("You have perished in the heat of battle. Ending Dungeon Crawler.")
                    return
                else:
                    await user.send(f"The {enemyclass.getname()} did {damage} damage! **Your health: {player.health}**",
                                    view=combat)
        else:
            await user.send(f"The {enemyclass.getname()} has went into defense mode, raising their defense!",
                            view=combat)
            enemyclass.defmode == True

    async def healcallback(interaction):
        await interaction.response.edit_message(view=None)
        if player.mana < 20:
            await user.send("Not enough Mana to heal. Go into defensive mode to regenerate some of your Mana!.",
                            view=combat)
        else:
            if player.health < 100:
                player.health += 20
                player.mana -= 20
                if player.health > 100:
                    player.health = 100
                await user.send(f"You have healed some of your wounds. **Health: {player.health} Mana: {player.mana}**",
                                view=combat)
            else:
                await user.send("Your health is already full!", view=combat)

    async def retreatcallback(interaction):
        nonlocal room
        room -= 1
        await interaction.response.edit_message(view=None)
        await user.send(f"**Room: {room + 1}** \n You have retreated from combat. Where do you want to go next?",
                        view=move)

    retreat.callback = retreatcallback
    attack.callback = attackcallback
    defend.callback = defensecallback
    heal.callback = healcallback

    # End of combat section

    # Chest Section

    openc = Button(label=f"Open Chest", style=discord.ButtonStyle.primary)
    moveback = Button(label=f"Leave and move on", style=discord.ButtonStyle.green)

    chest = View()
    chest.add_item(openc)
    chest.add_item(moveback)

    async def chestopen(interaction):
        await interaction.response.edit_message(view=None)
        await user.send("Move along! Area under construction. :)", view=move)

    async def leavechest(interaction):
        await interaction.response.edit_message(view=None)
        await user.send("Why didn't you open it?? Anyway, move along! Area under construction. :)", view=move)

    openc.callback = chestopen
    moveback.callback = leavechest

    # End of chest section

    # Game Section

    room = 0  # first room

    leftbtn = Button(label=f"Left", style=discord.ButtonStyle.primary)
    rightbtn = Button(label=f"Right", style=discord.ButtonStyle.green)
    frontbtn = Button(label=f"Forward", style=discord.ButtonStyle.gray)

    move = View()
    move.add_item(leftbtn)
    move.add_item(frontbtn)
    move.add_item(rightbtn)

    async def leftcallback(interaction):
        await interaction.response.edit_message(view=None)
        nonlocal room
        nonlocal maxrooms
        nonlocal enemyclass
        room += 1
        if room == maxrooms:
            await user.send("Boss fight room would be here. Here's a cookie for finishing this! 🍪")
            return
        if left[room] == "enemy":
            enemyclass = Enemy(enemylist[random.randint(0, len(enemylist) - 1)])
            enemyclass.gethealth()
            enemyclass.getdamage()
            enemyclass.getdefense()
            await user.send(
                f"**Room: {room + 1}** \n You went Left, Encountering a {enemyclass.getname()}, Health: {enemyclass.gethealth()}, Damage: {enemyclass.getdamage()}, Defense: {enemyclass.getdefense()}, prepare to fight.",
                view=combat)
        if left[room] == "room":
            await user.send(f"**Room: {room + 1}** \n You went Left, What is your next move?", view=move)
        if left[room] == "room item":
            await user.send(
                f"**Room: {room + 1}** \n You went Left, a locked chest is in front of you, what will you do?",
                view=chest)

    async def rightcallback(interaction):
        await interaction.response.edit_message(view=None)
        nonlocal room
        nonlocal maxrooms
        nonlocal enemyclass
        room += 1
        if room == maxrooms:
            await user.send("Boss fight room would be here. Here's a cookie for finishing this! 🍪")
            return

        if right[room] == "enemy":
            enemyclass = Enemy(enemylist[random.randint(0, len(enemylist) - 1)])
            enemyclass.gethealth()
            enemyclass.getdamage()
            enemyclass.getdefense()
            await user.send(
                f"**Room: {room + 1}** \n You went Left, Encountering a {enemyclass.getname()}, Health: {enemyclass.gethealth()}, Damage: {enemyclass.getdamage()}, Defense: {enemyclass.getdefense()}, prepare to fight.",
                view=combat)
        if right[room] == "room":
            await user.send(f"**Room: {room + 1}** \n You went Right, What is your next move?", view=move)
        if right[room] == "room item":
            await user.send(
                f"**Room: {room + 1}** \n You went Right, a locked chest is in front of you, what will you do?",
                view=chest)

    async def frontcallback(interaction):
        await interaction.response.edit_message(view=None)
        nonlocal room
        nonlocal maxrooms
        nonlocal enemyclass
        room += 1
        if room == maxrooms:
            await user.send("Boss fight room would be here. Here's a cookie for finishing this! 🍪")
            return
        if front[room] == "enemy":
            enemyclass = Enemy(enemylist[random.randint(0, len(enemylist) - 1)])
            enemyclass.gethealth()
            enemyclass.getdamage()
            enemyclass.getdefense()
            await user.send(
                f"**Room: {room + 1}** \n You went Left, Encountering a {enemyclass.getname()}, Health: {enemyclass.gethealth()}, Damage: {enemyclass.getdamage()}, Defense: {enemyclass.getdefense()}, prepare to fight.",
                view=combat)
        if front[room] == "room":
            await user.send(f"**Room: {room + 1}** \n You went Forward, What is your next move?", view=move)
        if front[room] == "room item":
            await user.send(f"**Room: {room + 1}** \n You went Forward, a locked chest is in front of you, what will "
                            f"you do?", view=chest)

    leftbtn.callback = leftcallback
    rightbtn.callback = rightcallback
    frontbtn.callback = frontcallback
