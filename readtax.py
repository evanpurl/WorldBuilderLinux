def readtax(directory):
    with open(directory) as f:
        line = f.readline()
        f.close()
    return line


def readtreasure(directory):
    with open(directory) as f:
        line = f.readline()
        f.close()
    return line
