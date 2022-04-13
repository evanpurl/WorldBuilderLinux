import os


def minemultiplier(directory):
    if os.path.exists(directory + "/minemultiply.txt"):
        with open(directory + "/minemultiply.txt", "r") as f:
            line = f.readline()
            return line
    else:
        with open(directory + "/minemultiply.txt", "w+") as f:
            f.write(str(1))
            return 1


def lumbermultiplier(directory):
    if os.path.exists(directory + "/lumbermultiply.txt"):
        with open(directory + "/lumbermultiply.txt", "r") as f:
            line = f.readline()
            return line
    else:
        with open(directory + "/lumbermultiply.txt", "w+") as f:
            f.write(str(1))
            return 1