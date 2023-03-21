import os.path
import shutil
from PIL import Image

import platform

from yolov5.detect import run

def count_tentacles_actual(img):
    # Clear out old results (old exp folder)
    
    parent_folder = os.getcwd()
    if platform.system() == 'Windows':
        path = parent_folder + '\\runs'
    else:
        path = parent_folder + '/runs'

    if (os.path.isdir(path)):
        shutil.rmtree(path)

    # Resize image to 640 x 640 (or it won't count properly)
    resized_img = Image.open(img).resize((640, 640))
    resized_img.save('resized.jpg')

    # Run the model
    run(
        weights='coral_model.pt', 
        data = 'Coral-Tentacle-Detection-1/data.yaml',
        source='resized.jpg',
        imgsz=(640, 640),
        conf_thres=0.3,
        save_txt=True,
        hide_labels=True,
        # save_conf=True
    )

    # Return filename of new labeled image
    if platform.system() == 'Windows':
        text = os.getcwd() + '\\runs\detect\exp\\resized.jpg'
    else:
        text = os.getcwd() + '/runs/detect/exp/resized.jpg'
    return (text)

def get_count():
    if platform.system() == 'Windows':
        filename = os.getcwd() + '\\runs\detect\exp\labels\\resized.txt'
    else:
        filename = os.getcwd() + '/runs/detect/exp/labels/resized.txt'
    with open(filename, 'r') as textfile:
        lines = len(textfile.readlines()) 

    return lines

def get_coordinates():
    if platform.system() == 'Windows':
        filename = os.getcwd() + '\\runs\detect\exp\labels\\resized.txt'
    else:
        filename = os.getcwd() + '/runs/detect/exp/labels/resized.txt'
    file = open(filename, 'r')
    file_lines = file.readlines()
    large_array = []

    for line in file_lines:
        array = line.split(' ')
        new_array = []

        new_array.append(float(array[1]))   # x_center of bounding box
        new_array.append(float(array[2]))   # y_center of bounding box
        
        large_array.append(new_array)

    file.close()
    return large_array