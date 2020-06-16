from src.mask import Mask
from src.graphCut import GraphCut
import cv2 as cv

print("Interactive Graph Cut for Computer Vision \nBased on Jolly and and Boykov Paper \n"
      "--------------------------------------------------------------------------------")

filename = 'src/img_test/bunny.jpg'

mask = Mask().makeMask(filename)

image = cv.imread(filename)

graph = GraphCut(image, mask)

print(mask)