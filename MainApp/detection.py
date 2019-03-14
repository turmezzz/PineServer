import os
import cv2
import matplotlib.pyplot as plt
from darkflow.net.build import TFNet


def draw_border_and_save(img, result, objs_to_detect):
    for res in result:
        label = res['label']
        if label not in objs_to_detect:
            continue
        tl = (res['topleft']['x'], res['topleft']['y'])
        br = (res['bottomright']['x'], res['bottomright']['y'])
        img = cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    return img


def detection(i_img, i_path_and_name_to_save, i_objs_to_detect):
    result = tfnet.return_predict(i_img)
    file_name = i_path_and_name_to_save.split('/')[-1]
    for i in range(len(result)):
        result[i]['file_name'] = file_name
    # result = [{
    #             'bottomright': {'x': 636, 'y': 776},
    #             'confidence': 0.28718543,
    #             'label': 'person',
    #             'topleft': {'x': 563, 'y': 281},
    #             'file_name': 'img_0.jpg'}]
    img = draw_border_and_save(i_img, result, i_objs_to_detect)
    plt.imsave(i_path_and_name_to_save, img)
    return result


options = {
    'model': os.path.abspath('.') + '/MainApp/cfg/yolo.cfg',
    'load': os.path.abspath('.') + '/MainApp/bin/yolo.weights',
    'config': os.path.abspath('.') + '/MainApp/cfg/',
    'threshold': 0.5
}
tfnet = TFNet(options)


