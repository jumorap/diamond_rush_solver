import os
from PIL import Image
import imagehash


def convert_to_array(image_hashes):
    image_hashes_array = []
    for image_class in image_hashes:
        for image_hash in image_hashes[image_class]:
            image_hashes_array.append((image_class, image_hash))
    return image_hashes_array


def convert_into_matrix(array, row, cols):
    matrix = []
    for i in range(0, row):
        matrix.append(array[i * cols:(i + 1) * cols])
    return matrix


# Data collector

# return a sorted array with all the hashes of the images
def get_all_image_hashes():
    image_classes = os.listdir("./images")
    image_hashes = {i: set() for i in image_classes}
    for image_class in image_classes:
        images = os.listdir("./images/" + image_class)
        for image in images:
            image = Image.open("./images/" + image_class + "/" + image)
            image_hash = imagehash.average_hash(image)
            image_hashes[image_class].add(image_hash)

    return convert_to_array(image_hashes)


# given an image, compares by hash with the stored images and returns the class
def get_class(image, image_hashes_array, cutoff):
    image_hash = imagehash.average_hash(image)
    more_possible_classes = []
    for image_class, image_values_stored in image_hashes_array:
        image_distance = image_hash - image_values_stored
        if image_distance < cutoff:
            more_possible_classes.append((image_distance, image_class))

    return get_possible_classes(more_possible_classes)


# given an array of tuples (distance, class), returns the class with the lowest distance
def get_possible_classes(possible_classes):
    if len(possible_classes) == 0:
        return [(-1, "UK")]

    possible_classes.sort(key=lambda x: x[0])
    if len(possible_classes) > 5:  # limit the number of classes to 5
        possible_classes = possible_classes[:5]

    # delete repeated classes
    classes_set = set()
    not_repetitive_classes = []
    for i in range(len(possible_classes)):
        if possible_classes[i][1] not in classes_set:
            classes_set.add(possible_classes[i][1])
            not_repetitive_classes.append(possible_classes[i])

    if len(not_repetitive_classes) > 1 and not_repetitive_classes[0][0] in [0, 1]:
        return [not_repetitive_classes[0]]

    if len(not_repetitive_classes) > 1:
        for i in range(len(not_repetitive_classes)):
            if not_repetitive_classes[i][1] in ["P", "D"]:  # if the class is P or D, return it
                return [(-1, not_repetitive_classes[i][1])]
        for i in range(len(not_repetitive_classes)):  # if there is W return it
            if not_repetitive_classes[i][1] in ["W"]:
                return [(-1, "W")]

    if len(not_repetitive_classes) == 2:
        if not_repetitive_classes[0][1] in ["M", "B"] and not_repetitive_classes[1][1] in ["M", "B"]:
            return [(-1, "M")]

    return not_repetitive_classes


# given an array of images in PIL format, returns the class of each image
def classify_full_image(images_block, images_blocks_paths, cutoff=20):
    image_hashes_array = get_all_image_hashes()  # save this somewere to save procesing

    image_classes = []
    for image_block, path in zip(images_block, images_blocks_paths):
        image_class = get_class(image_block, image_hashes_array, cutoff)
        image_classes.append((image_class, path))
    return image_classes


def get_class_and_coordinates(classified_images):
    classes = []
    for image_class, path in classified_images:
        path = path.split("_")[1]
        path = path.split(".")[0]
        coordinates = path.split("x")
        classes.append((image_class[0][1], coordinates))
    return classes


def fill_matrix(classes):
    matrix = [["UK" for i in range(10)] for j in range(15)]
    for image_class, coordinates in classes:
        matrix[int(coordinates[0])][int(coordinates[1])] = image_class
    return matrix


def get_current_classes():
    images_blocks_paths = os.listdir("./images_utils/blocks")
    images_list = [Image.open("./images_utils/blocks/" + image_block_path) for image_block_path in images_blocks_paths]

    classified_images = classify_full_image(images_list, images_blocks_paths, 16)
    classes = get_class_and_coordinates(classified_images)
    matrix = fill_matrix(classes)
    return matrix


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print()
