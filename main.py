import cv2 as cv
import matplotlib.pylab as plt 
import numpy as np
import pandas as pd

XCOORD_ORIENTATION=523
YCOORD_ORIENTATION=40

XCOORDMIN=150
XCOORDMAX=470
YCOORDMIN=90
YCOORDMAX=380

STANDARDCENTERX=174
STANDARDCENTERY=144

img_ori=cv.imread("IMG/36.PNG",1)
img = cv.cvtColor(img_ori, cv.COLOR_BGR2GRAY)
aoi=img[YCOORDMIN:YCOORDMAX,XCOORDMIN:XCOORDMAX]
aoi_orientation=img[YCOORD_ORIENTATION:YCOORD_ORIENTATION+30,XCOORD_ORIENTATION:XCOORD_ORIENTATION+30]

cv.imshow('asda',aoi)
cv.imshow('asda',aoi_orientation)

_, threshold=cv.threshold(aoi,20,250,cv.THRESH_BINARY)
contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
orientation_value=aoi_orientation[10,10]

XYcontour=[]
plt.imshow(threshold)

for contour in contours:
    contour_as_string=str(contour.flatten())
    contour_separated=contour_as_string.split(" ")
    for i in contour_separated:
        i=i.replace("[","")
        i=i.replace(" ","")
        i=i.replace("]","")
        i=i.replace("...","")
        if(len(i)<=3 and len(i)>0):
            i=int(i)
            XYcontour.append(i)
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        M = cv.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00'])   
    XYcontour=[]
print("Centrado?:")
if x<STANDARDCENTERX+10 and x>STANDARDCENTERX-10 and y>STANDARDCENTERY-10 and y<STANDARDCENTERY+10:
    print("TRUE")
else:
    print("FALSE")
print(x)
print(y)

print("Orientacion?")
if orientation_value<20:
    print("TRUE")
else:
    print("FALSE")
print(orientation_value)

cv.imshow('adsad',img)

plt.show()
#plt.show()

cv.waitKey(0)
cv.destroyAllWindows()