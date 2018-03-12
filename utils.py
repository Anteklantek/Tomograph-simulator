import math


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


def get_num_of_pixel(x, y, pixels_in_row):
    return x * pixels_in_row + y


def get_num_of_pixel_32(x,y):
    return get_num_of_pixel(x,y,32)


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
