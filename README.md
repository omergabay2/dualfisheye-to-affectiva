# dualfisheye-to-affectiva
this code was written in order to recognize multiple faces expressions with 360 dualfisheye cameras.
I used theta S camera - capturing 360 dualfisheye images with 15 fps.

I used ffmpeg to convert dualfisheye image to rectangular image.
the mapping file was created by "projection.c" program which creates the files
"fisheye_grid_ymap.pgm" and "fisheye_grid_xmap.pgm"
you can find the program at the link:
https://github.com/raboof/dualfisheye2equirectangular
you can create a mapping file for several cameras and resolutions.

in order to analayze expressions you need to get the affectiva ros node
https://www.affectiva.com/

face detection algorithem was taken from https://realpython.com/face-recognition-with-python/

## ***Running The Program***

***run:***
 
```
python run.py
```


```ruby
import subprocess
import time

def main():
    try:
        process1 = subprocess.Popen("roslaunch multi_camera_affdex multi_camera_affdex.launch", shell=True)
        time.sleep(1)
        #waiting for affactiva
        print("Affectiva is running...")
        process2 = subprocess.Popen("rosbag record /usb_cam/image_raw", shell=True)
        print("Rosbag start recording...")
        process3 = subprocess.Popen("rostopic echo -p /affdex_data > ~/PycharmProjects/dualfisheye-to-affectiva/scripts/data.txt", shell=True)
        process4 = subprocess.Popen("python face_publisher.py", shell=True)
        process5 = subprocess.Popen("python plot_data.py", shell=True)
        print("Plotting data ...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        process1.kill()
        print("\nAffectiva is shutting down...")
        process2.kill()
        print("Rosbag stop recording...")
        process3.kill()
        print("Stop writing from /affdex_data topic...")
        process4.kill()
        print("Stop Capturing...")
        process5.kill()
        print("Close ploting data ...\n")
        exit()

if __name__ == '__main__':
    main()
```

***python code face_publisher.py:***
capture dualfisheye photos, converting them to rectangular and, display the fixed picture,then recognize faces and publish them as image messages to ros topic "/usb_cam/image/raw".
echo the "/affdex_data" topic to txt file

***python code plot_data.py:***
reading the txt file in live, getting the data and drawing real-time plots of expressions for each face.










