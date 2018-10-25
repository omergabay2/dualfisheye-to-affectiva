import subprocess
import time

def main():
    try:
        #chose 1 for camera and 2 for rosbag
        mode = 0

        process1 = subprocess.Popen("roslaunch multi_camera_affdex multi_camera_affdex.launch", shell=True)
        time.sleep(1)
        #waiting for affactiva
        process2 = subprocess.Popen("python aff_sub.py",  shell=True)

        if mode == 0:
            process3 = subprocess.Popen("rosbag record -O last_record.bag /usb_cam/image_raw", shell=True)
            process4 = subprocess.Popen("python face_publisher.py", shell=True)

        elif mode == 1:
            process3 = subprocess.Popen("mplayer ~/PycharmProjects/dualfisheye-to-affectiva/scripts/outpy.avi", shell=True)
            process4 = subprocess.Popen("rosbag play last_record.bag", shell=True)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        process1.kill()
        process2.kill()
        process3.kill()
        process4.kill()
        print("Program has stopped ...\n")
        exit()

if __name__ == '__main__':
    main()
