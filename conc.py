#! /usr/bin/python
import rospy
from std_msgs.msg import String



pub = rospy.Publisher("/omer_conc", String, queue_size=1)

def callback_conc_data(msg):
    names = str(msg).split(",")
    for word in names:
        new_data = word
        pub.publish(new_data)


def main():
    rospy.init_node('omer_get_conc', anonymous=True)
    rospy.Subscriber("/omer_data", String, callback_conc_data)

    r = rospy.Rate(3)
    while not rospy.is_shutdown():
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

