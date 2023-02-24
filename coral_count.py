import os.path
import shutil
import cv2
from PIL import Image

from yolov5.detect import run

image = 'coral_photos/IMG-6289.JPG'
# image = 'yolov5\Coral-Tentacle-Detection-1\\test\images\IMG-6289_JPG.rf.ce9338dc077961ea1741b6e7e0d8d4b5.jpg'
# Temporary placeholder

def count_tentacles(img):
    # Clear out old results
    parent_folder = os.getcwd()
    path = parent_folder + '\yolov5\\runs\detect'

    if (os.path.isdir(path)):
        shutil.rmtree(path)

    # open_image = Image.open(img)
    resized_img = Image.open(img).resize((640, 640))
    resized_img.save('resized.jpg')

    # Run the model
    # NOTE: Image size must be 640 x 640 or it won't count properly.
    run(source='resized.jpg', imgsz=(640, 640))

    # NOTE: Need to close the image window before anything after this line will run.

    # Read labels text file for displaying count
    path_end = os.path.basename(os.path.normpath(image))
    path_actual_name = path_end.rsplit('.', 1)[0]

    filename = parent_folder + '\yolov5\\runs\detect\exp\labels\\' + path_actual_name + '.txt'

    print(get_count(parent_folder + '\yolov5\\runs\detect\exp\labels\\resized.txt'))

    # with open(filename, 'r') as textfile:
    #     lines = len(textfile.readlines())
    #     print(lines, "tentacles")

    cv2.destroyAllWindows()

def get_count(path_name):
    with open(path_name, 'r') as textfile:
        lines = len(textfile.readlines())

    return lines

def main():
    count_tentacles(image)

if __name__ == "__main__":
    main()