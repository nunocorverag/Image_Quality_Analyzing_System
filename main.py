import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.interpolate import UnivariateSpline


def plot_pixel_luminosity_function(arr_pix_func):
    """Plots the pixel luminosity function."""
    x_values = []
    y_values = []
    for point in arr_pix_func:
        x_values.append(point[0])
        y_values.append(point[1])

    # Fit a polynomial of degree 1 to the data
    p = np.polyfit(x_values, y_values, 1)
    print(f"Function {p[0]} * x + {p[1]}")

    plt.plot(x_values, y_values)
    plt.xlabel("Pixel Sequence Number")
    plt.ylabel("Pixel Luminosity")
    plt.title("Pixel Luminosity Function")
    plt.show()

def calculate_esf(arr_pix_func):
    """Calculates the ESF function from an array of pixel luminance."""
    arr_pix_func = np.array(arr_pix_func)
    # Normalize the pixel luminance array
    arr_pix_func_norm = arr_pix_func[:, 1] / np.sum(arr_pix_func[:, 1])

    # Calculate the ESF as the cumulative sum of normalized luminance values
    esf = np.cumsum(arr_pix_func_norm)

    return esf

# Referencia del archivo
REF_FILE = "IMG/1.PNG"

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

#Length to check in area x
length_to_check = 25

# Imprimir los puntos de per_list_tuple que están 25 píxeles a la izquierda y derecha de la línea entre max_x_tuple y max_y_tuple, con la misma coordenada y
for point in per_list_tuple:
    x = point[0]
    y = point[1]
    # print(f"Point: {point}")
    # Dibujar un círculo en los puntos
    right_paralel.append((x+length_to_check,y))
    left_paralel.append((x-length_to_check,y))
    cv.circle(ref_with_contours, (x + 100 ,y), 1, (0, 255, 255), -1)
    cv.circle(ref_with_contours, (x - 100 ,y), 1, (0, 255, 255), -1)

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

print(f"Middle lp: {middle_lp}")
print(f"Middle rp: {middle_rp}")

# Array of the function to calculate the change in luminosity
arr_pix_func_data = []
y = middle_lp[1]
cont = 0
for x in range(middle_lp[0], middle_rp[0]):
    cont += 1
    lum_pix = REF_IMG_GS[y][x]
    arr_pix_func_data.append((cont, lum_pix))

# Obtain the ESF by normalizing data

esf_data = calculate_esf(arr_pix_func_data)

# Use spline interpolation to get a function representing the ESF
x = np.arange(len(esf_data))
spl = UnivariateSpline(x, esf_data)
lsf_function = spl.derivative()
print("derivative:",lsf_function)

# Perform the Fourier transform of the LSF function
lsf_data = lsf_function(x)
mtf_data = np.fft.fft(lsf_data)

# Calculate the magnitude for each spatial frequency
magnitude_data = np.abs(mtf_data)
# Create an array for the spatial frequencies
spatial_frequency = np.fft.fftfreq(len(magnitude_data))

# Find indices where spatial frequency is non-negative
positive_indices = np.where(spatial_frequency >= 0)

# Take only the positive values
positive_spatial_frequency = spatial_frequency[positive_indices]
positive_magnitude_data = magnitude_data[positive_indices]

# Find the x value where y is 0.5
half_point_x = positive_spatial_frequency[np.where(positive_magnitude_data > 0.5)[0][0]]
print("The x value where y is 0.5:", half_point_x)

# Plot the curve of MTF
plt.plot(positive_spatial_frequency, positive_magnitude_data)
plt.xlabel("Spatial Frequency")
plt.ylabel("Magnitude")
plt.title("MTF Curve")
plt.show()


# plt.scatter(middle_rp[0], middle_rp[1], c='grey', s=25)
# plt.scatter(middle_lp[0], middle_lp[1], c='grey', s=25)

# # left_paralel_upper_tuple = right_paralel[mid_x - 25]
# # left_paralel_lower_tuple = right_paralel[mid_x + 25]

# # right_paralel_upper_tuple = right_paralel[mid_x - 25]
# # right_paralel_lower_tuple = right_paralel[mid_x + 25]

# plt.scatter(up_rp[0], up_rp[1], c='yellow', s=25)
# plt.scatter(down_rp[0], down_rp[1], c='yellow', s=25)
# plt.scatter(up_lp[0], up_lp[1], c='yellow', s=25)
# plt.scatter(down_lp[0], down_lp[1], c='yellow', s=25)

# # Dibujar la línea entre up_rp y up_lp
# cv.line(ref_with_contours, (up_rp[0], up_rp[1]), (up_lp[0], up_lp[1]), (255, 255, 0), 2)
# cv.line(ref_with_contours, (down_rp[0], down_lp[1]), (down_lp[0], down_lp[1]), (255, 255, 0), 2)

# #Dibujar la linea roja
# cv.line(ref_with_contours, (middle_rp[0], middle_rp[1]), (middle_lp[0], middle_lp[1]), (255, 0, 0), 2)

# # Dibujar el punto a mitad
# plt.scatter(mid_x, mid_y, c='red', s=25)

# # Dibujar los contornos en una copia de la imagen original
# cv.drawContours(ref_with_contours, contours, -1, (0, 0, 255), 2)

# # Dibujar el cuadro azul alrededor del área de interés
# cv.rectangle(ref_with_contours, (X_MIN, Y_MIN), (X_MAX, Y_MAX), (255, 0, 0), 2)

# # Dibujar los puntos de interés
# # print(f"Max x tuple coords: {max_x_tuple}")
# # print(f"Max y tuple coords: {max_y_tuple}")
# plt.scatter(max_x_tuple[0], max_x_tuple[1], c='green', s=25)
# plt.scatter(max_y_tuple[0], max_y_tuple[1], c='green', s=25)

# ##GRAFICAR ------------------------------------------------------------
# # Trama de la imagen
# plt.imshow(ref_with_contours, cmap='gray')
# plt.title('Reference image in grey scale')
# # Dibujar las líneas offset

# offset = 25

# # plt.show()