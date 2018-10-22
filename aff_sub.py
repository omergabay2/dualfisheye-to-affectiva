#! /usr/bin/python
import rospy
import time

from std_msgs.msg import String
from affdex_msgs.msg import AffdexFrameInfo, Vec2


# Instantiate CvBridge
new_data = str()
start_time = time.time()
faces = {}

def callback_affdex_data(msg):
    global new_data, faces
    face_index = len(faces)
    x_now = msg.face_points[26].x
    for index, timeline in faces.items():
        if timeline[0] > x_now - 80 and timeline[0] < x_now + 80:
            face_index = index
            break

    if face_index not in faces:
        faces[face_index] = []

    faces[face_index].append(x_now)

    new_data = "time:" + str(time.time() - start_time) + "," + "Person ID:" + str(face_index+1) + "," + "Location:" + str(msg.face_points[26].x) + "," + "Joy:" + str(msg.emotions[0]) + "," + "Anger:" + str(msg.emotions[1]) + "," + "Didgust:" + str(msg.emotions[2]) + "," + "Contempt:" + str(msg.emotions[3]) + "," + "Engagement:" + str(msg.emotions[4]) + "," + "Fear:" + str(msg.emotions[5]) + "," + "Sadness:" + str(msg.emotions[6]) + "," + "Surprise:" + str(msg.emotions[7]) + "," + "Valence:" + str(msg.emotions[8])
    print new_data

def main():
    rospy.init_node('affdex_data_edit', anonymous=True)
    rospy.Subscriber("/affdex_data", AffdexFrameInfo, callback_affdex_data)
    pub = rospy.Publisher("/omer_data", String, queue_size=1)
    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        pub.publish(new_data)
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
