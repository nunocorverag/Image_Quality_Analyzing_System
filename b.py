import cv2 as cv

CV_IMAGE = cv.imread('IMG/REF_23.PNG', cv.IMREAD_GRAYSCALE)
lst = []
for y in range(len(CV_IMAGE)):
    for x in range(len(CV_IMAGE[y])):
        lst.append(CV_IMAGE[y][x])
    
print(max(lst))

cv.imshow('IMAGE_QUALITY_ANALYZING_SYSTEM',CV_IMAGE)
cv.waitKey(0)