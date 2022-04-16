import os
import sys
import discord
from discord.ui import Button, View


async def createclass(ctx, bot):
    dirr = sys.path[0]

    def is_auth(m):
        return m.author == ctx.author

    classname = Button(label="Class Name", style=discord.ButtonStyle.primary)

    clasname = View()
    clasname.add_item(classname)

    await ctx.respond("Welcome to the class creator! You will be asked a series of questions to create your class.",
                      view=clasname)

    async def classnamecallback(interaction):
        c = []
        await interaction.response.edit_message(view=None)
        await ctx.respond("What is the class' name?")

        cname = await bot.wait_for('message', check=is_auth, timeout=300)
        cname = cname.content

        await ctx.respond(f"The name you chose is {cname}")
        await ctx.respond("Does this class boost the player's health?")
        hyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if hyorn.content.lower() == "y":
            await ctx.respond("How much would the player's health increase by?")
            health = await bot.wait_for('message', check=is_auth, timeout=300)
            health = health.content
            c.append(f'health: {health}')
        await ctx.respond("Does this class boost the player's damage?")
        dyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if dyorn.content.lower() == "y":
            await ctx.respond("How much would the player's damage increase by?")
            damage = await bot.wait_for('message', check=is_auth, timeout=300)
            damage = damage.content
            c.append(f'damage: {damage}')
        await ctx.respond("Does this class boost the player's defense?")
        deyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if deyorn.content.lower() == "y":
            await ctx.respond("How much would the player's defense increase by?")
            defense = await bot.wait_for('message', check=is_auth, timeout=300)
            defense = defense.content
            c.append(f'defense: {defense}')
        await ctx.respond("Does this class contain magic?")
        deyorn = await bot.wait_for('message', check=is_auth, timeout=300)
        if deyorn.content.lower() == "y":
            magic = "magic"
            c.append(magic)
        if not os.path.exists(f"{dirr}/globals/classes/"):
            os.mkdir(f"{dirr}/globals/classes/")
        with open(f"{dirr}/globals/classes/{cname}.txt", "w+") as cl:
            for a in c:
                cl.write(a + '\n')

        await ctx.respond(f"Class with the name {cname} has been created!")

    classname.callback = classnamecallback


async def createenemy(ctx, bot):
    dirr = sys.path[0]

    def is_auth(m):
        return m.author == ctx.author

    ename = Button(label="Enemy Name", style=discord.ButtonStyle.primary)

    enemy = View()
    enemy.add_item(ename)

    await ctx.respond("Welcome to the enemy creator! Follow the prompt to create your enemy.",
                      view=enemy)

    async def enemynamecallback(interaction):
        c = []
        await interaction.response.edit_message(view=None)
        await ctx.respond("What is the enemy's name?")

        cname = await bot.wait_for('message', check=is_auth, timeout=300)
        cname = cname.content

        await ctx.respond(f"The name you chose is {cname}")
        await ctx.respond("How much health does this enemy have?")
        health = await bot.wait_for('message', check=is_auth, timeout=300)
        health = health.content
        c.append(f'health: {health}')
        await ctx.respond(f'health: {health}')
        await ctx.respond("How much damage would this enemy do?")
        damage = await bot.wait_for('message', check=is_auth, timeout=300)
        damage = damage.content
        c.append(f'damage: {damage}')
        await ctx.respond(f'damage: {damage}')
        await ctx.respond("How much defense does this enemy have?")
        defense = await bot.wait_for('message', check=is_auth, timeout=300)
        defense = defense.content
        c.append(f'defense: {defense}')
        await ctx.respond(f'defense: {defense}')
        if not os.path.exists(f"{dirr}/globals/enemies/"):
            os.mkdir(f"{dirr}/globals/enemies/")
        with open(f"{dirr}/globals/enemies/{cname}.txt", "w+") as cl:
            for a in c:
                cl.write(a + '\n')

        await ctx.respond(f"Enemy with the name {cname} has been created!")

    ename.callback = enemynamecallback


async def createdungeon(ctx, bot):
    dirr = sys.path[0]

    def is_auth(m):
        return m.author == ctx.author

    dname = Button(label="Dungeon Name", style=discord.ButtonStyle.primary)

    enemy = View()
    enemy.add_item(dname)

    await ctx.respond("Welcome to the dungeon creator! Follow the prompt to create your dungeon.",
                      view=enemy)

    async def dungeonnamecallback(interaction):
        c = []
        await interaction.response.edit_message(view=None)
        await ctx.respond("What is this dungeon called?")

        cname = await bot.wait_for('message', check=is_auth, timeout=300)
        cname = cname.content

        await ctx.respond(f"The name you chose is {cname}")
        await ctx.respond("What light level does this dungeon have?")
        health = await bot.wait_for('message', check=is_auth, timeout=300)
        health = health.content
        c.append(f'll: {health}')
        await ctx.respond(f'Light Level: {health}')
        await ctx.respond("What enemies are present in this dungeon? Separate each by commas. ie snake,skeleton,skeleton archer")
        damage = await bot.wait_for('message', check=is_auth, timeout=300)
        damage = damage.content.replace(" ,", "").replace(", ", "")
        c.append(f'enemies: {damage}')
        await ctx.respond(f'enemies: {damage}')
        await ctx.respond("What boss is in this dungeon? Check discord for boss list.")
        damage = await bot.wait_for('message', check=is_auth, timeout=300)
        await ctx.respond(f"Boss: {damage.content}")
        c.append(f"boss: {damage.content}")
        if not os.path.exists(f"{dirr}/globals/dungeons/"):
            os.mkdir(f"{dirr}/globals/dungeons/")
        with open(f"{dirr}/globals/dungeons/{cname}.txt", "w+") as cl:
            for a in c:
                cl.write(a + '\n')

        await ctx.respond(f"Dungeon with the name {cname} has been created!")

    dname.callback = dungeonnamecallback
