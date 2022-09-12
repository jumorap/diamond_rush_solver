import os
from PIL import Image
import imagehash
from collections import namedtuple
from colorthief import ColorThief
import math

#utils 
def convertToArray(image_hashes):
    image_hashes_array = []
    for image_class in image_hashes:
        for image_hash in image_hashes[image_class]:
            image_hashes_array.append((image_class, image_hash))
    return image_hashes_array

def convert_into_matrix(array, row, cols):
    matrix = []
    for i in range(0, row):
        matrix.append(array[i*cols:(i+1)*cols])
    return matrix




#Data collector

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


#given an image, compares by hash with the stored images and returns the class
def getClass(image, image_hashes_array, image_colors_dict, cutoff):
    image_hash = imagehash.average_hash(image)
    image_color = ColorThief(image).get_color(quality=1)
    morePossibleClasses = []
    for image_class, image_values_stored in image_hashes_array:
        image_distance = image_hash - image_values_stored
        if(image_distance < cutoff):
            morePossibleClasses.append((image_distance, image_class))
    
    return getMorePossibleClasses(morePossibleClasses, image_colors_dict, image_color)


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

    return [closestColorClass]

#given an array of tuples (distance, class), returns the class with the lowest distance
def getMorePossibleClasses(morePossibleClasses, image_colors_dict, image_color):
    if(len(morePossibleClasses) == 0):
        return [(-1, "UK")]

    morePossibleClasses.sort(key=lambda x: x[0])
    if(len(morePossibleClasses) > 5): #limit the number of classes to 5
        morePossibleClasses = morePossibleClasses[:5]

    #delete repeated classes
    classesSet = set()
    NotRepetitiveClasses = []
    for i in range(len(morePossibleClasses)):
        if(morePossibleClasses[i][1] not in classesSet):
            classesSet.add(morePossibleClasses[i][1])
            NotRepetitiveClasses.append(morePossibleClasses[i])

    if len(NotRepetitiveClasses) > 1 and NotRepetitiveClasses[0][0] in [0,1]:
        return [NotRepetitiveClasses[0]]

    
    if len(NotRepetitiveClasses)  > 1:
        for i in range(len(NotRepetitiveClasses)):
            if(NotRepetitiveClasses[i][1] in ["P", "D"]): #if the class is P or D, return it
                return [(-1,NotRepetitiveClasses[i][1])]
        for i in range(len(NotRepetitiveClasses)):  #if there is W return it
            if(NotRepetitiveClasses[i][1] in ["W"]):
                return [(-1, "W")]


    if len(NotRepetitiveClasses) == 2:
        if(NotRepetitiveClasses[0][1] in ["M", "B"] and NotRepetitiveClasses[1][1] in ["M", "B"]):
            return [(-1, "M")]

    return filterClassesByColor(NotRepetitiveClasses, image_colors_dict, image_color)

#given an array of images in PIL format, returns the class of each image 
def classify_full_image(images_block, images_blocks_paths, cutoff = 20):

    image_hashes_array = getAllImageHashes() #save this somewere to save procesing
    image_colors_dict = readImageColors() 

    image_classes = []
    for image_block, path in zip(images_block, images_blocks_paths):
        image_class = getClass(image_block, image_hashes_array, image_colors_dict, cutoff)
        image_classes.append((image_class, path))
    return image_classes

def getClassAndCoordinates(classified_images):
    classes = []
    for image_class, path in classified_images:
        path = path.split("_")[1]
        path = path.split(".")[0]
        coordinates = path.split("x")
        classes.append((image_class[0][1], coordinates))
    return classes
    
def fillMatrix(classes):
    matrix = [["UK" for i in range(10)] for j in range(15)]
    for image_class, coordinates in classes:
        matrix[int(coordinates[0])][int(coordinates[1])] = image_class
    return matrix

def getCurrentClasses():
    images_blocks_paths = os.listdir("./images_utils/blocks")
    images_list = [Image.open("./images_utils/blocks/" + image_block_path) for image_block_path in images_blocks_paths]

    clasified_images = classify_full_image(images_list,  images_blocks_paths, 16)
    classes = getClassAndCoordinates(clasified_images)
    matrix = fillMatrix(classes)
    return matrix

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end = " ")
        print()

curr = getCurrentClasses()
printMatrix(curr)


