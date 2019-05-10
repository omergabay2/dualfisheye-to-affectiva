#! /usr/bin/python
import rospy
import matplotlib.pyplot as plt
import time
from std_msgs.msg import String
from affdex_msgs.msg import AffdexFrameInfo
from std_msgs.msg import Int32
import sys


def main():
    rospy.init_node('send_messenger', anonymous=True)
    pub = rospy.Publisher("/send_msg", String, queue_size=1)
    r = rospy.Rate(3)

    while not rospy.is_shutdown():
        print "Write 'C' for Clear"
        command_input = raw_input()
        if command_input == 'C':
            pub.publish("C")
            print("Clearing Look At Matrix")
        if command_input == 'R':
            pub.publish("R")
            print("Clearing Talking Persons")
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
