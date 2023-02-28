import numpy as np
import matplotlib.pyplot as plt
import os

def plot_points(image_path):
    coordinates = get_coordinates()

    x = np.array([])
    y = np.array([])

    for pair in coordinates:
        x = np.append(x, 640 - pair[0] * 640)
        y = np.append(y, 640 - pair[1] * 640)

    im = plt.imread(image_path)
    fig, ax = plt.subplots()
    im = ax.imshow(im, extent=[0, 640, 0, 640])
    ax.plot(x, y, 'o')
    plt.axis('off')

    # plt.show()
    name = 'yolov5/runs/detect/exp/labels/graphed.jpg'
    plt.savefig(name)
    return name

def get_coordinates():
    filename = os.getcwd() + '\yolov5\\runs\detect\exp\labels\\resized.txt'
    file = open(filename, 'r')
    file_lines = file.readlines()
    large_array = []

    for line in file_lines:
        array = line.split(' ')
        new_array = []

        new_array.append(float(array[1]))
        new_array.append(float(array[2]))
        
        large_array.append(new_array)

    file.close()
    return large_array

if __name__ == "__main__":
    main()