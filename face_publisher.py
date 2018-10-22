#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import subprocess
import logging
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from threading import Thread

image = None


def thread1_take_pictures():
    # this function takes pictures
    # each picture is saved to VideoWriter and display in a new window
    # In additional, the last picture taken will be saved on global variable named "last_picture"

    global image

    subprocess.call(
        "./projection -x fisheye_grid_xmap.pgm -y fisheye_grid_ymap.pgm -h 960 -w 1920 -r 960 -c 1920 -b 51 -m thetas",
        shell=True)
    # create the mapping files from dualfisheye to rectungaular 640 1280 640 1280 30 or 960 1920 960 1920 51

    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 1, (1920, 960))
    cap = cv2.VideoCapture(1)

    try:
        while True:
            ret, frame = cap.read()

            crop_img = frame[0:640, 0:1280]
            # read & cut the unrellavnt data from the image - always 640 and 1280!!!!!

            resize_img = cv2.resize(crop_img, (1920, 960))
            # resize the image for resolution 1920:960

            cv2.imwrite('captured.png', resize_img)
            # save the image for ffmpeg

            ffmpeg_process = subprocess.Popen("ffmpeg -y -i captured.png -i fisheye_grid_xmap.pgm -i fisheye_grid_ymap.pgm -filter_complex remap fixed.png", shell=True)
            # remapping the image from fisheye to  equirectangular
            ffmpeg_process.communicate()
            # wait until the process is ending

            image2 = cv2.imread('fixed.png')
            # read the equirectangular image

            image = image2
            # in order to use the image in the other thread too we put it in a global variable

            cv2.imshow('Live', image2)
            k = cv2.waitKey(1)
            # display live

            out.write(image2)
            # recording for video

            if k == ord('q'):
                cap.release()
                cv2.destroyAllWindows()

    except:
        print logging.exception("thread1_take_pictures exception")

    cap.release()
    cv2.destroyAllWindows()


def rospy_main_thread():
    # this function takes the pending "last_picture"
    # it detect and crop faces and publish them to "/usb_cam/image_raw" topic which Affectiva will subscribe too and analyze
    # later Affectiva will send the data to a "/affdex_data" topic which will be acquired by plot_sub
    global image

    def faces_detection(image2):
        cascPath = "haarcascade_frontalface_alt2.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(5, 5),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Found {0} faces!".format(len(faces)))
        return faces

    pub = rospy.Publisher('/usb_cam/image_raw', Image, queue_size=1)
    rospy.init_node('Camera_Publisher', anonymous=True)

    rate = rospy.Rate(10)  # 10hzro
    bridge = CvBridge()

    while not rospy.is_shutdown():

        if image is None:
            continue
        image2 = image
        image = None

        found_faces = faces_detection(image2)

        for (x, y, w, h) in found_faces:
            # publish face each time face is recognized
            # send some more of the information of each face for the affectiva to read it with better chance
            if x > 30 and 1920 - (x + w) > 30:
                cropped_face = image2[0:960, x - 30:(x + w + 30)]
                black_blank = np.zeros((960, x - 30, 3), np.uint8)
            else:
                cropped_face = image2[0:960, x:x + w]
                black_blank = np.zeros((960, x, 3), np.uint8)

            black_blank[:] = (0, 0, 0)
            ready = np.concatenate((black_blank, cropped_face), axis=1)
            #location = ((x + w) / 2 + x / 2) / 10
            #ready[0][0][0] = location
            cv2_frame = np.asarray(ready)

            image_message = bridge.cv2_to_imgmsg(cv2_frame, "bgr8")

            try:
                pub.publish(image_message)  # publishing the faces images
                print("Published")
            except CvBridgeError as e:
                print(e)

            rate.sleep()


def main():
    try:
        f = Thread(target=thread1_take_pictures)
        f.daemon = True
        f.start()
        rospy_main_thread()
    except:
        print("not publishing")


if __name__ == '__main__':
    main()
