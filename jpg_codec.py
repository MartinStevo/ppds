from __future__ import division
from PIL import Image
from numba import cuda
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import dct, idct
import math
import cv2


def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


@cuda.jit
def my_kernel_2D_div(io_array, Q):
    x, y = cuda.grid(2)
    if x < io_array.shape[0] and y < io_array.shape[1]:
        io_array[x][y] //= Q[x % 8][y % 8]


@cuda.jit
def my_kernel_2D_mul(io_array, Q):
    x, y = cuda.grid(2)

    if x < io_array.shape[0] and y < io_array.shape[1]:
        io_array[x][y] *= Q[x % 8][y % 8]


def do_dct(array):
    for row in range(height // 8):
        for col in range(width // 8):
            temp_row = row * 8
            temp_col = col * 8
            temp = np.zeros((8, 8))
            temp = array[temp_row: temp_row + 8, temp_col: temp_col + 8]
            temp_dct = dct2(temp)
            for i in range(8):
                for j in range(8):
                    array[temp_row + i][temp_col + j] = temp_dct[i][j]
            return array


def do_idct(array):
    for row in range(height // 8):
        for col in range(width // 8):
            temp_row = row * 8
            temp_col = col * 8
            temp = np.zeros((8, 8))
            temp = array[temp_row: temp_row + 8, temp_col: temp_col + 8]
            temp_idct = idct2(temp)
            for i in range(8):
                for j in range(8):
                    array[temp_row + i][temp_col + j] = temp_idct[i][j]
            return array


'''kvantizačná matica'''
Q = np.array([[16,  11,  10,  16,  24,  40,  51,  61],
             [12,  12,  14,  19,  26,  58,  60,  55],
             [14,  13,  16,  24,  40,  57,  69,  56],
             [14,  17,  22,  29,  51,  87,  80,  62],
             [18,  22,  37,  56,  68, 109, 103,  77],
             [24,  35,  55,  64,  81, 104, 113,  92],
             [49,  64,  78,  87, 103, 121, 120, 101],
             [72,  92,  95,  98, 112, 100, 103,  99]])


'''načítanie obrázku, prevod do grayscale'''
image = cv2.imread("image.jpeg")
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

[width, height] = grayscale.shape
array_image = np.array(grayscale, dtype=int)

'''dis. cos transf.'''
do_dct(array_image)

'''CUDA - delenie kvantizačnou maticou'''
threadsperblock = (8, 8)

blockspergrid_x = math.ceil(array_image.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(array_image.shape[1] / threadsperblock[1])
blockspergrid = (blockspergrid_x, blockspergrid_y)

my_kernel_2D_div[blockspergrid, threadsperblock](array_image, Q)

'''v tejto časti by sa malo ešte nachádzať
kódovanie obrázka - po uhlopriečkach,
následne uloženie poľa do súboru,
načítanie a spätné dekódovanie na 2D array...
na demonštrovanie CUDA úlohy je táto časť
bezpredmetná
'''
# code_to_file()

'''CUDA - spätné vynásobenie kvantizačnou maticou'''
my_kernel_2D_mul[blockspergrid, threadsperblock](array_image, Q)

'''spätná dis. cos transf.'''
do_idct(array_image)

'''vykreslenie pôvodného obrázku'''
plt.imshow(grayscale, cmap='Greys_r')
plt.show()
'''vykreslenie nového obrázku'''
plt.imshow(array_image, cmap='Greys_r')
plt.show()
