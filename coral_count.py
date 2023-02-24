import os.path
import shutil
from PIL import Image

from yolov5.detect import run

# image = 'coral_photos/IMG-6289.JPG'
# Temporary placeholder

def count_tentacles_actual(img):
    # Prepare new image name
    path_end = os.path.basename(os.path.normpath(img))
    path_extension = path_end.rsplit('.', 1)[1]  # .JPG, .PNG, etc.
    new_image_name = 'resized.' + path_extension

    # Clear out old results
    parent_folder = os.getcwd()
    path = parent_folder + '\yolov5\\runs\detect'

    if (os.path.isdir(path)):
        shutil.rmtree(path)

    # Resize image to 640 x 640 (or it won't count properly)
    resized_img = Image.open(img).resize((640, 640))
    resized_img.save(new_image_name)

    # Run the model
    run(source=new_image_name)

    # Return filename of new labeled image
    return (os.getcwd() + '\yolov5\\runs\detect\exp\\' + new_image_name)

def get_count():
    filename = os.getcwd() + '\yolov5\\runs\detect\exp\labels\\resized.txt'
    with open(filename, 'r') as textfile:
        lines = len(textfile.readlines())

    return lines

# def main():
#     print(count_tentacles(image))
#     print(get_count())

# if __name__ == "__main__":
#     main()