cd MainApp
mkdir bin
cd bin
wget https://pjreddie.com/media/files/yolov2.weights
cd ..
pip install -e .
cd ..
python manage.py makemigrations
python manage.py migrate