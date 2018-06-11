import sys
import numpy as np
import cv2 as cv

args = sys.argv
filename = args[1]

photo = cv.imread(filename)
h = photo.shape[0]
w = photo.shape[1]

roi_w = round(0.16 * w)
roi_h = round(0.08 * h)

corner 			= np.zeros((4,roi_h,roi_w,3))
corner[0,:,:,:] = photo[0:roi_h,	0:roi_w,:]
corner[1,:,:,:] = photo[-roi_h-1:-1,	0:roi_w,:]
corner[2,:,:,:] = photo[0:roi_h, 	-roi_w-1:-1,:]
corner[3,:,:,:] = photo[-roi_h-1:-1, 	-roi_w-1:-1,:]

# Corner: image in BGR

for k in range(0,4):
	# Convert to gray BGR -> Gray:  Y = 0.299R + 0.587G + 0.114B
	b,g,r = cv.split(corner[k,:,:,:])
	gray 	 	= 0.299*r + 0.587*g + 0.114*b
	lum_mean 	= np.mean(gray)
	lum_diff 	= np.max(gray) - np.min(gray)
	lum_std 	= np.std(gray)
	print("Corner ",k)
	print("  mean = ",lum_mean)
	print("  diff = ",lum_diff)
	print("  std = ",lum_std)
	print("  error = ",lum_std/lum_mean*100,"%")
	cv.imshow("Corner "+str(k),gray/256)

key = cv.waitKey(0)
if key == 13:
	cv.destroyAllWindows()
