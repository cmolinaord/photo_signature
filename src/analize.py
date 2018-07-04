#
# 0 ======== 2
# |          |
# |  photo   |
# |          |
# 1 ======== 3
#

import sys
import numpy as np
import cv2 as cv
import tools as tool

args = sys.argv
photo_path = args[1]
sign_path = args[2]

photo = cv.imread(photo_path)
cv.imshow("Photo_signed",photo)

signed = tool.sign_image(photo_path,sign_path,verbose=True)
cv.imshow("Signed",signed)

gradient = tool.edge_detect(signed)
cv.imshow("Gradient",gradient)

key = cv.waitKey(0)
if key == 13:
	cv.destroyAllWindows()
