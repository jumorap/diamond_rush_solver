from selenium import webdriver
from PIL import Image
import math
import os
import numpy as np
import pydirectinput


import Solver.matrix


global browser, ss_path, current_lvl, arr_blocks_np


def load_browser():
    """
    Load caché options to browser, saving the games played before.
    Use chromedriver to open the game, resizing the window
    """
    global browser
    # Configure the browser to load the previous games in caché
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/Users/juan1/AppData/Local/Chromium/User Data/Default") # Get from chrome://version/ in browser. Tagged as "profile route"

    # Pick the App to lunch the browser and configure the window size with the URL to load
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    browser.set_window_size(530, 804)
    browser.get('https://www.minijuegosgratis.com/v3/games/games/prod/219431/diamond-rush/index.html')


def take_screenshot():
    """
    Take a screenshot to current game in window and saves it as "canvas.png"
    """
    global ss_path, current_lvl
    # Wait an input to save the current canvas as a screenshot
    current_lvl = input("Enter here to take a screenshot of the map: ")
    ss_path = "./images_utils/canvas.png"
    browser.save_screenshot(ss_path)

    # Opens an image in RGB mode and get the size
    im = Image.open(rf"{ss_path}")
    width, height = im.size

    # Setting the points for cropped image
    window_game = int(height * (640 / 960))
    measure = math.ceil((width - window_game) / 2)
    left, top, right, bottom = measure, 0, measure + window_game, height

    # Cropped image of above dimension and save the new image
    im1 = im.crop((left, top, right, bottom))
    im1.save(ss_path)

    # Resize the image to 560x840
    im1 = Image.open(ss_path)
    im1 = im1.resize((560, 840))
    im1.save(ss_path)
    print("Image saved")


def save_per_block_type(i, j, image):
    """
    Save multiple images cataloged in matrix.py as their self reference
    """
    m_current_lvl = eval(f"matrix.Level{current_lvl}")
    path = f"./images/{m_current_lvl[i][j]}"
    try:
        os.mkdir(path)
    except:
        ""
    image.save(f"{path}/{m_current_lvl[i][j]}_{i}x{j}_lvl{current_lvl}.png")


def manage_screenshot():
    """
    Cut the map image as 15*10 image per block and save it as "./images/blocks/b*x*.png"
    """
    global ss_path, arr_blocks_np
    block_path = "./images_utils/blocks/b"
    ss = Image.open(rf"{ss_path}")
    width, height = ss.size
    arr_blocks_np = []

    width_base, height_base = math.ceil(width / 10), math.ceil(height / 15)

    for i in range(15):
        for j in range(10):
            right, bottom = width_base * (j + 1), height_base * (i + 1)
            left, top = j * width_base, i * height_base

            im1 = ss.crop((left, top, right, bottom))
            # save_per_block_type(i, j, im1)
            path_temp = f"{block_path}_{i}x{j}.png"
            im1.save(path_temp)
            arr_blocks_np.append(np.asarray(Image.open(path_temp)))


def np_image():
    """
    Load the current image as a CPU array in numpy format
    :return: np array
    """
    return np.asarray(Image.open(ss_path))


def np_blocks():
    """
    :return: np array:  arr_blocks_np
    """
    return np.array(arr_blocks_np)


def movements(move):
    """
    Move the character in the game
    :param move: str
    :return:
    """
    check_browser()
    pydirectinput.keyDown(move)
    pydirectinput.keyUp(move)


def check_browser():
    """
    Check if the browser is open
    """
    try:
        browser.title
    except:
        exit("Browser closed")


def main():
    """
    The current file must be used as an imported file that open the browser with caché info,
    load the game, saves the current image in game as ./images/ss/*.png and cut it as 10*15 images,
    where 1 image represents 1 block
    """
    load_browser()
    take_screenshot()
    manage_screenshot()


if __name__ == "__main__":
    main()
