import cv2 as cv

def search_border_x(image,dir,starting_point_x,starting_point_y, differential):

    last_i = 0
    i = starting_point_x

    for loop in range(2):
        while abs(int(image[starting_point_y][i]) - last_i) < 50:
            last_i = image[starting_point_y][i]
            if loop == 0:
                i += differential * dir
            else:
                i += 1 * dir

        if loop == 1: break

        i -= int(differential* dir)
        last_i = image[starting_point_y][i]

    return (i - 3 * dir, starting_point_y)

def search_border_y(image,dir,starting_point_x,starting_point_y, differential):

    last_i = 0
    i = starting_point_y

    for loop in range(2):
        
        while abs(int(image[i][starting_point_x]) - last_i) < 50:
            last_i = image[i][starting_point_x]
            if loop == 0:
                i += differential * dir
            else:
                i += 1 * dir

        if loop == 1: break

        i -= int(differential* dir)
        last_i = image[i][starting_point_x]

    return (starting_point_x, i - 3 * dir)

def get_square_data(image):
    CV_IMAGE = cv.imread(image, cv.IMREAD_GRAYSCALE)

    DIMENSION = CV_IMAGE.shape
    HEIGHT = int(DIMENSION[0])
    LENGHT = int(DIMENSION[1])
    HALF_HEIGHT = int(HEIGHT / 2)
    HALF_LENGHT = int(LENGHT / 2)
    DIFFERENTIAL = 10

    check_point = search_border_y(CV_IMAGE, -1, HALF_LENGHT, HALF_HEIGHT, DIFFERENTIAL)
    check_point2 = search_border_x(CV_IMAGE, -1, check_point[0], check_point[1], DIFFERENTIAL)

    borders = []
    direction = 1

    for i in range(2):
        check_point = search_border_y(CV_IMAGE, direction, check_point2[0], check_point2[1], DIFFERENTIAL)
        borders.append(check_point)
        check_point2 = search_border_x(CV_IMAGE, direction, check_point[0], check_point[1], DIFFERENTIAL)
        borders.append(check_point2)
        direction = -1

    ##for i in borders:
    ##    cv.line(CV_IMAGE, i, i, (255,255,255), 6)
    ##    cv.putText(CV_IMAGE, str(borders.index(i)), i, cv.FONT_HERSHEY_SIMPLEX , 0.5, (255, 255, 255), 2)

    CENTER = (borders[0][0] + int(abs(borders[3][1] - borders[0][1])/2), borders[0][1] - int(abs(borders[3][0] - borders[2][0])/2))

    ##print('borders: ', borders, 'CENTER: ', CENTER)

    ##cv.putText(CV_IMAGE, 'CENTER', CENTER, cv.FONT_HERSHEY_SIMPLEX , 0.5, (255, 255, 255), 2)

    ##cv.line(CV_IMAGE, CENTER, CENTER, (255,255,255), 6)

    return (CV_IMAGE, borders, CENTER, (HALF_LENGHT, HALF_HEIGHT))

if __name__ == '__main__':
    square_data = get_square_data('IMG/REF_23.PNG')
    cv.imshow('IMAGE_QUALITY_ANALYZING_SYSTEM',square_data[0])
    cv.waitKey(0)