import random
import time

import browser_image


def main(solution_matrix):
    """
    Move randomly the character
    """
    """choices = ["up", "down", "left", "right"]
    correct_lvl2 = [
        "left", "left", "left", "left", "left", "down", "left", "up",
        "up", "up", "up", "up", "up", "up", "up", "up", "right", "right",
        "up", "down", "right", "right", "down", "down", "down", "right",
        "right", "up", "left", "left", "down", "down", "down", "left",
        "left"
    ]"""

    # Replace L with left, R with right, U with up, D with down
    solution_matrix = [x.replace("L", "left") for x in solution_matrix]
    solution_matrix = [x.replace("R", "right") for x in solution_matrix]
    solution_matrix = [x.replace("U", "up") for x in solution_matrix]
    solution_matrix = [x.replace("D", "down") for x in solution_matrix]

    # Print and show a timer of 3 seconds
    timer = 3

    print("Please go to the game and wait 3 seconds")

    for i in range(timer):
        print(timer - i)
        time.sleep(1)

    for election in solution_matrix:
        print(f"Moving {election}")
        browser_image.movements(election)
        time.sleep(0.07)

    """while True:
        election = random.choice(choices)
        print(f"Moving {election}")
        browser_image.movements(election)
        time.sleep(1)"""
