import numpy as np
import cv2
import cv2.aruco as aruco
from coordinates import rotate_marker_corners


def track(matrix_coefficients, distortion_coefficients, output_file):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file + '.avi', fourcc, 29, (1440,2560))
    cap = cv2.VideoCapture('instrument4.mp4')
    marker1 = []
    marker2 = []
    marker1N = []
    marker2N = []
    #marker3 = []
    #marker4 = []

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:

        # operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Change grayscale
            aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)  # Use 5x5 dictionary to find markers
            parameters = aruco.DetectorParameters_create()  # Marker detection parameters
            parameters.cornerRefinementMethod = 1
            # lists of ids and the corners belonging to each id
            corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict,
                                                                    parameters=parameters,
                                                                    cameraMatrix=matrix_coefficients,
                                                                    distCoeff=distortion_coefficients)


            if np.all(ids is not None):  # If there are markers found by detector
                for i in range(0, len(ids)):  # Iterate in markers
                    # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
                    rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners[i], 0.005, matrix_coefficients,
                                                                               distortion_coefficients)
                    (rvec - tvec).any()  # get rid of that nasty numpy value array error
                    normal = rotate_marker_corners(rvec, 0.005, tvec)
                    coords = tvec
                    if len(ids)==2:
                        if i==0:
                            if ids[0]==0:
                                marker1.append(coords)
                                marker1N.append(normal)
                            if ids[0]==1:
                                marker2.append(coords)
                                marker2N.append(normal)
                            # if ids[0]==2:
                            #     marker3.append(coords)
                            # if ids[0]==3:
                            #     marker4.append(coords)
                        if i==1:
                            if ids[1] == 0:
                                marker1.append(coords)
                                marker1N.append(normal)
                            if ids[1] == 1:
                                marker2.append(coords)
                                marker2N.append(normal)
                            # if ids[1] == 2:
                            #     marker3.append(coords)
                            # if ids[1] == 3:
                            #     marker4.append(coords)
                        # if i==2:
                        #     if ids[2] == 0:
                        #         marker1.append(coords)
                        #     if ids[2] == 1:
                        #         marker2.append(coords)
                        #     if ids[2] == 2:
                        #         marker3.append(coords)
                        #     if ids[2] == 3:
                        #         marker4.append(coords)
                        # if i==3:
                        #     if ids[3] == 0:
                        #         marker1.append(coords)
                        #     if ids[3] == 1:
                        #         marker2.append(coords)
                        #     if ids[3] == 2:
                        #         marker3.append(coords)
                        #     if ids[3] == 3:
                        #         marker4.append(coords)

                    aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
                    aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  # Draw Axis
            # Display the resulting frame
            out.write(frame)
            scale_percent = 55  # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow('frame', resized)

            # Wait 3 milisecoonds for an interaction. Check the key and do the corresponding job.
            key = cv2.waitKey(3) & 0xFF

            if key == ord('q'):  # Quit
                break
        else:
            break

        # When everything done, release the capture

    cap.release()
    out.release()
    #kekw
    cv2.destroyAllWindows()
    return marker1, marker2, marker1N, marker2N #marker3, marker4

