import os.path
import shutil
import torch
import sys
import cv2
import glob
import numpy as np

from yolov5.detect import run

image = 'coral_photos/IMG-6268.JPG'
# Temporary placeholder

def count_tentacles(img):
    # Clear out old results
    parent_folder = os.getcwd()
    path = parent_folder + '\yolov5\\runs\detect'

    if (os.path.isdir(path)):
        shutil.rmtree(path)

    # model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

    run(source=img)
    cv2.destroyAllWindows()

    filename = parent_folder + '\yolov5\\runs\detect\exp\labels\IMG-6268.txt'

    with open(filename, 'r') as textfile:
        lines = len(textfile.readlines())
        print(lines, "tentacles")
    
    # model.conf = 0.3
    # model.hide_labels = True
    # model.data = 'Coral-Tentacle-Detection-1/data.yaml'
    # model.project = 'yolov5/runs/detect'
    # model.name = 'exp'

    # results = model(img, size=640)
    
    # results = model(img, conf=0.3, hide_labels=True, data='Coral-Tentacle-Detection-1/data.yaml', 
    # imgsz=[640, 640], project='yolov5\runs\detect', name='exp')

    # formatted_results = results_to_string(results)
    # print(formatted_results, "tentacles")

    # results.pandas().xyxy[0]

    # results.show()

def results_to_string(results):
    return_string = ""
    if results.pred[0].shape[0]:
        for c in results.pred[0][:, -1].unique():
            n = (results.pred[0][:, -1] == c).sum()
            return_string += f"{n}"
    
    return return_string

def main():
    count_tentacles(image)

if __name__ == "__main__":
    main()