import cv2 as cv
import matplotlib.pylab as plt 
import numpy as np
import pandas as pd

img=cv.imread("IMG/REF_23.PNG",0)
img_mpl =plt.imread('IMG/REF_23.PNG')
print(img.shape)
#pd.Series(img_mpl.flatten()).plot(kind='hist', bins=50, title= "PixelDistribution")
print(img_mpl.flatten()*255)
_, threshold=cv.threshold(img,50,255,cv.THRESH_BINARY)
print(threshold)
contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
fig, axs = plt.subplots(1,3,figsize=(15,5))
axs[0].imshow(img_mpl[:,:,0], cmap='Reds')
axs[1].imshow(img_mpl[:,:,1], cmap='Greens')
axs[2].imshow(img_mpl[:,:,2], cmap='Blues')
print(axs[0])
plt.imshow(threshold)
for contour in contours:
    print(contour)
    print(type(contour))
    cv.drawContours(img, [contour], 0, (0, 0, 255), 5) 
cv.imshow('adsad',img)
plt.show()
#plt.show()

cv.waitKey(0)
cv.destroyAllWindows()