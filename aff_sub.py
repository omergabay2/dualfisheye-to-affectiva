#! /usr/bin/python
import rospy
import matplotlib.pyplot as plt
import time
from std_msgs.msg import String
from affdex_msgs.msg import AffdexFrameInfo, Vec2


new_data = str()
start_time = time.time()
faces = {}
plots = {}

def callback_affdex_data(msg):
    global new_data, faces, plots
    face_index = len(faces)
    x_now = msg.face_points[26].x

    for index, timeline in faces.items():
        if timeline[0]['x'] > x_now - 80 and timeline[0]['x'] < x_now + 80:
            face_index = index
            break
    if face_index not in faces:
        faces[face_index] = []

    times = time.time() - start_time

    personality = {}
    personality["Time"] = times
    personality["Joy"] = round(msg.emotions[0], 2)
    personality["x"] = x_now

    faces[face_index].append(personality)

    new_data = "time:" + str(times) + "," + "Person ID:" + str(face_index+1) + "," + "Location:" + str(msg.face_points[26].x) + "," + "Joy:" + str(msg.emotions[0]) + "," + "Anger:" + str(msg.emotions[1]) + "," + "Didgust:" + str(msg.emotions[2]) + "," + "Contempt:" + str(msg.emotions[3]) + "," + "Engagement:" + str(msg.emotions[4]) + "," + "Fear:" + str(msg.emotions[5]) + "," + "Sadness:" + str(msg.emotions[6]) + "," + "Surprise:" + str(msg.emotions[7]) + "," + "Valence:" + str(msg.emotions[8])
    print new_data

    if len(faces) > len(plots):
        plots = {}
        for index in xrange(len(faces)):
            plots[index] = plt.subplot(len(faces), 1, index + 1)

    for index, timeline in faces.items():
        xs = []
        ys = []
        for personality in timeline:
            xs.append(personality['Time'])
            ys.append(personality['Joy'])
        this_plot = plots[index]
        this_plot.clear()
        this_plot.plot(xs, ys)
        this_plot.set_title("person %d x: %d" % ((index + 1), (timeline[0]['x'])))
        this_plot.set_ylabel("Joy")
        this_plot.set_xlabel("Time(s)")
        plt.tight_layout()
        plt.pause(0.01)


def main():
    rospy.init_node('affdex_data_edit', anonymous=True)
    rospy.Subscriber("/affdex_data", AffdexFrameInfo, callback_affdex_data)
    pub = rospy.Publisher("/omer_data", String, queue_size=1)
    r = rospy.Rate(20)

    while not rospy.is_shutdown():
        pub.publish(new_data)
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
