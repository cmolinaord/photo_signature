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

# Opacity multiplier of the signature
opacity = 0.5

# Input values
reduc = 0.16  # subimage relative width
roi_margin_h = 2
roi_margin_w = 1.2

args = sys.argv
filename = args[1]

photo = cv.imread(filename)
h, w, bbp = photo.shape

sign = cv.imread("signature/cmolina.png",-1)
hs0, ws0, bbs = sign.shape

# Sizes of rsized image
ws1 = int(reduc * w)
hs1 = int(ws1 * hs0 / ws0)

#Sizes of ROI to analyze
roi_w = int(roi_margin_w * ws1)
roi_h = int(roi_margin_h * hs1)

corner	= np.zeros((4,	roi_h,			roi_w,			3))
corner[0,:,:,:] = photo[0:roi_h,		0:roi_w,		:]
corner[1,:,:,:] = photo[-roi_h-1:-1,	0:roi_w,		:]
corner[2,:,:,:] = photo[0:roi_h, 		-roi_w-1:-1,	:]
corner[3,:,:,:] = photo[-roi_h-1:-1, 	-roi_w-1:-1,	:]

bright 		= np.zeros(4)
edge_contr 	= np.zeros(4)

# Analyze corners
for k in range(0,4):
	# Convert to gray BGR -> Gray:  Y = 0.299R + 0.587G + 0.114B
	b,g,r = cv.split(corner[k,:,:,:])
	gray 	 		= 0.299*r + 0.587*g + 0.114*b
	bright[k] 		= np.mean(gray)
	edges 			= tool.edges(corner[k,:,:,:])
	edge_contr[k]	= np.std(edges)
	print("Corner", k)
	print("  brightness =", round(bright[k], 2))
	print("  Contrast of edges =", round(edge_contr[k], 2))


best_corner = np.argmin(edge_contr)
print("The best corner to put your signature is", best_corner)

# Scale factors
scale = ws1 / ws0
# Resize signature
sign = cv.resize(sign,(0,0),fx=scale,fy=scale,interpolation=cv.INTER_LANCZOS4)
hs1, ws1 ,bbs = sign.shape

cv.imshow("Photo",photo)

photo_new = photo

sig_l	= range(0 		+ int((roi_margin_w - 1) * 0.5 * roi_w),
				ws1 	+ int((roi_margin_w - 1) * 0.5 * roi_w))

sig_r 	= range(-ws1 	- int((roi_margin_w - 1) * 0.5 * roi_w),
				0 		- int((roi_margin_w - 1) * 0.5 * roi_w))

sig_u 	= range(0		+ int((roi_margin_h - 1) * 0.5 * roi_h),
				hs1 	+ int((roi_margin_h - 1) * 0.5 * roi_h))

sig_d 	= range(-hs1 	- int((roi_margin_h - 1) * 0.5 * roi_h),
				0 		- int((roi_margin_h - 1) * 0.5 * roi_h))

if best_corner == 0:
	nx, ny = np.meshgrid(sig_l,sig_u)
elif best_corner == 1:
	nx, ny = np.meshgrid(sig_l,sig_d)
elif best_corner == 2:
	nx, ny = np.meshgrid(sig_r,sig_u)
else:
	nx, ny = np.meshgrid(sig_r,sig_d)

sign_rgb = sign[:,:,:3]
sign_alpha = sign[:,:,-1]
# The signature is expected to be black over a transparent background
# This is good for bright corners
# So we keep the same colors for bright corners, but we invert the colors, if the
# corner is a darker one.
if bright[best_corner] < 128:
	sign_rgb = 255 - sign_rgb

a = (sign_alpha * opacity)/256
for c in range(3):
	photo_new[ny,nx,c] = (1-a)*photo[ny,nx,c] + a*sign_rgb[:,:,c]

cv.imshow("Photo_signed",photo_new)

gradient = tool.edges(photo_new)
cv.imshow("Gradient",gradient)

key = cv.waitKey(0)
if key == 13:
	cv.destroyAllWindows()
