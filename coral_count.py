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
    resized_img.save('resized.jpg')

    # Run the model
    run(source='resized.jpg')

    # Return filename of new labeled image
    return (os.getcwd() + '\yolov5\\runs\detect\exp\\resized.jpg')

def get_count():
    filename = os.getcwd() + '\yolov5\\runs\detect\exp\labels\\resized.txt'
    with open(filename, 'r') as textfile:
        lines = len(textfile.readlines()) 

    return lines