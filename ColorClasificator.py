#get the main color of the image in hex
from PIL import Image
import numpy as np
import os
from collections import namedtuple
from colorthief import ColorThief
#import plt
import matplotlib.pyplot as plt

RangeColors = namedtuple('RangeColors', 'max min')

PERSONAJE_COLORS = RangeColors([228, 202, 172], [219, 189, 155])



def get_dominant_palette(PIL_image):
    color_thief = ColorThief(PIL_image)
    palette = color_thief.get_palette(color_count=3)
    return palette

#load the images numpy npy
images = np.load('images.npy')

def isInColorRange(color, colorRange):
    return (colorRange.min[0] <= color[0] <= colorRange.max[0]) and (colorRange.min[1] <= color[1] <= colorRange.max[1]) and (colorRange.min[2] <= color[2] <= colorRange.max[2])

def getPersonajeLocation(images):
    #convert the images to PIL
    images = [Image.fromarray(image) for image in images]

    for i in range(len(images)):
        palette = get_dominant_palette(images[i])
        for color in palette:
            if isInColorRange(color, PERSONAJE_COLORS):
                print("row", i//15, "column", i%10)



#get all the file names in the folder
def getImages():
    path = 'images/blocks'
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    return files




images = getImages()


for image_index, image in enumerate(images):
    image = Image.open(image)
    palette = get_dominant_palette(image)
    print(image_index, " ", palette)
    for i in range(4):
        if isInColorRange(palette[i], PERSONAJE_COLORS):
            print(palette[i])


            
    
        



    