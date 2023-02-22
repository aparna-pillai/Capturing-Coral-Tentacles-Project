import os.path
import shutil
import cv2

from yolov5.detect import run

image = 'coral_photos/IMG-6268.JPG'
# Temporary placeholder

def count_tentacles(img):
    # Clear out old results
    parent_folder = os.getcwd()
    path = parent_folder + '\yolov5\\runs\detect'

    if (os.path.isdir(path)):
        shutil.rmtree(path)

    # Run the model
    run(source=img)

    # NOTE: Need to close the image window before anything after this line will run.

    # Read labels text file for displaying count
    path_end = os.path.basename(os.path.normpath(image))
    path_actual_name = path_end.rsplit('.', 1)[0]

    filename = parent_folder + '\yolov5\\runs\detect\exp\labels\\' + path_actual_name + '.txt'

    with open(filename, 'r') as textfile:
        lines = len(textfile.readlines())
        print(lines, "tentacles")

    cv2.destroyAllWindows()

def main():
    count_tentacles(image)

if __name__ == "__main__":
    main()