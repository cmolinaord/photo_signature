import numpy as np
import cv2

cropY = 0.08
cropX = 0.16

photo = cv2.imread('test/image.jpg')
height = photo.shape[0]
width = photo.shape[1]

corner1 = photo[0:round(cropY * height),	0:round(cropX * width)]
corner2 = photo[-round(cropY * height):-1,	0:round(cropX * width)]
corner3 = photo[0:round(cropY * height), 	-round(cropX * width):-1]
corner4 = photo[-round(cropY * height):-1, 	-round(cropX * width):-1]

# Mean by color
corner1.mean(axis=(0,1))


cv2.imshow("corner1",corner1)
cv2.imshow("corner2",corner2)
cv2.imshow("corner3",corner3)
cv2.imshow("corner4",corner4)

cv2.waitKey(10000)

# dst = cv.cvtColor(photo,COLOR_BGR2HSV)
