
import imageio
import matplotlib.pyplot as plt
from opencv_calibration import load_coefficients
from tracking_function import track
import sys
import numpy as np
import math
import os
from makeorigin import make_dashedLines




if __name__ == '__main__':




    output_file = sys.argv[1]
    [camera_matrix, dist_matrix] = load_coefficients('camera2.yml')
    marker1, marker2, marker1N, marker2N = track(camera_matrix, dist_matrix, output_file) #marker3, marker4




    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection="3d")
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('y')
    ax.set_xlim3d(-0.5, 0.5)
    ax.set_ylim3d(0, 1)
    ax.set_zlim3d(0, -1)




    for index in np.arange(0, len(marker1), 15):

        # if index == 0:
        color = "green"
        # if index == 60:
        #     color = "blue"
        # if index == 180:
        #     color = "red"
        # if index == 270:
        #     color = "black"
        # if index == 360:
        #     color = "yellow"
        # point1 = [marker1[index][0][0][0], marker1[index][0][0][1], marker1[index][0][0][2]]
        # point2 = [marker2[index][0][0][0], marker2[index][0][0][1], marker2[index][0][0][2]]
        # point3 = [marker3[index][0][0][0], marker3[index][0][0][1], marker3[index][0][0][2]]
        # point4 = [marker4[index][0][0][0], marker4[index][0][0][1], marker4[index][0][0][2]]
        x_points = [marker1[index][0][0][0], marker2[index][0][0][0]] #marker3[index][0][0][0], marker4[index][0][0][0]]
        y_points = [marker1[index][0][0][1], marker2[index][0][0][1]] #marker3[index][0][0][1], marker4[index][0][0][1]]
        z_points = [marker1[index][0][0][2], marker2[index][0][0][2]] #marker3[index][0][0][2], marker4[index][0][0][2]]

        x_points_marker1N = [(marker1N[index][0][0][0]+marker2N[index][0][0][0])/2]
        y_points_marker1N = [(marker1N[index][0][0][1]+marker2N[index][0][0][1])/2]
        z_points_marker1N = [(marker1N[index][0][0][2]+marker2N[index][0][0][2])/2]

        #x_points_marker2N = [marker2N[index][0][0][0]]
        #y_points_marker2N = [marker2N[index][0][0][1]]
        #z_points_marker2N = [marker2N[index][0][0][2]]

        points = ax.scatter3D(x_points, z_points, y_points, c=color)
        line = ax.plot(x_points, z_points, y_points, c=color)
        line = line.pop()

        axes = ax.quiver((marker1[index][0][0][0]+marker2[index][0][0][0])/2, (marker1[index][0][0][2]+marker2[index][0][0][2])/2, (marker1[index][0][0][1]+marker2[index][0][0][1])/2, x_points_marker1N, z_points_marker1N, y_points_marker1N,  length=0.05, normalize=True)
        #axes2 = ax.quiver(marker2[index][0][0][0], marker2[index][0][0][2], marker2[index][0][0][1], x_points_marker2N, z_points_marker2N, y_points_marker2N, length=0.05, normalize=True)

        text1 = ax.text(marker1[index][0][0][0], marker1[index][0][0][2], marker1[index][0][0][1], "1")
        text2 = ax.text(marker2[index][0][0][0], marker2[index][0][0][2], marker2[index][0][0][1], "2")
        #ax.text(marker3[index][0][0][0], marker3[index][0][0][1], marker3[index][0][0][2], "3")
        #ax.text(marker4[index][0][0][0], marker4[index][0][0][1], marker4[index][0][0][2], "4")
        plt.pause(1)
        points.remove()
        text1.remove()
        text2.remove()
        axes.remove()
        line.remove()
        #axes2.remove()
        print(x_points)
        print(z_points)
        print(y_points)
        distance = math.sqrt((x_points[0]-x_points[1])**2+(y_points[0]-y_points[1])**2+(z_points[0]-z_points[1])**2)
        print(distance)


    #

    plt.show()



