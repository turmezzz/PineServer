import os
import cv2
# import time
import matplotlib.pyplot as plt
from darkflow.net.build import TFNet


def draw_border_and_save(img, result):
    for res in result:
        tl = (res['topleft']['x'], res['topleft']['y'])
        br = (res['bottomright']['x'], res['bottomright']['y'])
        label = res['label']
        img = cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    return img


def detection(i_img, i_path_and_name_to_save):
    result = tfnet.return_predict(i_img)
    img = draw_border_and_save(i_img, result)
    plt.imsave(i_path_and_name_to_save, img)
    return result
    # return {}


options = {
    'model': os.path.abspath('.') + '/MainApp/cfg/yolo.cfg',
    'load': os.path.abspath('.') + '/MainApp/bin/yolo.weights',
    'config': os.path.abspath('.') + '/MainApp/cfg/',
    'threshold': 0.1
}
tfnet = TFNet(options)


