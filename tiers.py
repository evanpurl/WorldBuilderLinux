# This file will contain everything having to do with tiers.
import os


def tier0(directory):
    with open(directory + "/tier.txt", "w+") as f:
        f.write(str(0))
        f.close()
    # Function creates the tiers file when the bot joins a server, and adds tier 0 to that file.


def readtier(directory):  # Function reads the tier of the server.
    with open(directory + "/tier.txt", "r") as f:
        line = f.readline()
        f.close()
        return line


def uptier(directory, serverdir):
    # Function that ups the tier of the server. Will have requirements to go up in tier. ie cost
    # of server currency, materials, etc.
    # Max tier would be 4 for now. Just to test everything. More tiers could be made later.
    maxtier = os.listdir(directory + "/globals/upgrades")
    with open(serverdir + "/tier.txt", "r") as f:
        line = f.readline()
        f.close()

    newtier = int(line) + 1
    if newtier >= len(maxtier):
        print("Cannot upgrade your tier further!")
        return f"Tier is {line}."
    else:
        with open(serverdir + "/tier.txt", "w+") as f:
            f.write(str(newtier))
            f.close()
        return f"New tier is {newtier}."

# print(uptier("C:/Users/evan/PycharmProjects/WorldBuilder", "C:/Users/evan/PycharmProjects/WorldBuilder/World/904120920862519396"))
