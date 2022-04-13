import sys

dirr = sys.path[0]


# Decision based AI, makes decisions based on certain scenarios
def isbleeding(weaponname, name):
    with open(f"{dirr}/globals/items/{weaponname}.txt", "r") as weapon:
        for a in weapon.readlines():
            if "bleeding" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    wb = True
                else:
                    wb = False
        weapon.close()
    with open(f"{dirr}/globals/enemies/{name}.txt", "r") as enemy:
        for a in enemy.readlines():
            if "bleedable" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    en = True
                else:
                    en = False
        enemy.close()
    if wb and en:
        return True
    else:
        return False


def isburning(weaponname, name):
    with open(f"{dirr}/globals/items/{weaponname}.txt", "r") as weapon:
        for a in weapon.readlines():
            if "burning" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    wb = True
                else:
                    wb = False
        weapon.close()
    with open(f"{dirr}/globals/enemies/{name}.txt", "r") as enemy:
        for a in enemy.readlines():
            if "burnable" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    en = True
                else:
                    en = False
        enemy.close()
    if wb and en:
        return True
    else:
        return False


def isfreezing(weaponname, name):
    with open(f"{dirr}/globals/items/{weaponname}.txt", "r") as weapon:
        for a in weapon.readlines():
            if "freezing" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    wb = True
                else:
                    wb = False
        weapon.close()
    with open(f"{dirr}/globals/enemies/{name}.txt", "r") as enemy:
        for a in enemy.readlines():
            if "freezable" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    en = True
                else:
                    en = False
        enemy.close()
    if wb and en:
        return True
    else:
        return False


def isexplodable(weaponname, name):
    with open(f"{dirr}/globals/items/{weaponname}.txt", "r") as weapon:
        for a in weapon.readlines():
            if "exploding" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    wb = True
                else:
                    wb = False
        weapon.close()
    with open(f"{dirr}/globals/enemies/{name}.txt", "r") as enemy:
        for a in enemy.readlines():
            if "explodable" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    en = True
                else:
                    en = False
        enemy.close()
    if wb and en:
        return True
    else:
        return False


def ispoisonable(weaponname, name):
    with open(f"{dirr}/globals/items/{weaponname}.txt", "r") as weapon:
        for a in weapon.readlines():
            if "poisoning" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    wb = True
                else:
                    wb = False
        weapon.close()
    with open(f"{dirr}/globals/enemies/{name}.txt", "r") as enemy:
        for a in enemy.readlines():
            if "poisonable" in a.replace("\n", ""):
                spl = a.replace("\n", "").split(" ")
                if "t" in spl[1]:
                    en = True
                else:
                    en = False
        enemy.close()
    if wb and en:
        return True
    else:
        return False
