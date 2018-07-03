import numpy as np
import cv2 as cv
import os

def edge_detect(photo):
	# Convert to gray BGR -> Gray:  Y = 0.299R + 0.587G + 0.114B
	b,g,r = cv.split(photo)
	gray 	 	= 0.299*r + 0.587*g + 0.114*b
	out = cv.Laplacian(gray,cv.CV_8U,ksize=5)
	return out

def sign_image(photo_filename, sign_filename, size = 0.16, hmargin = 2, wmargin = 1.2, opacity = [], verbose=False):

	photo = cv.imread(photo_filename)
	h, w, bbp = photo.shape

	sign = cv.imread(sign_filename,-1)
	hs0, ws0, bbs = sign.shape

	# Sizes of rsized image
	ws1 = int(size * w)
	hs1 = int(ws1 * hs0 / ws0)

	#Sizes of ROI to analyze
	roi_w = int(wmargin * ws1)
	roi_h = int(hmargin * hs1)

	corner	= np.zeros((4,	roi_h,			roi_w,			3))
	corner[0,:,:,:] = photo[0:roi_h,		0:roi_w,		:]
	corner[1,:,:,:] = photo[-roi_h-1:-1,	0:roi_w,		:]
	corner[2,:,:,:] = photo[0:roi_h, 		-roi_w-1:-1,	:]
	corner[3,:,:,:] = photo[-roi_h-1:-1, 	-roi_w-1:-1,	:]

	bright 		= np.zeros(4)
	edge_contr 	= np.zeros(4)

	# Analyze corners
	for k in range(4):
		# Convert to gray BGR -> Gray:  Y = 0.299R + 0.587G + 0.114B
		b,g,r = cv.split(corner[k,:,:,:])
		gray 	 		= 0.299*r + 0.587*g + 0.114*b
		bright[k] 		= np.mean(gray)
		edges 			= edge_detect(corner[k,:,:,:])
		edge_contr[k]	= np.std(edges)

	best_corner = np.argmin(edge_contr)

	# Compute auto opacity (only if opacity is not defined)
	if opacity == []:
		op_max = 0.9
		op_min = 0.3
		opacity = -2*(op_max-op_min)/256 * np.abs(bright[k]-128) + op_max

	if verbose:
		print(photo_filename)
		print('\t', end='')
		for k in range(4):
			print(k,"\t", end='')
		print("Best\tOp\nB:\t", end='')
		for k in range(4):
			print(round(bright[k], 2),"\t", end='')
		print(best_corner,"\t",round(opacity,3),"\nC:\t", end='')
		for k in range(4):
			print(round(edge_contr[k], 2),"\t", end='')
		print("")

	# Scale factors
	scale = ws1 / ws0
	# Resize signature
	sign = cv.resize(sign,(0,0),fx=scale,fy=scale,interpolation=cv.INTER_LANCZOS4)
	hs1, ws1 ,bbs = sign.shape

	photo_new = photo

	sig_l	= range(0 		+ int((wmargin - 1) * 0.5 * roi_w),
					ws1 	+ int((wmargin - 1) * 0.5 * roi_w))

	sig_r 	= range(-ws1 	- int((wmargin - 1) * 0.5 * roi_w),
					0 		- int((wmargin - 1) * 0.5 * roi_w))

	sig_u 	= range(0		+ int((hmargin - 1) * 0.5 * roi_h),
					hs1 	+ int((hmargin - 1) * 0.5 * roi_h))

	sig_d 	= range(-hs1 	- int((hmargin - 1) * 0.5 * roi_h),
					0 		- int((hmargin - 1) * 0.5 * roi_h))

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

	return photo_new

def get_files(path):
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			yield file
