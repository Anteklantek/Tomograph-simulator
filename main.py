from PIL import Image, ImageDraw
import utils
import math
import numpy


square = Image.open("test_images/dot_decentered.bmp")
pixels = square.load()

number_of_steps = 100
scope = math.pi/3
number_of_detectors = 100
sinogram = []
generator_step = 2 * math.pi / number_of_steps
for i in range(0, number_of_steps):
    generator_angle = i * generator_step
    generator_point = utils.get_circle_pixel_by_angle(generator_angle, 64)
    list_of_detectors = utils.get_list_of_detector_pixels(scope, generator_angle, 64, number_of_detectors)
    for detector in list_of_detectors:
        sum_of_pix = utils.get_sum_of_between_pixels_on_path(generator_point[0], generator_point[1], detector[0], detector[1], pixels)
        sinogram.append(sum_of_pix)


normalized_sinogram = utils.normalize_sinogram(sinogram)

img = Image.new('RGB', (number_of_detectors, number_of_steps))
img.putdata(normalized_sinogram)
img.save("test_images/sinogram.bmp", "BMP")

for i in range(0,number_of_detectors):
    for j in range(0, number_of_steps):
        print(sinogram[i * j], end=" ")
    print("\n")

square.save("test_images/white_line.bmp")

