#Computer Graphics Assignment 01 => Project 10

#importing libraries
import cv2 
import numpy as np

#import parent image and template image
parent_image='../assets/room.png'
template_image='../assets/mask.png'

# Read the parent image 
mask = cv2.imread(parent_image)
img_parent = cv2.imread(parent_image)
img = cv2.imread(parent_image,0)

# Convert parent image to grayscale 
img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) 

# Read the template image
template = cv2.imread(template_image,0) 

# Store width and heigth of template in w and h 
w, h = template.shape[::-1]

# Store width and heigth of parent image in W and H 
W, H = img.shape[::-1]

# Perform match operations. 
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 

# Specify a threshold (to maintain accuracy level)
threshold = 0.79

# Store the coordinates of matched area in a numpy array 
cordinates = np.where( res >= threshold)

# filled mask with black color 
cv2.rectangle(mask, (0,0), (W, H), (0,0,0),-1)

# Draw detected areas on mask as white boxes. 
for pt in zip(*cordinates[::-1]):
    cv2.rectangle(mask, pt, (pt[0] + w, pt[1] + h), (255,255,255),-1) 

# Merge parent image with mask to provide the output.
img_parent = cv2.bitwise_and(img_parent, mask)

# Show the final image with the matched area.
cv2.imshow('Detected',img_parent)

