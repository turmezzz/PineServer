import os


if not os.path.exists('./files'):
    os.mkdir('files')
    os.chdir('files')
    os.mkdir('output')
    os.mkdir('zips')
    os.chdir('..')
os.chdir('MainApp')
if not os.path.exists('bin'):
    os.mkdir('bin')
    os.chdir('bin')
    os.system('wget https://pjreddie.com/media/files/yolov2.weights')
    os.rename('yolov2.weights', 'yolo.weights')
os.system('pip3 install -e .')
