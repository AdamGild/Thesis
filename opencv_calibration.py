import numpy as np
import cv2
import glob


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def calibrate(dirpath, prefix, image_format, square_size, width, height):

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    #dirpath is the folder location of the image set

    if dirpath[-1:] == '/':
        dirpath = dirpath[:-1]

    images = glob.glob(dirpath+'/' + prefix + '*.' + image_format)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners

            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
            # if wanting to resize the image when it is displayed for dimension purposes, merely uncomment the code below and change scale percentage to your preference

            # scale_percent = 40  # percent of original size
            # framewidth = int(img.shape[1] * scale_percent / 100)
            # frameheight = int(img.shape[0] * scale_percent / 100)
            # dim = (framewidth, frameheight)
            #
            # # resize image
            #resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            cv2.imshow('ímg', img)  #change to cv2.imshow('img', resized) if resizing the image

            cv2.waitKey(500)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


    return [ret, mtx, dist, rvecs, tvecs]

def save_coefficients(mtx, dist, path):

    #function for saving the camera matrix and distortion coefficients matrix

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()

def load_coefficients(path):

    #function for loading the camera matrix and distortion coefficients, to be used in Reconstruction_main.py

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]