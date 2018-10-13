# dualfisheye-to-affectiva
this code was written in order to recognize multiple faces expressions with 360 dualfisheye cameras.
I used theta S camera - capturing 360 dualfisheye images with 15 fps.

I used ffmpeg to convert dualfisheye image to rectangular image.
the mapping file was created by "projection.c" program which creates the files
"fisheye_grid_ymap.pgm" and "fisheye_grid_xmap.pgm"
you can find the program at the link:
https://github.com/raboof/dualfisheye2equirectangular
you can create a mapping file for several cameras and resultoions.

in order to analayze expressions you need to get the affectiva ros node
https://www.affectiva.com/

face recognition algorithem was taken from https://realpython.com/face-recognition-with-python/

first run: 
roslaunch multi_camera_affdex multi_camera_affdex.launch

then run the python code face_publisher.py:
capture dualfisheye photos, converting them to rectangular and, display the fixed picture,then recognize faces and publish them as image messages to ros topic "/usb_cam/image/raw".

echo the "/affdex_data" topic to txt file

then runthe python code plot_data.py:
reading the txt file in live, getting the data and drawing real-time plots of expressions for each face.










