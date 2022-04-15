# Here, the code for the decision making for the AI will be stored here.
import os
import sys
import random


def enemymove(defense):
    rand = random.randint(1, 50)
    if defense:
        if rand > 32:
            return "defend"
        else:
            return "attack"
    else:
        if rand > 32:
            return "attack"
        else:
            return "defend"
