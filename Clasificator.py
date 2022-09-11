from array import array
import tensorflow
import browser_image
import PIL
import numpy as np

#load the model
model = tensorflow.keras.models.load_model('DimondModel.h5')


def getImages():
    browser_image.main()
    #load the images
    images = browser_image.np_blocks()
    return images


#load the images with numpy npy
def getImagesNpy():
    images = np.load('images.npy')
    return images

def prepareImages(images):
    #resize each image to 224x224
    images = np.array([np.array(PIL.Image.fromarray(image).resize((224,224))) for image in images])
    #delete the alpha channel
    images = images[:,:,:,:3]
    return images


#images = prepareImages(getImagesNpy())
#predictions = model.predict(images)


#read the predictions
classes = ['R', 'B', 'H', 'U', 'M', 'K', 'S', 'A', 'C', 'P', 'L', 'W', 'D', 'blocks']

#predict based on the classes
def predict(images):
    images = prepareImages(images)
    predictions = model.predict(images)
    predictions = np.argmax(predictions, axis=1)
    predictions = [classes[prediction] for prediction in predictions]
    predictions = np.array(predictions).reshape(15,10)
    return predictions



    
images = getImagesNpy()
predictions = predict(images)
print(predictions)






