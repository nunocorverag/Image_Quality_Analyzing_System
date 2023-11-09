import cv2 as cv
import luma

def nearest_point_center(borders, center):
    options = []
    for i in borders:
        options.append(((i[0] - center[0])**2 + (i[1] - center[1])**2)**(1/2))
    return borders[options.index(min(options))]

def get_brightness(image, point):
    
    pixel_brightness = []
    for y in range(point[1]-50,point[1]+50):
        for x in range(point[0]-50,point[0]+50):
            pixel_brightness.append(image[y][x])

    return max(pixel_brightness)
            
if __name__ == '__main__':
    image_name = 'IMG/REF_24.PNG'
    square_data = luma.get_square_data(image_name)
    point_to_get_brightness = nearest_point_center(square_data[1], square_data[3])
    print(get_brightness(square_data[0], point_to_get_brightness))
