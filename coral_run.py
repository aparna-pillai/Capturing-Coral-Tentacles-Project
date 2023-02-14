# import glob
# from IPython.display import Image, display

# for image in glob.glob('/content/yolov5/runs/detect/exp/*.jpg'):
#     display(Image(filename=image, width=500))
#     print("\n")

import sys
import os.path
import shutil
import torch
import matplotlib.pyplot as plt
import cv2

path = 'runs'
if (os.path.isdir(path)):
    shutil.rmtree(path)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
img = 'coral_photos/IMG-6268.JPG'

results = model(img)
print(results)
print(results.pred[0])
# print(results.render())
# results.show()
# results.crop()

# fig, ax = plt.subplots(figsize=(16, 12))
# plt.imshow(results.render()[0])
# plt.show()

def results_to_string(results):
    return_string = ""
    if results.pred[0].shape[0]:
        for c in results.pred[0][:, -1].unique():
            n = (results.pred[0][:, -1] == c).sum()
            return_string += f"{n}"
    
    return return_string