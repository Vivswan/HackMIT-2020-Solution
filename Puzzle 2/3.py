import numpy as np
from PIL import Image

np_labels = np.load('np_labels.npy')

lines = None
coordinates = []
with open("assignment.txt", "r") as file:
    lines = file.readlines()

for i in range(0, len(lines)):
    line = lines[i].strip().replace("(", "").replace(")", "").replace(" ", "").split(",")
    if len(line[0]) > 0:
        x = int(line[0].strip())
        y = int(line[1].strip())
        coordinates.append([x, y, np_labels[i]])

np_img = np.ones((max(coordinates)[0] + 1, max(coordinates)[0] + 1, 3), dtype=np.uint8)

for i in coordinates:
    if i[2] == 0:
        np_img[i[0]][i[1]] *= 255
    if i[2] == 5:
        np_img[i[0]][i[1]] *= 0

w, h = max(coordinates)[0], max(coordinates)[0]
img = Image.fromarray(np_img, 'RGB')
# img.save('my.png')
img.show()
