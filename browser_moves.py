import random
import time

import browser_image


def main():
    """
    Move randomly the character
    """
    choices = ["up", "down", "left", "right"]
    correct_lvl2 = [
        "left", "left", "left", "left", "left", "down", "left", "up",
        "up", "up", "up", "up", "up", "up", "up", "up", "right", "right",
        "up", "down", "right", "right", "down", "down", "down", "right",
        "right", "up", "left", "left", "down", "down", "down", "left",
        "left", "down"
    ]

    # Print and show a timer of 3 seconds
    timer = 3

    print("Please go to the game and wait 3 seconds")

    for i in range(timer):
        print(timer - i)
        time.sleep(1)

    for election in correct_lvl2:
        print(f"Moving {election}")
        browser_image.movements(election)
        time.sleep(1)

    while True:
        election = random.choice(choices)
        print(f"Moving {election}")
        browser_image.movements(election)
        time.sleep(1)


if __name__ == '__main__':
    main()
