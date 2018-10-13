import matplotlib.pyplot as plt
import time
from matplotlib import style
from itertools import islice

style.use('fivethirtyeight')
plt.show(block=False)
fig0 = plt.figure()
plt.draw()
plt.pause(0.01)
plots = {}

while True:
    global plots

    graph_data = open('test2.txt', 'r').read()
    lines = graph_data.split('\n')
    if not lines[0]:
        continue
    begin=lines[1].split(',')

    faces = {}

    for line in islice(lines,2,None):
        expressions = line.split(',')
        if len(line) > 1:

            time = round(((float(expressions[0]) - float(begin[0])) / 1000000000), 2)
            joy = round(float(expressions[1]), 2)
            x = int(float(expressions[110]))

            face_index=len(faces)
            print "Number Of Faces", face_index
            for index, timeline in faces.items():
                if timeline[0]['x'] > x-6 and timeline[0]['x'] < x+6:
                    face_index = index
                    break

            if face_index not in faces:
                faces[face_index] = []

            personality = {}
            personality["time"] = time
            personality["happy"] = joy
            personality["x"] = x

            faces[face_index].append(personality)

    # create new plots if more faces recognized
    if len(faces) > len(plots):
        plots = {}
        for index in xrange(len(faces)):
            plots[index] = plt.subplot(len(faces), 1, index + 1)

    for index, timeline in faces.items():
        xs = []
        ys = []
        for personality in timeline:
            xs.append(personality['time'])
            ys.append(personality['happy'])
        plot = plots[index]
        plot.clear()
        plot.plot(xs, ys)
        plt.pause(0.01)

    time.sleep(1)