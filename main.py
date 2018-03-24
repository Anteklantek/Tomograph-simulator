from PIL import Image, ImageDraw
import utils
import math
import numpy

image_name = "two_squares.bmp"

image = Image.open("test_images/" + image_name)
pixels = image.load()

number_of_steps = 360
scope = math.pi/3
number_of_detectors = 150
radius = image.size[0]//2

sinogram = utils.doTomography(scope, number_of_steps, number_of_detectors, radius, pixels, number_of_steps)

# for i in range(0, number_of_steps):
#     for j in range(0, number_of_detectors):
#         print(sinogram[i * number_of_detectors + j][0], end=" ")
#     print("\n")

img = Image.new('RGB', (number_of_detectors, number_of_steps))
img.putdata(sinogram)
img.save("test_images/sinogram.bmp", "BMP")

sinogram_image = Image.open("test_images/sinogram.bmp")
sinogram_pixels = sinogram_image.load()

out = utils.generate_out_image(scope, radius, number_of_steps, number_of_detectors, sinogram_pixels, number_of_steps)

normalized_list = utils.generate_normalized_list(out)

img = Image.new('RGB', (radius * 2, radius * 2))
img.putdata(normalized_list)
img.save("out/" + image_name, "BMP")



