import cv2 as cv
import matplotlib.pyplot as plt
import math

# Referencia del archivo
REF_FILE = "IMG/REF_23.PNG"

# Cambiar para recibir una entrada
FILE_TO_ANALIZE = "IMG/REF_11.PNG"

# Imagen de referencia en escala de grises
REF_IMG_GS = cv.imread(REF_FILE, cv.IMREAD_GRAYSCALE)

# Height 480
# Width 640
# print(REF_IMG_GS.shape)

X_MIN = 150
Y_MIN = 80

X_MAX = 500
Y_MAX = 380
#Area of interest

# Recorta la imagen a la región de interés
aoi = REF_IMG_GS[Y_MIN:Y_MAX, X_MIN:X_MAX]

# Umbralizar la imagen
_, thresh = cv.threshold(aoi, 20, 255, cv.THRESH_BINARY_INV)

# Encontrar los contornos externos
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

ref_with_contours = cv.cvtColor(REF_IMG_GS, cv.COLOR_GRAY2BGR)

# Ajustar las coordenadas del contorno al área de interés original
max_x = None
max_y = None

max_x_tuple = None
max_y_tuple = None

for contour in contours:
    for point in contour:
        # print(f"x: {point[0][0]}, y: {point[0][1]}")
        point[0][0] += X_MIN
        point[0][1] += Y_MIN

        x = point[0][0]
        y = point[0][1]

        #Find the max x and max y and assign them coords (To find the edges --> top-right and bottom-left)
        if max_x == None:
            max_x = x
            max_y = y

        if max_x <= x:
            max_x = x
            max_x_tuple = (x,y)

        if max_y <= y:
            max_y = y
            max_y_tuple = (x,y)
# Calcular el punto a mitad
mid_x = (max_x_tuple[0] + max_y_tuple[0]) // 2
mid_y = (max_x_tuple[1] + max_y_tuple[1]) // 2

#Perpendicular list tuple
per_list_tuple = []

for contour in contours:
    for point in contour:

        x = point[0][0]
        y = point[0][1]

        if x >= max_y_tuple[0] and x <= max_x_tuple[0] and y >= max_x_tuple[1]:
            per_list_tuple.append((x,y))

# for x,y in per_list_tuple:
#     print(f"X: {x}, Y: {y}")

# print(f"Length of list: {len(per_list_tuple)}")

right_paralel = []
left_paralel = []

# Imprimir los puntos de per_list_tuple que están 25 píxeles a la izquierda y derecha de la línea entre max_x_tuple y max_y_tuple, con la misma coordenada y
for point in per_list_tuple:
    x = point[0]
    y = point[1]
    # print(f"Point: {point}")
    # Dibujar un círculo en los puntos
    right_paralel.append((x+25,y))
    left_paralel.append((x-25,y))
    cv.circle(ref_with_contours, (x + 25 ,y), 1, (0, 255, 255), -1)
    cv.circle(ref_with_contours, (x - 25 ,y), 1, (0, 255, 255), -1)

#Length of paralels
length_rp = len(right_paralel)
mid_rp = length_rp//2-1
middle_rp = right_paralel[mid_rp]
up_rp = right_paralel[mid_rp-25]
down_rp = right_paralel[mid_rp+25]

length_lp = len(left_paralel)
mid_lp = length_lp//2-1
middle_lp = left_paralel[mid_lp]
up_lp = left_paralel[mid_lp-25]
down_lp = left_paralel[mid_lp+25]

plt.scatter(middle_rp[0], middle_rp[1], c='grey', s=25)
plt.scatter(middle_lp[0], middle_lp[1], c='grey', s=25)

print(f"Middle line: {mid_x, mid_y}")
print(f"Middle rp: {middle_rp}")

# left_paralel_upper_tuple = right_paralel[mid_x - 25]
# left_paralel_lower_tuple = right_paralel[mid_x + 25]

# right_paralel_upper_tuple = right_paralel[mid_x - 25]
# right_paralel_lower_tuple = right_paralel[mid_x + 25]

plt.scatter(up_rp[0], up_rp[1], c='green', s=25)
plt.scatter(down_rp[0], down_rp[1], c='green', s=25)
plt.scatter(up_lp[0], up_lp[1], c='green', s=25)
plt.scatter(down_lp[0], down_lp[1], c='green', s=25)

# Dibujar el punto a mitad
plt.scatter(mid_x, mid_y, c='red', s=25)

# Dibujar los contornos en una copia de la imagen original
cv.drawContours(ref_with_contours, contours, -1, (0, 0, 255), 2)

# Dibujar el cuadro azul alrededor del área de interés
cv.rectangle(ref_with_contours, (X_MIN, Y_MIN), (X_MAX, Y_MAX), (255, 0, 0), 2)

# Dibujar los puntos de interés
# print(f"Max x tuple coords: {max_x_tuple}")
# print(f"Max y tuple coords: {max_y_tuple}")
plt.scatter(max_x_tuple[0], max_x_tuple[1], c='green', s=25)
plt.scatter(max_y_tuple[0], max_y_tuple[1], c='green', s=25)

##GRAFICAR ------------------------------------------------------------
# Trama de la imagen
plt.imshow(ref_with_contours, cmap='gray')
plt.title('Reference image in grey scale')
# Dibujar las líneas offset

offset = 25

plt.show()