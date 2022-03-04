import cv2
import math
import numpy as np

def is_input_invalid(value: int) -> bool:
    return not(type(value) is int) or not(value <= 255)
    
class CMYK:
    def __init__(self, c, m, y, k) -> None:
        self.c = c
        self.m = m
        self.y = y
        self.k = k
    def print(self):
        print('({c}, {m}, {y}, {k})'.format(c = math.trunc(self.c), m = math.trunc(self.m), y = math.trunc(self.y), k = math.trunc(self.k)))
    def return_array(self):
        return [math.trunc(self.c), math.trunc(self.m), math.trunc(self.y), math.trunc(self.k)]

class RGB:
    def __init__(self, red, green, blue) -> None:
        self.red = red
        self.green = green
        self.blue = blue
    def print(self):
        print('({r}, {g}, {b})'.format(r = self.red, g = self.green, b = self.blue))
    def convert_to_CMYK(self) -> CMYK:
        if(self.red, self.green, self.blue) == (0, 0, 0):
            return 0, 0, 0, 100
        
        c = 1 - self.red / 255
        m = 1 - self.green / 255
        y = 1 - self.blue / 255

        minimal_cmy = min(c, m, y)
        c = (c - minimal_cmy) / (1 - minimal_cmy)
        m = (m - minimal_cmy) / (1 - minimal_cmy)
        y = (y - minimal_cmy) / (1 - minimal_cmy)
        k = minimal_cmy

        return c * 100, m * 100, y * 100, k * 100


image = cv2.imread('test.png')

newImage = []
for column in image:
    convertedColumnPixels = []
    for pixel in column:
        rgb = RGB(*pixel)
        convertedPixel = CMYK(*rgb.convert_to_CMYK()).return_array()
        convertedColumnPixels.append(convertedPixel)
    newImage.append(convertedColumnPixels)

npNewImage = np.array(newImage)

cv2.imwrite('cmyk.tiff', npNewImage)