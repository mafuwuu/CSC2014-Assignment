import numpy as np 
import cv2
from matplotlib import pyplot as pt

#load the image
image = cv2.imread('008.png')

# grayscale
result = image.copy()
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# adaptive threshold
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)

# Detects tables within images
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

# Reduces noise within image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

# Remove non-text contours by filling in the contour
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Filling rectangles with white
for c in cnts:
    cv2.drawContours(image,[c], 0, (255,255,255), -1)
 
#saves result into jpg    
cv2.imwrite('testing.jpg', image)
# DO NOT DELETE THIS !!!

# Load the image
img = cv2.imread('testing.jpg')

# convert to grayscale
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# smooth the image to avoid noises
grey = cv2.medianBlur(grey,5)

# Apply adaptive threshold
thresh = cv2.adaptiveThreshold(grey, 255, 1, 1, 11, 3)

# apply some dilation and erosion to join the gaps
kernel = np.ones((7,9), np.uint8)
thresh = cv2.dilate(thresh, kernel ,iterations = 10)

# Find the contours
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# For each contour, draw the rectangle
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    # pixels more than 10
    if h > 10:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        
#everyone has dif path
path = 'C:\\Users\\NEW\\Desktop\\Digital Image\\Proj\\Q2\\Cont'

for i in range(len(contours)):
    # get contour
    cnt = contours[i]
    # get the dimensions of the boundingRect
    x,y,w,h = cv2.boundingRect(cnt)
    # create a subimage based on boundingRect
    sub_img = img[y:y+h,x:x+w]
    # save image of contour with indexed name
    cv2.imwrite(path + "\contour_"+str(i)+".jpg", sub_img)

pt.imshow(img)
pt.show()