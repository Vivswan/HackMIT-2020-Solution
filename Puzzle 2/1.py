
import tensorflow as tf

import os
import shutil

import numpy as np
from shutil import copyfile
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('my_h5_model.h5')
# model.summary()
# data_dir = pathlib.Path("images")
# images = list(data_dir.glob('*.png'))
# np_image = []
# for i in images:
#     image = PIL.Image.open(str(images[len(np_image)]))
#     np_image.append(np.array(image))
#
# np_image = np.array(np_image) / 255.0
#
# np.save('np_image.npy', np_image)
np_image = np.load('np_image.npy')

model.compile()
# print(np_image.shape)
prediction = model.predict(np_image)
classes = []
xx = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

for i in prediction:
    classes.append(np.argmax(i))
#
print(classes)
np.save("prediction.npy", prediction)
np.save("classes.npy", classes)
# classes = np.load("classes.npy")

shutil.rmtree("airplanes")
os.makedirs("airplanes")
shutil.rmtree("dogs")
os.makedirs("dogs")
shutil.rmtree("something else")
os.makedirs("something else")

for i in range(0, len(prediction)):
    if classes[i] == 0:
        copyfile("images/" + str(i) + ".png", "airplanes/" + str(i) + ".png")
    elif classes[i] == 5:
        copyfile("images/" + str(i) + ".png", "dogs/" + str(i) + ".png")
    else:
       copyfile("images/" + str(i) + ".png", "something else/" + str(i) + ".png")
