from PIL import Image, ImageDraw
import utils
import math
import numpy


image = Image.open("test_images/centered_square.bmp")
pixels = image.load()



number_of_steps = 360
scope = math.pi/3
number_of_detectors = 10
radius = image.size[0]/2
angle = 0

detectors = utils.get_list_of_detector_pixels(scope,angle,radius,number_of_detectors)
generator = utils.get_circle_pixel_by_angle(angle,radius)

draw = ImageDraw.Draw(image)

for detector in detectors:
    line = utils.bresenham_line(round(detector[0]), round(detector[1]), round(generator[0]), round(generator[1]))
    draw.point(line,fill=255)

draw.point(detectors,fill=123)
image.save("test_images/detectors.bmp", "BMP")

image = Image.open("test_images/centered_square.bmp")
pixels = image.load()

sinogram = utils.doTomography(scope,number_of_steps,number_of_detectors,radius,pixels, number_of_steps)

img = Image.new('RGB', (number_of_detectors, number_of_steps))
img.putdata(sinogram)
img.save("test_images/sinogram.bmp", "BMP")

for i in range(0,number_of_detectors):
    for j in range(0, number_of_steps):
        print(sinogram[i * j], end=" ")
    print("\n")


