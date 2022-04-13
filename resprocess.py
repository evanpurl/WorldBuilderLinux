import sys
import os

dirr = sys.path[0]


def mineprocess():
    os.chdir(f"{dirr}/globals/items")
    res = os.listdir(os.getcwd())
    resourcenames = []
    for a in res:
        f = open(a, "r")
        lines = f.readlines()
        resource = [i for i in lines if 'mine' in i]
        if resource:
            resourcenames.append(a)
    return resourcenames


def getvalues():
    os.chdir(f"{dirr}/globals/items")
    resources = mineprocess()
    values = []
    for a in resources:
        f = open(a, "r")
        for line in f:
            if "Value:" in line:
                values.append(line.replace("Value: ", "").replace(" \n", ""))
    return resources, values


def woodprocess():
    os.chdir(f"{dirr}/globals/items")
    res = os.listdir(os.getcwd())
    resourcenames = []
    for a in res:
        f = open(a, "r")
        lines = f.readlines()
        resource = [i for i in lines if 'wood' in i]
        if resource:
            resourcenames.append(a)
    return resourcenames


def gettreevalues():
    os.chdir(f"{dirr}/globals/items")
    resources = woodprocess()
    values = []
    for a in resources:
        f = open(a, "r")
        for line in f:
            if "Value:" in line:
                values.append(line.replace("Value: ", "").replace(" \n", ""))
    return resources, values
