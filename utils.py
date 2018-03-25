import math
from PIL import Image, ImageDraw
import numpy as np
import numpy

def bresenham_line(x1, y1, x2, y2):
    list_of_pixels = []
    x = x1
    y = y1
    if x1 < x2:
        xi = 1
        dx = x2 - x1
    else:
        xi = -1
        dx = x1 - x2
    if y1 < y2:
        yi = 1
        dy = y2 - y1
    else:
        yi = -1
        dy = y1 - y2

    list_of_pixels.append((x,y))
    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        while x != x2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi
            list_of_pixels.append((x, y))
    else:
        ai = ( dx - dy ) * 2
        bi = dx * 2
        d = bi - dy
        while y != y2:
            if d >= 0:
               x += xi
               y += yi
               d += ai
            else:
                d += bi
                y += yi
            list_of_pixels.append((x, y))
    return list_of_pixels


def get_circle_pixel_by_angle(angle, radius):
    return radius + math.cos(angle)*radius, radius + math.sin(angle) * radius


def get_circle_pixel_by_angle_64(angle):
    return 32 + math.cos(angle)*32, 32 + math.sin(angle) * 32


def get_first_detector_by_scope_and_angle(scope, generator_angle, radius):
    detector = generator_angle + math.pi - scope
    return get_circle_pixel_by_angle(detector, radius)


def get_first_detector_by_scope_and_angle_64(scope, angle):
    return get_first_detector_by_scope_and_angle(scope, angle, radius=32)


def get_list_of_detector_pixels(scope, generator_angle, radius, number_of_detectors):
    list_of_detector_pixels = []
    step = 2 * scope / (number_of_detectors-1)
    first_detector_angle = generator_angle + math.pi - scope
    for i in range(0, number_of_detectors):
        list_of_detector_pixels.append(get_circle_pixel_by_angle(first_detector_angle + (i * step), radius))
    return list_of_detector_pixels


def get_list_of_detector_pixels_64(scope, generator_angle, number_of_detectors):
    return get_list_of_detector_pixels(scope, generator_angle, 32, number_of_detectors)


def get_last_detector_by_scope_and_angle(scope, generator_angle, radius):
    detector = generator_angle + math.pi + scope
    return get_circle_pixel_by_angle(detector, radius)


def get_last_detector_by_scope_and_angle_64(scope, angle):
    return get_last_detector_by_scope_and_angle(scope, angle, radius=32)


def get_sum_of_between_pixels_on_path(x1, y1, x2, y2, pixels):
    path_pixels = bresenham_line(round(x1), round(y1), round(x2), round(y2))
    path_pixels = path_pixels[1:len(path_pixels)-1]
    sum = 0
    for pixel in path_pixels:
        sum += pixels[pixel[0], pixel[1]][0]
    return sum


def normalize_sinogram(sinogram):
    maximum = max(sinogram)
    for i in range(len(sinogram)):
        sinogram[i] = round(sinogram[i]/maximum * 255), round(sinogram[i]/maximum * 255), round(sinogram[i]/maximum * 255)
    return sinogram


def save_image_of_lines(step_number, detectors, generator, image_name):
    image = Image.open("test_images/" + image_name + ".bmp")
    draw = ImageDraw.Draw(image)
    for detector in detectors:
        line = bresenham_line(round(detector[0]), round(detector[1]), round(generator[0]), round(generator[1]))
        draw.point(line, fill=255)
    image.save("out_detectors/" + str(step_number) + ".bmp", "BMP")


def doTomography (scope, number_of_steps, number_of_detectors, radius, pixels, image_name):
    sinogram = []
    generator_step = 2 * math.pi / number_of_steps
    for i in range(number_of_steps):
        generator_angle = i * generator_step
        generator_point = get_circle_pixel_by_angle(generator_angle, radius)
        list_of_detectors = get_list_of_detector_pixels(scope, generator_angle, radius, number_of_detectors)
        save_image_of_lines(i, list_of_detectors, generator_point, image_name)
        for detector in list_of_detectors:
            sum_of_pix = get_sum_of_between_pixels_on_path(generator_point[0], generator_point[1], detector[0], detector[1], pixels)
            sinogram.append(sum_of_pix)

    return normalize_sinogram(sinogram)


def generate_out_images(scope, radius, number_of_steps, number_of_detectors, pixels):
    s = (radius * 2, radius * 2)
    generator_step = 2 * math.pi / number_of_steps
    out_table = np.zeros(s)
    for i in range(number_of_steps):
        angle = i * generator_step
        generator_point = get_circle_pixel_by_angle(angle, radius)
        detectors = get_list_of_detector_pixels(scope, angle, radius, number_of_detectors)
        for j in range(number_of_detectors):
            line = bresenham_line(round(generator_point[0]), round(generator_point[1]), round(detectors[j][0]),
                                  round(detectors[j][1]))
            line = line[1:len(line) - 1]
            for point in line:
                out_table[point[1], point[0]] += pixels[j, i][0]
        intermediate_image = Image.new('RGB', (radius * 2, radius * 2))
        intermediate_image.putdata(generate_normalized_list(out_table))
        intermediate_image.save("out_end/" + str(i) + ".bmp", "BMP")


def generate_normalized_list(out):
    max_value = numpy.amax(out)
    out_list = out.tolist()
    flat_list = []

    for sublist in out_list:
        for item in sublist:
            flat_list.append(item)

    normalized_list = []

    for element in flat_list:
        # element -= 130000
        if element < 0:
            normalized_pixel = 0, 0, 0
        else:
            normalized_element = element / max_value * 255
            normalized_pixel = int(round(normalized_element)), int(round(normalized_element)), int(round(normalized_element))
        normalized_list.append(normalized_pixel)

    return normalized_list
