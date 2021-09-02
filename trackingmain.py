import argparse
import cv2
from opencv_calibration import load_coefficients
from tracking_function import track
import sys




if __name__ == '__main__':




    output_file = sys.argv[1]
    [camera_matrix, dist_matrix] = load_coefficients('camera.yml')
    track(camera_matrix, dist_matrix, output_file)

