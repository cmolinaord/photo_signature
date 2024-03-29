import sys
import os
import numpy as np
import cv2 as cv
import tools as tool
import time as t
from PIL import	Image

args = sys.argv
folder_path = args[1]
sign_path = args[2]
dst_path = args[3]

t1 = t.time()

num_photos = len(os.listdir(os.getcwd()))
print("Processing", num_photos, "photos in", folder_path)
print("Using signature in", sign_path)

for filename in tool.get_files(folder_path):
	# Extract EXIF from original image
	im = Image.open(filename)
	exif_data = im.info['exif']

	# Run Signature tool
	signed = tool.sign_image(filename,sign_path,verbose=True)
	signed_filename = dst_path + "/" + filename
	cv.imwrite(signed_filename,signed)

	# Write EXIF on new image
	im_new = Image.open(signed_filename)
	im_new.save(signed_filename, 'JPEG', exif=exif_data)

t2 = t.time() - t1
print(" ")
print(num_photos,"photos processed in",round(t2,3),"s")
print("Signed photos saved in ",dst_path)
