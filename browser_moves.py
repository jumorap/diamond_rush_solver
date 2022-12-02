import time

import browser_image


def main(solution_matrix):
    """
    Move the character with the matrix solution
    """
    # Replace L with left, R with right, U with up, D with down
    solution_matrix = [x.replace("L", "left")
                       .replace("D", "down")
                       .replace("U", "up")
                       .replace("R", "right") for x in solution_matrix]

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
