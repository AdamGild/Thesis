import argparse
import cv2
from opencv_calibration import load_coefficients
from tracking_function import track





if __name__ == '__main__':






    [camera_matrix, dist_matrix] = load_coefficients('camera.yml')
    track(camera_matrix, dist_matrix)
