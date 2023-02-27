import os.path
import shutil
from PIL import Image

from yolov5.detect import run


def count_tentacles_actual(img):
    # Clear out old results (old exp folder)
    parent_folder = os.getcwd()
    path = parent_folder + '\yolov5\\runs\detect'

    if (os.path.isdir(path)):
        shutil.rmtree(path)

    # Resize image to 640 x 640 (or it won't count properly)
    resized_img = Image.open(img).resize((640, 640))
    resized_img.save('resized.JPG')

    # Run the model
    run(source='resized.JPG')

    # Return filename of new labeled image
    return (os.getcwd() + '\yolov5\\runs\detect\exp\\resized.JPG')

def get_count():
    filename = os.getcwd() + '\yolov5\\runs\detect\exp\labels\\resized.txt'
    with open(filename, 'r') as textfile:
        lines = len(textfile.readlines())

    return lines

def get_coordinates():
    filename = os.getcwd() + '\yolov5\\runs\detect\exp\labels\\resized.txt'
    file = open(filename, 'r')
    file_lines = file.readlines()

    for line in file_lines:
        array = line.split(' ')
        print("X-center: " + array[1] + ", Y-center: " + array[2])

    file.close()