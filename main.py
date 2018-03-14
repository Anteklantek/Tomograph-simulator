from PIL import Image, ImageDraw
import utils
import math
import numpy


image = Image.open("test_images/centered_square.bmp")
pixels = image.load()

number_of_steps = 360
scope = math.pi/3
number_of_detectors = 80
radius = image.size[0]/2

# sinogram = utils.doTomography(scope, number_of_steps, number_of_detectors, radius, pixels, number_of_steps)
#
# for i in range(0, number_of_steps):
#     for j in range(0, number_of_detectors):
#         print(sinogram[i * number_of_detectors + j][0], end=" ")
#     print("\n")
#
# img = Image.new('RGB', (number_of_detectors, number_of_steps))
# img.putdata(sinogram)
# img.save("test_images/sinogram.bmp", "BMP")

sinogram_image = Image.open("test_images/sinogram.bmp")
sinogram_pixels = sinogram_image.load()

out = utils.generate_out_image(scope,radius,number_of_steps,number_of_detectors,sinogram_pixels,number_of_steps)



# for i in range(0,number_of_detectors):
#     for j in range(0, number_of_steps):
#         print(sinogram[i * j], end=" ")
#     print("\n")


