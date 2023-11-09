#LibraryImports

import cv2 as cv #Importing openCV as cv
import matplotlib.pylab as plt #Importing matplotlyb.pylab as plt
import numpy as np #Importing numpy as np

#Constant Declarations:
#Coordinates to determine the size of the image created for evaluating the orientation
XCOORD_ORIENTATION=523 #Coordinate of the upper corner in X
YCOORD_ORIENTATION=40  #Coordinate of the upper corner in Y

#Coordinates to determine the size of the image created for evaluating the centered value
XCOORDMIN=150 #Coordinate of the upper-left corner in X
XCOORDMAX=470 #Coordinate of the upper-right corner in X
YCOORDMIN=90  #Coordinate of the upper corner in Y
YCOORDMAX=380 #Coordinate of the lower corner in Y

#Coordinates of the center in the reference image
STANDARDCENTERX=174 #Coordinate of the center in X
STANDARDCENTERY=144 #Coordinate of the center in Y

#----------------------------------------------------Code------------------------------------------------------------

#Declaration of important variables
img_ori=cv.imread("IMG/36.PNG",1) #Opening the image using openCV
img = cv.cvtColor(img_ori, cv.COLOR_BGR2GRAY) #Transforming the image into gray scale
aoi=img[YCOORDMIN:YCOORDMAX,XCOORDMIN:XCOORDMAX] #Creating an AOI (area of interest) with a more centered image in order to analize
#less amount of pixels
aoi_orientation=img[YCOORD_ORIENTATION:YCOORD_ORIENTATION+30,XCOORD_ORIENTATION:XCOORD_ORIENTATION+30] #Creating an AOI that contains
#The border of the image to indicate orientation

#Showing the images as an example
cv.imshow('asda',aoi) #Showing the image of the AOI
cv.imshow('asda',aoi_orientation) #Showing the image of the AOI used for orientation

_, threshold=cv.threshold(aoi,20,250,cv.THRESH_BINARY)#creating a threshold that reduces the amount of colored pixels so that only
#the black ones stay with their original color
contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #Creating contours of the figures
#That the image processing in the library is able to identify, this creates a matrix that contains more matrixes 
#Containing the coordinates of the identified contours 
orientation_value=aoi_orientation[10,10] #Obtaining the color of the orientation image to be certain whether it is
#correctly orientated

XYcontour=[] #Creating an array that will contain the border coordinates in X and Y
plt.imshow(threshold) #Showing the resulting threshold image as a reference

for contour in contours: #Dividing the matrix of contours into single contours
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True) #Approximates the contour to a known figure
    M = cv.moments(contour) #Creates diferent moments of the figure including centroid and total area
    if M['m00'] != 0.0: #If the moment is not the one representing total area
        x = int(M['m10']/M['m00']) #The coordinate X is equal to one of the centroid coordinates divided by the total area 
        y = int(M['m01']/M['m00']) #The coordinate of Y is equal to one of the centroid coordinates divided by the total area
print("Centrado?:")
if x<STANDARDCENTERX+10 and x>STANDARDCENTERX-10 and y>STANDARDCENTERY-10 and y<STANDARDCENTERY+10: #Checks whether the values
#Calculated from the center enter in an area of 100 u^2 from the original center
    print("TRUE") #Print true if the condition is reached
else:#If the condition is not reached
    print("FALSE")#Print false
print(x)
print(y)

print("Orientacion?")
if orientation_value<20: #Checks whether the black square indicating orientation is there or not by checking if the pixels are
#black
    print("TRUE")
else:
    print("FALSE")
print(orientation_value)

cv.imshow('adsad',img)

plt.show()
#plt.show()

cv.waitKey(0)
cv.destroyAllWindows()