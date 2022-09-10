from selenium import webdriver
from PIL import Image
import math
import os

import MATRICES

global browser, ss_path, current_lvl


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
    browser.set_window_size(720, 1000)
    browser.get('https://www.minijuegosgratis.com/v3/games/games/prod/219431/diamond-rush/index.html')


def take_screenshot():
    """
    Take a screenshot to current game in window and saves it as "canvas.png"
    """
    global ss_path, current_lvl
    while True:
        # Wait an input to save the current canvas as a screenshot
        current_lvl = input("Enter here to take a screenshot of the map: ")
        ss_path = "./images/ss/canvas.png"
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
        manage_screenshot()
        print("Image saved")


def save_per_block_type(i, j, image):
    """
    Save multiple images cataloged in MATRICES.py as their self reference
    """
    m_current_lvl = eval(f"MATRICES.Level{current_lvl}")
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
    global ss_path
    block_path = "./images/blocks/b"
    ss = Image.open(rf"{ss_path}")
    width, height = ss.size
    print(width, height)

    width_base = math.ceil(width / 10) - 1
    height_base = math.ceil(height / 15) - 1
    print(width_base, height_base)

    for i in range(15):
        for j in range(10):
            right = width_base * (j + 1)
            bottom = height_base * (i + 1)
            left = j * width_base
            top = i * height_base

            im1 = ss.crop((left, top, right, bottom))
            print((left, top, right, bottom))
            save_per_block_type(i, j, im1)
            # im1.save(f"{block_path}_{i}x{j}.png")


def main():
    """
    The current file must be used as an imported file that open the browser with caché info,
    load the game, saves the current image in game as ./images/ss/*.png and cut it as 10*15 images,
    where 1 image represents 1 block
    """
    load_browser()
    take_screenshot()


if __name__ == "__main__":
    main()
