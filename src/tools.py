import numpy as np
import cv2 as cv

def edges(photo):
	# Convert to gray BGR -> Gray:  Y = 0.299R + 0.587G + 0.114B
	b,g,r = cv.split(photo)
	gray 	 	= 0.299*r + 0.587*g + 0.114*b
	out = cv.Laplacian(gray,cv.CV_8U,ksize=5)
	return out
