

import matplotlib.pyplot as plt
from opencv_calibration import load_coefficients
from tracking_function import track
import sys
import numpy as np
import math





if __name__ == '__main__':




    output_file = sys.argv[1]   #when running script, add Reconstruction_main.py output1 for example to make the name of the outputted avi video file output1

    [camera_matrix, dist_matrix] = load_coefficients('camera.yml')    #put name of calibration matrices file here
    marker1, marker2, marker1N, marker2N, total_frames = track(camera_matrix, dist_matrix, output_file)

    object_length = []
    camera_distance = []
    angle = []
    angle_pose = []
    shift_distance = []




    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection="3d")
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('y')


    ax.set_xlim3d(-0.5, 0.5)     #can change axes limits if the environment for tracking deems it necessary
    ax.set_ylim3d(0, 1)          #NOTE due to the format in which the object is plotted, the z points are plotted as y points and vice versa, meaning the z limits are actually the y limits and vice versa
    ax.set_zlim3d(0.5, -0.5)




    for index in np.arange(0, len(marker1), 15):   #plot a pose every half second


        x_points = [marker1[index][0][0][0], marker2[index][0][0][0]]
        y_points = [marker1[index][0][0][1], marker2[index][0][0][1]]
        z_points = [marker1[index][0][0][2], marker2[index][0][0][2]]

        x_points_markerN = [(marker1N[index][0][0][0]+marker2N[index][0][0][0])/2]   #averaging the two marker normals
        y_points_markerN = [(marker1N[index][0][0][1]+marker2N[index][0][0][1])/2]
        z_points_markerN = [(marker1N[index][0][0][2]+marker2N[index][0][0][2])/2]



        points = ax.scatter3D(x_points, z_points, y_points, c="green")  #plotting the two marker coordinates as points

        line = ax.plot(x_points, z_points, y_points, c="green")   #connecting the two markers with a line
        line = line.pop()

        #plotting the normal with midpoint of two markers as its origin
        axes = ax.quiver((marker1[index][0][0][0]+marker2[index][0][0][0])/2, (marker1[index][0][0][2]+marker2[index][0][0][2])/2, (marker1[index][0][0][1]+marker2[index][0][0][1])/2, x_points_markerN, z_points_markerN, y_points_markerN,  length=0.05, normalize=True)

        #labelling the two markers with their ids
        text1 = ax.text(marker1[index][0][0][0], marker1[index][0][0][2], marker1[index][0][0][1], "1")
        text2 = ax.text(marker2[index][0][0][0], marker2[index][0][0][2], marker2[index][0][0][1], "2")

        #removing all plots before updated for the next half-second
        plt.pause(1)
        points.remove()
        text1.remove()
        text2.remove()
        axes.remove()
        line.remove()



    for index in np.arange(0, len(marker1)):      #loop for calculating evaluation criteria

        x_points = [marker1[index][0][0][0], marker2[index][0][0][0]]
        y_points = [marker1[index][0][0][1], marker2[index][0][0][1]]
        z_points = [marker1[index][0][0][2], marker2[index][0][0][2]]

        x_points_markerN = [(marker1N[index][0][0][0] + marker2N[index][0][0][0]) / 2]  # averaging the two marker normals
        y_points_markerN = [(marker1N[index][0][0][1] + marker2N[index][0][0][1]) / 2]
        z_points_markerN = [(marker1N[index][0][0][2] + marker2N[index][0][0][2]) / 2]

        length = math.sqrt((x_points[0]-x_points[1])**2+(y_points[0]-y_points[1])**2+(z_points[0]-z_points[1])**2)   #euclidean distance from one marker to the other
        object_length.append(length)

        distance = ((z_points[0]+z_points[1])/2)   #average of the two markers z points to get the z coordinate of the object plane in the camera coordinate system
        camera_distance.append(distance)

        #collecting data for calculating the relative angle of the normal with the object
        length_vector = [(x_points[0]-x_points[1]), (y_points[0]-y_points[1]), (z_points[0]-z_points[1])]
        dot = np.dot(length_vector, [x_points_markerN, y_points_markerN, z_points_markerN])

        length_vector_mag = np.linalg.norm(length_vector)
        normal_mag = np.linalg.norm([x_points_markerN, y_points_markerN, z_points_markerN])

        relative_angle = np.arccos(dot/(length_vector_mag*normal_mag))  #using this data to calculate the relative angle of the normal with the object
        angle.append(relative_angle)

        #collecting data for calculating the relative angle of the object with its initial position
        if index==0:
            length_vector_2 = [(x_points[0]-x_points[1]), (y_points[0]-y_points[1]), (z_points[0]-z_points[1])]

        dot2 = np.dot(length_vector, length_vector_2)
        length_vector_2_mag = np.linalg.norm(length_vector_2)

        if index==0:    #to eliminate error at frame 0
            angle_pose.append(0)
        if index!=0:    #to eliminate error at frame 0
            relative_angle2 = np.arccos(dot2 / (length_vector_mag * length_vector_2_mag)) #using this data to calculate the relative angle of the object with its initial position
            angle_pose.append(relative_angle2*(180/math.pi))

        #collecting data to calculate shift along x axis

        if index==0:       #initial coordinate of centre of knife
            starting_coords = [(marker1[0][0][0][0]+marker2[0][0][0][0])/2, (marker1[0][0][0][2]+marker2[0][0][0][2])/2, (marker1[0][0][0][1]+marker2[0][0][0][1])/2]

        current_coords = [(marker1[index][0][0][0]+marker2[index][0][0][0])/2, (marker1[index][0][0][2]+marker2[index][0][0][2])/2, (marker1[index][0][0][1]+marker2[index][0][0][1])/2]
        shift = math.sqrt((current_coords[0] - starting_coords[0])**2 + (current_coords[1] - starting_coords[1])**2 + (current_coords[2] - starting_coords[2])**2)

        shift_distance.append(shift*100)



    #
    x = list(range(1,len(marker1)+1))

    plt.subplot(2,1,1)

    plt.title("Angle Relative to Starting Orientation")
    plt.xlabel("Frame")
    plt.ylabel("Angle (degrees)")
    plt.plot(x ,angle_pose, color = "red")

    plt.subplot(2,1,2)

    plt.title("Shift Distance from Starting Orientation")
    plt.xlabel("Frame")
    plt.ylabel("Shift Distance (cm)")
    plt.plot(x, shift_distance, color="red")

    plt.show()

    #Evaluation Data
    object_length_mean = np.mean(object_length)
    camera_distance_mean = np.mean(camera_distance)
    relative_angle_mean = (np.mean(angle))*(180/math.pi)
    ratio = (len(marker1))/total_frames

    print(object_length_mean)
    print(camera_distance_mean)
    print(relative_angle_mean)
    print(ratio*100)



