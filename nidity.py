import pandas as pd
import numpy as np

from glob import glob

import cv2 as cv
import matplotlib.pylab as plt

reference_file = "IMG/REF_23.PNG"

reference_img_normscale = cv.imread(reference_file)
reference_img_grayscale = cv.imread(reference_file,cv.IMREAD_GRAYSCALE)

# img_to_analize_normalscale = cv.imread(file_to_analize)
# img_to_analize_grayscale  = cv.imread(file_to_analize,cv.IMREAD_GRAYSCALE)

#width --> 640px
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

def calculate_nidity(file):
    # Referencia del archivo
    REF_FILE = file

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

    # Obtain the ESF by collecting data
    esf_data = np.array(arr_pix_func_data)

    # Print the ESF function
    print("ESF Function:")
    print(esf_data)

    # Plot the ESF function
    x_values = esf_data[:, 0]
    y_values = esf_data[:, 1]

    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label='Función ESF')
    plt.xlabel('Número de Secuencia de Píxeles')
    plt.ylabel('Luminosidad del Píxel')
    plt.title('Función de Difusión de Borde (ESF)')
    plt.legend()
    plt.show()

    # Use spline interpolation to get a function representing the ESF
    x = np.arange(len(esf_data))
    spl = UnivariateSpline(x, y_values)
    lsf_function = spl.derivative()

    # Print the LSF function
    print("LSF Function:")
    print(lsf_function)

    # Calculate the LSF data from the derivative of the ESF function
    lsf_data = lsf_function(x)

    # Plot the LSF function
    # plt.figure(figsize=(8, 6))
    # plt.plot(x, lsf_data, label='LSF Function')
    # plt.xlabel('Pixel Sequence Number')
    # plt.ylabel('Rate of Pixel Luminosity Change')
    # plt.title('Line Spread Function (LSF)')
    # plt.legend()
    # plt.show()

    # Perform the Fourier transform of the LSF function to get the MTF data
    mtf_data = np.fft.fft(lsf_data)

    # Normalize the magnitude data by dividing by 255
    normalized_magnitude_data = np.abs(mtf_data) / 255

    # Create an array for the spatial frequencies
    spatial_frequency = np.fft.fftfreq(len(normalized_magnitude_data))

    # Consider only the positive x-axis values for the Fourier transform
    positive_freq = spatial_frequency > 0
    positive_magnitude = normalized_magnitude_data[positive_freq]


    # Create an array for the positive spatial frequencies
    positive_spatial_frequency = spatial_frequency[positive_freq]

    # Plot the MTF function with positive spatial frequencies
    plt.figure(figsize=(8, 6))
    plt.plot(positive_spatial_frequency, positive_magnitude, label='Función MTF')
    plt.xlabel('Frecuencia Espacial')
    plt.ylabel('Magnitud Normalizada')
    plt.title('Función de Transferencia de Modulación (MTF)')
    plt.legend()

    # Encuentra el índice más cercano en el que la magnitud es 0.5
    index_of_05 = np.argmin(np.abs(positive_magnitude - 0.5))

    # Obtiene el valor de x correspondiente al índice donde la magnitud es 0.5
    x_value_at_05 = positive_spatial_frequency[index_of_05]
    plt.show()

    return x_value_at_05

    # print(f"El valor de x cuando la magnitud es 0.5 en la función MTF es: {x_value_at_05}")


print(calculate_nidity("IMG/REF_23.PNG"))
