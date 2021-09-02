import numpy as np
import cv2
import cv2.aruco as aruco


def track(matrix_coefficients, distortion_coefficients):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 29, (1080,1920))
    cap = cv2.VideoCapture('secondvid.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:

        # operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Change grayscale
            aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)  # Use 5x5 dictionary to find markers
            parameters = aruco.DetectorParameters_create()  # Marker detection parameters
            # lists of ids and the corners beloning to each id
            corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict,
                                                                    parameters=parameters,
                                                                    cameraMatrix=matrix_coefficients,
                                                                    distCoeff=distortion_coefficients)


            if np.all(ids is not None):  # If there are markers found by detector
                for i in range(0, len(ids)):  # Iterate in markers
                    # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
                    rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners[i], 0.025, matrix_coefficients,
                                                                               distortion_coefficients)
                    (rvec - tvec).any()  # get rid of that nasty numpy value array error
                    aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
                    aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.012)  # Draw Axis
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
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):  # Quit
                break
        else:
            break

        # When everything done, release the capture

    cap.release()
    out.release()

    cv2.destroyAllWindows()

