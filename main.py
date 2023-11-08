import cv2 as cv

image=cv.imread("IMG/REF_23.PNG",0)
cv.imshow("image", image)

cv.waitKey(0)
cv.destroyAllWindows()