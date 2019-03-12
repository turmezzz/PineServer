import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor


def get_out_pic_name():
    box = int(time.time() * 1000)
    return 'out_{0}.jpg'.format(str(box))


def draw_border_and_save(img, result):
    for res in result:
        tl = (res['topleft']['x'], res['topleft']['y'])
        br = (res['bottomright']['x'], res['bottomright']['y'])
        label = res['label']

        img = cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    plt.imsave(out_path + get_out_pic_name(), img)


def detection(i_img):
    print('starting detection')
    result = tfnet.return_predict(i_img)
    print('finished detection')
    return result



options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolo.weights',
    'threshold': 0.3
}
tfnet = TFNet(options)

in_path = '/Users/turmezzz/Yandex.Disk.localized/Programming/python/YOLO_playground/in_pics/'
out_path = '/Users/turmezzz/Yandex.Disk.localized/Programming/python/YOLO_playground/out_pics/'

img1 = cv2.cvtColor(np.asarray(cv2.imread(in_path + '1.jpg'), dtype='uint8'), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(np.asarray(cv2.imread(in_path + '2.jpg'), dtype='uint8'), cv2.COLOR_BGR2RGB)
img3 = cv2.cvtColor(np.asarray(cv2.imread(in_path + '3.jpg'), dtype='uint8'), cv2.COLOR_BGR2RGB)
img4 = cv2.cvtColor(np.asarray(cv2.imread(in_path + '4.jpg'), dtype='uint8'), cv2.COLOR_BGR2RGB)
img5 = cv2.cvtColor(np.asarray(cv2.imread(in_path + '5.jpg'), dtype='uint8'), cv2.COLOR_BGR2RGB)

imgs = [img1, img2, img3, img4, img5]


def f(i_img):
    result = detection(i_img)
    draw_border_and_save(i_img, result)


ex = ThreadPoolExecutor(max_workers=5)
futures = []
for i in range(20):
    futures.append(ex.submit(f, imgs[i % 5]))
for i in range(100):
    print(i)
    time.sleep(1)
#
# print('FUCK U')
#
# print(futures)
# print(futures[0])
# print(futures[0].result())
# print(futures[0].running())




