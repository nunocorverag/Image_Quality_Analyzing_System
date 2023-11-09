import cv2 as cv
import luma

def nearest_point_center(borders, center):
    options = []
    for i in borders:
        options.append(((i[0] - center[0])**2 + (i[1] - center[1])**2)**(1/2))
    return borders[options.index(min(options))]

def get_brightness(image, point):
    
    pixel_brightness = []
    for y in range(point[1]-25,point[1]+26):
        for x in range(point[0]-25,point[0]+26):
            pixel_brightness.append(image[y][x])

    print(max(pixel_brightness))
    cv.line(image, (point[0]-25,point[1]-25), (point[0]+25,point[1]+25), (255,255,255), 6)
    cv.imshow('IMAGE_QUALITY_ANALYZING_SYSTEM',image)
    cv.waitKey(0)
            
if __name__ == '__main__':
    square_data = luma.get_square_data('IMG/REF_23.PNG')
    point_to_get_brightness = nearest_point_center(square_data[1], square_data[3])
    get_brightness(square_data[0], point_to_get_brightness)
