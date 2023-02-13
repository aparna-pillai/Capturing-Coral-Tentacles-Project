import glob
from IPython.display import Image, display

for image in glob.glob('/content/yolov5/runs/detect/exp/*.jpg'):
    display(Image(filename=image, width=500))
    print("\n")