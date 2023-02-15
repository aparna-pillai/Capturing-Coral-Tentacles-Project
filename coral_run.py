import os.path
import shutil
import torch

image = 'coral_photos/IMG-6268.JPG'
# Temporary placeholder

def count_tentacles(img):
    path = 'runs'
    if (os.path.isdir(path)):
        shutil.rmtree(path)

    model = torch.hub.load(os.getcwd() + '/yolov5', 'custom', source='local', path='best.pt', force_reload=True)
    results = model(img, conf=0.3, hide_labels=True, data='Coral-Tentacle-Detection-1/data.yaml', imgsz=[640, 640], project='yolov5\runs\detect', name='exp')

    formatted_results = results_to_string(results)
    print(formatted_results, "tentacles")

    results.show()

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