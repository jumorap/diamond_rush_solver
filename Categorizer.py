import os
from PIL import Image
import imagehash
from collections import namedtuple
from colorthief import ColorThief
import math


#given an array of images in PIL format, returns the class of each image 
def classify_full_image_test(images_block, images_blocks_paths, cutoff = 20):

    image_hashes_array = getAllImageHashes() #save this somewere to save procesing
    image_colors_dict = readImageColors() 

    image_classes = []
    for image_block, path in zip(images_block, images_blocks_paths):
        image_class = getClass(image_block, image_hashes_array, image_colors_dict, cutoff)
        image_classes.append((image_class, path))
    return image_classes

def classify_full_image(images_block):
    image_classes = []
    image_hashes_array = getAllImageHashes() #save this somewere to save procesing
    image_colors_dict = readImageColors() 
    for image in images_block:
        image_class = getClass(image, image_hashes_array, image_colors_dict, 20)
        image_classes.append(image_class)
        image_classes.append(image_class)
    return image_classes


#return a sorted array with all the hashes of the images
def getAllImageHashes():
    image_classes = os.listdir("./images")
    image_hashes = {i : set() for i in image_classes}
    for image_class in image_classes:
        images = os.listdir("./images/" + image_class)
        for image in images:
            image = Image.open("./images/" + image_class + "/" + image)
            image_hash = imagehash.average_hash(image)
            image_hashes[image_class].add(image_hash)

    return convertToArray(image_hashes)


def getAllImageColors():
    image_classes = os.listdir("./images")
    image_colors = {i : set() for i in image_classes}
    for image_class in image_classes:
        images = os.listdir("./images/" + image_class)
        for image in images:
            image = Image.open("./images/" + image_class + "/" + image)
            image_color = ColorThief(image)
            color = image_color.get_palette(color_count=3)[2]
            print(color)
            image_colors[image_class].add(color)


    return convertToArray(image_colors)

# ------------------ IO Operations ------------------

#save image colors in a file
def saveImageColors(allImageColors):
    with open("imageColors.txt", "w") as f:
        for image_class, image_color in allImageColors:
            f.write(str(image_class) + " " + str(image_color[0]) + " " + str(image_color[1]) +" "+ str(image_color[2]) + "\n")

def readImageColors():
    image_colors_list = []
    with open("imageColors.txt", "r") as f:
        for line in f:
            line = line.split()
            image_class = line[0]
            image_color = (int(line[1]), int(line[2]), int(line[3]))
            image_colors_list.append((image_class, image_color))

    #convert allImageColors into a dictionary
    image_classes = ['R' ,'D' ,'P' ,'M'  ,'W' ,'A' ,'C' ,'K' ,'L' ,'S', 'H' ,'B' ,'U']
    image_colors = {i : set() for i in image_classes}
    for image_class, image_color in image_colors_list:
        image_colors[image_class].add(image_color)
    
    return image_colors

#function to save images hashes in a file as
def saveImageHashes(allImageHashed):
    with open("imageHashes.txt", "w") as f:
        for image_class, image_hash in allImageHashed:
            f.write(str(image_class) + " " + str(image_hash) + "\n")

def readImageHashes():
    image_hashes = []
    with open("imageHashes.txt", "r") as f:
        for line in f:
            line = line.split()
            image_class = line[0]
            image_hash = int(line[1])
            image_hashes.append((image_class, image_hash))
    return image_hashes


# ------------------ Util Functions ------------------
def convertToArray(image_hashes):
    image_hashes_array = []
    for image_class in image_hashes:
        for image_hash in image_hashes[image_class]:
            image_hashes_array.append((image_class, image_hash))
    return image_hashes_array

def convert_into_matrix(array, row, cols):
    matrix = []
    for i in range(row):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(array[i*cols + j])
    return matrix



# ------------------ Classify Functions ------------------
#given an image, compares by hash with the stored images and returns the class

ImageDistance = namedtuple('ImageDistance', 'distance kind')

def getClass(image, image_hashes_array, image_colors_dict, cutoff):
    image_hash = imagehash.average_hash(image)
    image_color = ColorThief(image).get_color(quality=1)
    possible_classes = [] #list of classes that are more likely to be the class of the image
    for image_class, image_values_stored in image_hashes_array:
        image_distance = image_hash - image_values_stored
        if(image_distance < cutoff):
            possible_classes.append(ImageDistance(image_distance, image_class))
    
    possible_classes =  getPossibleClasses(possible_classes)
    final_classes = filterClassesByColor(possible_classes, image_colors_dict , image_color)
    return final_classes

#given an array of tuples (distance, class), returns the class with the lowest distance
def getPossibleClasses(morePossibleClasses):
    if(len(morePossibleClasses) == 0):
        return ImageDistance(9999, "Uk")

    #order by distance
    morePossibleClasses.sort(key=lambda x: x[0])
    if(len(morePossibleClasses) > 5):     #limit the number of classes to 5
        morePossibleClasses = morePossibleClasses[:5]

    #delete repeated classes
    classesSet = set()
    NotRepetitiveClasses = []
    for i in range(len(morePossibleClasses)):
        if(morePossibleClasses[i][1] not in classesSet):
            classesSet.add(morePossibleClasses[i][1])
            NotRepetitiveClasses.append(morePossibleClasses[i])

    if len(NotRepetitiveClasses) > 1 and NotRepetitiveClasses[0].distance in [0,1]:
        return [NotRepetitiveClasses[0]]

    return NotRepetitiveClasses

def getDistanceBetweenColors(color1, color2):
    return math.sqrt((color1[0]-color2[0])**2 + (color1[1]-color2[1])**2 + (color1[2]-color2[2])**2)

def filterClassesByColor(possibleClasses, image_colors_dict, image_color):
    #check for the closest similarity in the colors
    clossestColorDistance = 10000
    closestColorClass = ""
    for distance , kind in possibleClasses:
        for color in image_colors_dict[kind]:
            colorDistance = getDistanceBetweenColors(color, image_color)
            if colorDistance < clossestColorDistance:
                clossestColorDistance = colorDistance
                closestColorClass = (distance, kind)

    return closestColorClass