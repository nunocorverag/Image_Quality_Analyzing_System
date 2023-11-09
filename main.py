import cv2 as cv
import matplotlib.pyplot as plt

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

# Dibujar los contornos en una copia de la imagen original
ref_with_contours = cv.cvtColor(REF_IMG_GS, cv.COLOR_GRAY2BGR)
cv.drawContours(ref_with_contours, contours, -1, (0, 0, 255), 2)

# Dibujar el cuadro azul alrededor del área de interés
cv.rectangle(ref_with_contours, (X_MIN, Y_MIN), (X_MAX, Y_MAX), (255, 0, 0), 2)

# Dibujar los puntos de interés
print(f"Max x tuple coords: {max_x_tuple}")
print(f"Max y tuple coords: {max_y_tuple}")
plt.scatter(max_x_tuple[0], max_x_tuple[1], c='green', s=25)
plt.scatter(max_y_tuple[0], max_y_tuple[1], c='green', s=25)

##GRAFICAR ------------------------------------------------------------
# Trama de la imagen
plt.imshow(ref_with_contours, cmap='gray')
plt.title('Reference image in grey scale')
plt.show()