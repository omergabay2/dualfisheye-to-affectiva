import matplotlib.pyplot as plt
import time
from matplotlib import style
from itertools import islice

global plots
style.use('fivethirtyeight')
plt.show(block=False)
fig0 = plt.figure(num='expressions')
plt.draw()
plt.pause(0.01)
plots = {}

while True:
    try:
        graph_data = open('data.txt', 'r').read()
        lines = graph_data.split('\n')
        if not lines[0]:
            continue
        begin = lines[1].split(',')

        faces = {}

        for line in islice(lines, 2, None):
            expressions = line.split(',')
            if len(line) > 1:

                times = round(((float(expressions[0]) - float(begin[0])) / 1000000000), 2)
                joy = round(float(expressions[1]), 2)

                #in order to change expression change the expression[]
                x = int(float(expressions[111-18]))
                face_index = len(faces)

                for index, timeline in faces.items():
                    if timeline[0]['x'] > x-80 and timeline[0]['x'] < x+80:
                        face_index = index
                        break

                if face_index not in faces:
                    faces[face_index] = []

                personality = {}
                personality["time"] = times
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
            this_plot = plots[index]
            this_plot.clear()
            this_plot.plot(xs, ys)
            this_plot.set_title("person %d x: %d" % ((index + 1), (timeline[0]['x'])))
            this_plot.set_ylabel("happy")
            this_plot.set_xlabel("time(s)")
            plt.tight_layout()
            plt.pause(0.01)

        time.sleep(1)
    except KeyboardInterrupt:
        print("Close plotting data ...")
        break
    except:
        print ("error")
