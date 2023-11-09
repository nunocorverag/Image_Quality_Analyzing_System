import cv2 as cv

def search_border(image,dir,starting_point_x,starting_point_y, differential):

    last_i = 0
    
    i = starting_point_x
    while abs(int(image[starting_point_y][i]) - last_i) < 15:
        last_i = image[starting_point_y][i]
        i += differential * dir

    i -= int(differential / 2 * dir)
    last_i = image[starting_point_y][i]
    while abs(int(image[starting_point_y][i]) - last_i) < 15:
        last_i = image[starting_point_y][i]
        i += 1 * dir

    return (i - 1 * dir, starting_point_y)

def search_border_y(image,dir,starting_point_x,starting_point_y, differential):

    last_i = 0
    
    i = starting_point_y
    while abs(int(image[i][starting_point_x]) - last_i) < 15:
        last_i = image[i][starting_point_x]
        i += differential * dir

    i -= int(differential / 2 * dir)
    last_i = image[i][starting_point_x]
    while abs(int(image[i][starting_point_x]) - last_i) < 15:
        last_i = image[i][starting_point_x]
        i += 1 * dir

    return (starting_point_x, i - 1 * dir)

nice_one = cv.imread('IMG/22.PNG', cv.IMREAD_GRAYSCALE)

dimension = nice_one.shape
height = int(dimension[0])
lenght = int(dimension[1])
half_height = int(height / 2)
half_lenght = int(lenght / 2)
DIFFERENTIAL = 20

check_point = search_border_y(nice_one, -1, half_lenght, half_height, DIFFERENTIAL)
check_point2 = search_border(nice_one, -1, check_point[0], check_point[1], DIFFERENTIAL)

borders = []

check_point = search_border_y(nice_one, 1, check_point2[0], check_point2[1], DIFFERENTIAL)
borders.append(check_point)
check_point2 = search_border(nice_one, 1, check_point[0], check_point[1], DIFFERENTIAL)
borders.append(check_point2)
check_point = search_border_y(nice_one, -1, check_point2[0], check_point2[1], DIFFERENTIAL)
borders.append(check_point)
check_point2 = search_border(nice_one, -1, check_point[0], check_point[1], DIFFERENTIAL)
borders.append(check_point2)

for i in borders:
    cv.line(nice_one, i, i, (255,255,255), 6)
    cv.putText(nice_one, str(borders.index(i)), i, cv.FONT_HERSHEY_SIMPLEX , 0.5, (255, 255, 255), 2)
center = (borders[0][0] + int(abs(borders[3][1] - borders[0][1])/2), borders[0][1] - int(abs(borders[3][0] - borders[2][0])/2))
print('borders: ', borders, 'center: ', center)
cv.putText(nice_one, 'center', center, cv.FONT_HERSHEY_SIMPLEX , 0.5, (255, 255, 255), 2)
cv.line(nice_one, center, center, (255,255,255), 6)

cv.imshow('lol',nice_one)
cv.waitKey(0)