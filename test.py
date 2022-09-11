from PIL import Image
import os
from Categorizer import classify_full_image
import browser_image

browser_image.main()
images_blocks = browser_image.np_blocks()
#convert to PIL
images_blocks = [Image.fromarray(image) for image in images_blocks]
clasified_images = classify_full_image(images_blocks)


#print array in matrix form 15x10
for i in range(0, len(clasified_images), 10):
    print(clasified_images[i:i+10])
    




# images_blocks_paths = os.listdir("./images_utils/blocks")
# images_list = [Image.open("./images_utils/blocks/" + image_block_path) for image_block_path in images_blocks_paths]
# 



