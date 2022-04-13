import os
from tiers import readtier


def upgradelist(directory, serverdir):
    upgrades = []
    tierdir = directory + f"/upgrades/tier{readtier(serverdir)}"
    listupgrades = os.listdir(tierdir)
    alreadyhave = whathaveupg(serverdir+ "/upgrades")
    for a in listupgrades:
        if a in alreadyhave:  # Files with -Done in the name (The file name would be changed when someone buys an
            pass
        else:
            upgrades.append(a.replace(".txt", ""))

    return upgrades


def whathaveupg(directory):
    if os.path.exists(directory):
        listupgrades = os.listdir(directory)
    else:
        os.mkdir(directory)
        listupgrades = os.listdir(directory)
    return listupgrades


def purchaseupgrade(directory, serverdir):
    un = []
    unn = []
    upgrade = []
    tierdir = directory + f"/upgrades/tier{readtier(serverdir)}"
    listupgrades = os.listdir(tierdir)
    alreadyhave = whathaveupg(serverdir + "/upgrades")
    for a, b in enumerate(listupgrades):
        if b in alreadyhave:
            un.append(f"{b.replace('.txt', '')}")
            unn.append(f"{a}")
            upgrade.append(f"{a + 1} {b.replace('.txt', '')} Purchased")
        else:
            un.append(f"{b.replace('.txt', '')}")
            unn.append(f"{a}")
            upgrade.append(f"{a + 1} {b.replace('.txt', '')}")
    return un, unn, upgrade



