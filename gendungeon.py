import os, sys, random

dirr = sys.path[0]


def dunrooms(roomnum):  # This function is designed to create the dungeon's rooms.
    directions = ["left", "front", "right"]
    left = []
    right = []
    front = []
    dec = ["room", "room", "room", "enemy", "room", "room", "room item", "enemy"]
    for a in range(1, roomnum + 1):
        for b in range(0, len(directions)):
            decision = dec[random.randint(0, len(dec) - 1)]
            if b == 0:
                left.append(decision)
            if b == 1:
                front.append(decision)
            if b == 2:
                right.append(decision)
    return left, front, right
