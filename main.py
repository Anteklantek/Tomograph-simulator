from PIL import Image, ImageDraw
import utils
import math


# pixels = list(image_dot.getdata())
# for i in range(32):
#     for j in range(32):
#             print(pixels[i * 32 + j][1], end=" ")
#     print("\n")


white = Image.open("test_images/square.bmp")
draw = ImageDraw.Draw(white)

# circle_list_1 = []
# for i in range(0,100):
#     circle_list_1.append(utils.get_circle_pixel_by_angle(math.pi * i / 200, 32))
# draw.point(circle_list_1, fill=255)

draw.point(utils.get_list_of_detector_pixels_64(math.pi/3, 0, 10), fill=128)







white.save("/home/antq/PycharmProjects/TomographSimulator/Tomograph-simulator/test_images/white_line.bmp")

# print(utils.first_pixel_of_angle_32(1.625 * math.pi))