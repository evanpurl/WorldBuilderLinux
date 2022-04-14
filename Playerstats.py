import os
import sys

dirr = sys.path[0]


class Player:
    def __init__(self, guildid, memberid):
        if not os.path.exists(f"{dirr}/World/{guildid}/Players/{memberid}"):
            os.mkdir(f"{dirr}/World/{guildid}/Players/{memberid}")
            os.mkdir(f"{dirr}/World/{guildid}/Players/{memberid}/inventory")

        self.health = 0
        self.level = 0
        self.xp = 0
        self.mana = 0
        self.maxmana = 100
        self.name = None
        self.damage = 0
        self.defmode = None
        self.defense = 0
        self.weapon = None
        self.shield = None
        self.armor = None
        self.guildid = guildid
        self.memberid = memberid
        self.itemlist = None
        self.inv = None

    def gethealth(self):
        if os.path.exists(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/health.txt"):
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/health.txt", "r") as health:
                h = health.readline()
                self.health = int(h)
            return self.health
        else:
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/health.txt", "w+") as health:
                self.health = 100
                health.write(str(100))
                health.close()
            return self.health

    def sethealth(self, health):
        self.health += int(health)
        return self.health

    def getmana(self):
        if os.path.exists(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/mana.txt"):
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/mana.txt", "r") as mana:
                h = mana.readline()
                self.mana = int(h)
                mana.close()
            return self.mana
        else:
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/mana.txt", "w+") as mana:
                self.mana = 100
                mana.write(str(100))
                mana.close()
            return self.mana

    def getname(self):
        with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/name.txt", "r") as name:
            n = name.readline()
            self.name = int(n)
            name.close()
        return self.name

    def getdamage(self):  # Updated 3/23/2022
        if os.path.exists(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/damage.txt"):
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/damage.txt", "r") as damage:
                dam = float(damage.readline())
        else:
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/damage.txt", "w+") as damage:
                damage.write(str(5))
            dam = 5
        return dam

    def getweapondamage(self, item):
        if item != None:
            with open(f"{dirr}/globals/items/{item}.txt", "r") as weapon:
                lines = weapon.readlines()
                damageline = [i for i in lines if "damage" in i]
                if damageline:
                    defe = float(damageline[0].split()[1])
            return defe
        else:
            return 0.0

    def getdefense(self):  # Updated 3/23/2022
        if os.path.exists(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/defense.txt"):
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/defense.txt", "r") as defense:
                defe = float(defense.readline())
        else:
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/defense.txt", "w+") as defense:
                defense.write(str(4))
            defe = 4
        return defe

    def getshielddef(self, shield):
        if shield is not None:
            with open(f"{dirr}/globals/items/{shield}.txt", "r") as shield:
                lines = shield.readlines()
                defenseline = [i for i in lines if "defense" in i]
                if defenseline:
                    defe = float(defenseline[0].split()[1])
            return defe
        else:
            return 0.0

    def getarmordef(self, armor):
        if armor != None:
            with open(f"{dirr}/globals/items/{armor}.txt", "r") as armorr:
                lines = armorr.readlines()
                defenseline = [i for i in lines if "defense" in i]
                if defenseline:
                    defe = float(defenseline[0].split()[1])
            return defe
        else:
            return 0.0

    def getitems(self, itemtype):
        itemlists = os.listdir(f"{dirr}/globals/items")
        itemlist = []
        os.chdir(f"{dirr}/globals/items")
        items = os.listdir(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory")
        for a in items:
            with open(a, "r") as f:
                lines = f.readlines()
                types = [i for i in lines if itemtype in i]
                if types:
                    itemlist.append(a.replace(".txt", ""))
        self.itemlist = itemlist
        return self.itemlist

    def addtoinv(self, itemname):
        pitems = os.listdir(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory")
        if itemname + '.txt' in pitems:
            with open(f"{dirr}/globals/items/{itemname}.txt", "r") as pitem:
                lines = pitem.readlines()
                weapon = [i for i in lines if 'weapon' in i]
                shield = [i for i in lines if 'shield' in i]
                armor = [i for i in lines if 'armor' in i]
                if weapon:
                    pass
                elif shield:
                    pass
                elif armor:
                    pass
                else:
                    with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt",
                              "r") as f:
                        lines = f.readlines()
                        amount = [i for i in lines if 'quantity' in i]
                        durability = [i for i in lines if 'durability' in i]
                    with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt",
                              "w") as f:
                        f.write(f"quantity: {str(int(amount[0].split(' ')[1]) + 1)}")
                        if durability:
                            f.write(f"\n{str(durability[0])}")
            pitem.close()
        else:
            with open(f"{dirr}/globals/items/{itemname}.txt", "r") as pitem:
                lines = pitem.readlines()
                weapon = [i for i in lines if 'weapon' in i]
                shield = [i for i in lines if 'shield' in i]
                armor = [i for i in lines if 'armor' in i]
            with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt", "w") as f:
                f.write(f"quantity: {str(1)}")
                if weapon:
                    f.write("\ndurability: 100")
                if shield:
                    f.write("\ndurability: 100")
                if armor:
                    f.write("\ndurability: 100")

    def remfrominv(self, itemname):
        itemname = itemname.replace(' \n', '')
        with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt",
                  "r") as f:
            amount = f.readlines()
        with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt",
                  "w") as f:
            f.write(f"quantity: {str(int(amount[0].split(' ')[1]) - 1)}")
            if len(amount) > 1:
                f.write("\n" + amount[1])
        with open(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt",
                  "r") as f:
            amount = f.readlines()
        if int(amount[0].split(" ")[1]) <= 0:
            os.remove(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory/{itemname}.txt")

    def totalinv(self):
        inv = []
        os.chdir(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory")
        items = os.listdir(os.getcwd())
        for a in items:
            with open(a, "r") as f:
                inv.append(f"{f.readline().split(' ')[1]} {a.replace('.txt', '')}")
        self.inv = inv
        return self.inv

    def craft(self, craftitem):
        rem = []
        itemfile = craftitem + ".txt"
        os.chdir(f"{dirr}/globals/items")
        if os.path.exists(f"{dirr}/globals/items/{itemfile}"):
            if itemfile in os.listdir(f"{dirr}/World/{self.guildid}/Players/{self.memberid}/inventory"):
                with open(itemfile, "r") as f:
                    lines = f.readlines()
                    try:
                        weapon = [i for i in lines if 'weapon' in i]
                        shield = [i for i in lines if 'shield' in i]
                        armor = [i for i in lines if 'armor' in i]
                        if weapon:
                            return f"You already have the weapon {craftitem} in your inventory!"
                        elif shield:
                            return f"You already have the shield {craftitem} in your inventory!"
                        elif armor:
                            return f"You already have the armor {craftitem} in your inventory!"
                        else:
                            recipe = [i for i in lines if 'recipe' in i]
                            if recipe:
                                r = recipe[0].split(": ")[1].split(",")
                                for a in r:
                                    self.remfrominv(a)
                                    rem.append(a)
                                self.addtoinv(craftitem)
                                return f"{craftitem} has been crafted using {', '.join(r)}"
                            else:
                                return f"{craftitem} cannot be crafted."

                    except FileNotFoundError:
                        for a in rem:
                            self.addtoinv(a)
                        return f"{craftitem} can not be crafted, missing crafting item!"
            else:
                with open(itemfile, "r") as f:
                    lines = f.readlines()
                    try:
                        recipe = [i for i in lines if 'recipe' in i]
                        if recipe:
                            r = recipe[0].split(": ")[1].split(",")
                            for a in r:
                                self.remfrominv(a)
                                rem.append(a)
                            self.addtoinv(craftitem)
                            return f"{craftitem} has been crafted using {', '.join(r)}."
                        else:
                            return f"{craftitem} cannot be crafted."

                    except FileNotFoundError:
                        for a in rem:
                            self.addtoinv(a)
                        return f"{craftitem} can not be crafted, missing crafting item!"
        else:
            return f"{craftitem} does not exist!"

    def getlevel(self):
        if not os.path.exists(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/level.txt"):
            with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/level.txt", "w+") as level:
                level.write(str(1))
                return 1
        else:
            with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/level.txt", "r") as level:
                l = level.readline()
                return l

    def getxp(self):
        if not os.path.exists(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/xp.txt"):
            with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/xp.txt", "w+") as level:
                level.write(str(0))
                return 0
        else:
            with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/xp.txt", "r") as level:
                l = level.readline()
                return l

    def setxp(self, xp):
        with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/xp.txt", "w+") as level:
            level.write(str(xp))

    def levelup(self):
        with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/level.txt", "r") as level:
            l = level.readline()
        with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/xp.txt", "w+") as xp:
            xp.write(str(0))
        with open(f"{dirr}/World/{str(self.guildid)}/Players/{str(self.memberid)}/level.txt", "w+") as level:
            lev = str(int(l) + 1)
            level.write(lev)
        return lev


class Enemy:
    def __init__(self, unitname):
        self.health = 0
        self.name = unitname
        self.damage = None
        self.defense = None
        self.defmode = None

    def getname(self):
        return self.name

    def gethealth(self):
        with open(f"{dirr}/globals/enemies/{self.name}.txt", "r") as enemyh:
            lines = enemyh.readlines()
            for a in lines:
                if "health" in a:
                    self.health = int(a.split(" ")[1])
        return self.health

    def sethealth(self, healthh):
        self.health += int(healthh)
        return self.health

    def getdamage(self):
        with open(f"{dirr}/globals/enemies/{self.name}.txt", "r") as enemyd:
            lines = enemyd.readlines()
            for a in lines:
                if "damage" in a:
                    self.damage = a.split(" ")[1]
        enemyd.close()
        return self.damage

    def getdefense(self):
        with open(f"{dirr}/globals/enemies/{self.name}.txt", "r") as enemyd:
            lines = enemyd.readlines()
            for a in lines:
                if "defense" in a:
                    self.defense = a.split(" ")[1]
        enemyd.close()
        return self.defense
