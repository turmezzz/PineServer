import os


os.chdir('MainApp')
os.mkdir('bin')
os.chdir('bin')
os.system('wget https://pjreddie.com/media/files/yolov2.weights')
os.rename('yolov2.weights', 'yolo.weights')
os.chdir('..')
os.system('pip install -e .')
