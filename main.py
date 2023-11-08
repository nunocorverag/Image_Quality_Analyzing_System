import cv2 as cv
import matplotlib.pylab as plt 
import numpy as np
import pandas as pd

img=cv.imread("IMG/36.PNG",0)
#pd.Series(img_mpl.flatten()).plot(kind='hist', bins=50, title= "PixelDistribution")
_, threshold=cv.threshold(img,20,250,cv.THRESH_BINARY)
contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
print(img[374,314])
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

    if XYcontour[0]<450 and XYcontour[0]>150 and XYcontour[1]<350 and XYcontour[1]>100:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        M = cv.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00']) 
    XYcontour=[]
cv.imshow('adsad',img)
print(x)
print(y)
plt.show()
#plt.show()

cv.waitKey(0)
cv.destroyAllWindows()