import os
import sys

dirr = sys.path[0]


def readwallet(guildid, memberid):
    with open(
            f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt",
            "r") as item:
        money = item.readline()

    return money


def writewallet(guildid, memberid, change):
    with open(
            f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt",
            "r") as item:
        money = item.readline()

    with open(
            f"{dirr}/World/{guildid}/Players/{memberid}/wallet.txt",
            "w") as item:
        item.write(str(int(money) + int(change)))

    return str(int(money) + int(change))