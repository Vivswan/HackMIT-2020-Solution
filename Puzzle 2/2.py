import pathlib

import PIL
from tensorflow.keras import datasets
import numpy as np

# airplanes: 0
# dogs: 5

# data_dir = pathlib.Path("images")
# number_images = len(list(data_dir.glob('*.png')))
# np_image = []
# for i in range(0, number_images):
#     image = PIL.Image.open("images/" + str(i) + ".png")
#     np_image.append(np.array(image))
#
# np_image = np.array(np_image)
# np.save('np_image.npy', np_image)

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

combine_images = np.concatenate((train_images, test_images), axis=0)
combine_labels = np.concatenate((train_labels, test_labels), axis=0)
print(combine_images.shape)
print(combine_labels.shape)

images = []
labels = []

for i in range(0, len(combine_labels)):
    if combine_labels[i][0] == 0 or combine_labels[i][0] == 5:
        images.append(combine_images[i])
        labels.append(combine_labels[i][0])

images = np.array(images)
labels = np.array(labels)

print(images.shape)
print(labels.shape)

np_image = np.load('np_image.npy')
np_labels = []

for i in range(0, len(np_image)):
    l = None
    for j in range(0, len(images)):
        if np.array_equal(np_image[i], images[j]):
            l = labels[j]
            break

    np_labels.append(l)
    print(f"{i}: {l}")

print(np_labels)
np.save('np_labels.npy', np_labels)
