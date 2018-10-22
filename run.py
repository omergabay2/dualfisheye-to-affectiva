import subprocess
import time

def main():
    try:
        process1 = subprocess.Popen("roslaunch multi_camera_affdex multi_camera_affdex.launch faceMode:=1 draw:=0", shell=True)
        time.sleep(1)
        #waiting for affactiva
        process2 = subprocess.Popen("python aff_sub.py",  shell=True)
        process3 = subprocess.Popen("rostopic echo -p /omer_data > ~/PycharmProjects/dualfisheye-to-affectiva/scripts/data.txt", shell=True)

        #for using camera uncomment:
        process4 = subprocess.Popen("rosbag record -O last_record.bag /usb_cam/image_raw", shell=True)
        process5 = subprocess.Popen("python face_publisher.py", shell=True)

        #for playing from rosbag uncomment process 5 (4 in order to watch the video):
        #process4 = subprocess.Popen("mplayer ~/PycharmProjects/dualfisheye-to-affectiva/scripts/outpy.avi", shell=True)
        #process5 = subprocess.Popen("rosbag play last_record.bag", shell=True)

        process6 = subprocess.Popen("python plot_data.py", shell=True)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        process1.kill()
        process2.kill()
        process3.kill()
        process4.kill()
        process5.kill()
        process6.kill()
        print("Program has stopped ...\n")
        exit()

if __name__ == '__main__':
    main()
