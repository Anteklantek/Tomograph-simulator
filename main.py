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

circle_list = []
circle_list.append(utils.get_first_detector_by_scope_and_angle(math.pi/3, 0, 32))
circle_list.append(utils.get_last_detector_by_scope_and_angle(math.pi/3, 0, 32))
draw.point(circle_list, fill=128)





white.save("/home/antq/PycharmProjects/TomographSimulator/Tomograph-simulator/test_images/white_line.bmp")

# print(utils.first_pixel_of_angle_32(1.625 * math.pi))