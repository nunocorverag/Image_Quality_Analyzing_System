import cv2 as cv
import luma

def nearest_point_center(borders, center):
    options = []
    for i in borders:
        options.append(((i[0] - center[0])**2 + (i[1] - center[1])**2)**(1/2))
    return borders[options.index(min(options))], center

def get_brightness(image, point):
    
    pixel_r = []
    pixel_g = []
    pixel_b = []
    for y in range(point[1]-50,point[1]+50):
        for x in range(point[0]-50,point[0]+50):
            pixel_r.append(image[y][x][0])
            pixel_g.append(image[y][x][1])
            pixel_b.append(image[y][x][2])

    return (max(pixel_r), max(pixel_g), max(pixel_b))
            
if __name__ == '__main__':
    image_name = 'IMG/REF_23.PNG'
    color_image = cv.imread(image_name, cv.IMREAD_COLOR)
    square_data = luma.get_square_data(image_name)
    point_to_get_brightness,center = nearest_point_center(square_data[1], square_data[3])
    print(get_brightness(color_image, point_to_get_brightness))
