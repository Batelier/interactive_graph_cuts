import numpy as np
import cv2 as cv

class Mask():

    black = [0,0,0]         #color for background pixels
    white = [255,255,255]   #color for foreground pixels
    blue = [0, 0, 255]      #color for undefined pixels
    undefinedPixels = 0
    backgroundPixels = 1
    foregroundPixels = 2

    background = {'color' : black, 'value' : 1}
    foreground = {'color' : white , 'value' : 2}
    undefined = {'color' : blue, 'value' : 0}

    drawing = False #disable drawing while button isn't pressed
    drawingValue = foreground #by default indicate foreground
    drawingThickness = 3

    def mouseClicked(self, event, x, y, flags, parameters):

        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = True
            cv.circle(self.img, (x,y), self.drawingThickness, self.drawingValue['color'], -1)
            cv.circle(self.mask, (x,y), self.drawingThickness, self.drawingValue['value'], -1)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv.circle(self.img, (x, y), self.drawingThickness, self.drawingValue['color'], -1)
                cv.circle(self.mask, (x, y), self.drawingThickness, self.drawingValue['value'], -1)

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                cv.circle(self.img, (x, y), self.drawingThickness, self.drawingValue['color'], -1)
                cv.circle(self.mask, (x, y), self.drawingThickness, self.drawingValue['value'], -1)

    def makeMask(self, filename):
        windowName = 'drawing'

        print('WELCOME TO MASK CREATING')
        self.img = cv.imread(filename)
        self.imgCopy = self.img.copy() #save the input image in order to make reset possible
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) #initialize values to 0 = undefined
        cv.namedWindow(windowName)
        cv.setMouseCallback('drawing', self.mouseClicked) #enable use of mouse

        print('Foreground by default \n'
              'Press b to draw background \n'
              'Press f to draw foreground \n'
              'Press r to reset the drawing \n'
              'Press m to create the mask ')

        while(1):

            cv.imshow('drawing', self.img)
            pressedKey = cv.waitKey(1)

            if pressedKey == ord('b'): #indicate background pixels
                self.drawingValue = self.background
            elif pressedKey == ord('f'): #indicate foreground pixels
                self.drawingValue = self.foreground
            elif pressedKey == ord('r'): # reset everything
                print("Reset \n")
                self.drawing = False
                self.drawingValue = self.foreground
                self.img = self.imgCopy.copy()
                self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) #reinitialize the mask to undefined
            elif pressedKey == ord('m'):
                print('Mask editing finished')
                return self.mask  #, self.imgCopy