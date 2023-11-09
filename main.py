import pandas as pd
import numpy as np

from glob import glob

import cv2 as cv
import matplotlib.pylab as plt

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

aoi = REF_IMG_GS[Y_MIN:Y_MAX,X_MIN:X_MAX]

CENTER_AOI_Y = len(aoi) // 2
CENTER_AOI_X = len(aoi[0]) // 2

# Umbralizar la imagen
_, thresh = cv.threshold(aoi, 20, 255, cv.THRESH_BINARY_INV)

# Encontrar los contornos externos
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

print(contours[0][0][0][0])

# Dibujar los contornos en una copia de la imagen original
aoi_with_contours = cv.cvtColor(aoi, cv.COLOR_GRAY2BGR)
cv.drawContours(aoi_with_contours, contours, -1, (0, 255, 0), 2)

##GRAFICAR ------------------------------------------------------------
# Trama de la imagen
plt.imshow(aoi_with_contours, cmap='gray')
plt.title('Reference image in grey scale')

# Dibujar un punto gris en las coordenadas específicas
plt.scatter(CENTER_AOI_X, CENTER_AOI_Y, c='gray', s=25)

plt.show()

