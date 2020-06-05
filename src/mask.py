import sys
import numpy as np
import cv2 as cv

class App:

    def showImage(self):
        #if len(sys.argv) == 2:
        #    filename = sys.argv[1]
        #else:
        filename = 'src/img_test/mouette.png'

        image = cv.imread(filename, 0)
        cv.namedWindow('image', cv.WINDOW_NORMAL)
        cv.imshow('image', image)

        cv.waitKey(20000)