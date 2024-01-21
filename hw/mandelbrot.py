import logging
import numpy as np
from multiprocessing import Pool
from PIL import Image

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200


def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    if n == max_iter:
        return 0  # Point is in the Mandelbrot set
    else:
        return n  # Point is not in the Mandelbrot set


def compute_pixel(args):
    x, y, xmin, xmax, ymin, ymax, max_iter = args
    c_real = xmin + (x / (SCREEN_WIDTH - 1)) * (xmax - xmin)
    c_imag = ymin + (y / (SCREEN_HEIGHT - 1)) * (ymax - ymin)
    color_value = mandelbrot(complex(c_real, c_imag), max_iter)
    return x, y, color_value


def create_mandelbrot_image(xmin=-2, xmax=1, ymin=-1.5, ymax=1.5, max_iter=50):
    try:
        pool = Pool()
        args_list = [(x, y, xmin, xmax, ymin, ymax, max_iter) for x in range(SCREEN_WIDTH) for y in
                     range(SCREEN_HEIGHT)]
        results = pool.map(compute_pixel, args_list)
        pool.close()
        pool.join()

        img_array = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=int)

        for x, y, color_value in results:
            img_array[x, y] = color_value

        img_array = (img_array / max_iter * 255).astype(np.uint8)
        img = Image.fromarray(img_array, 'L')

        return img
    except BaseException as e:
        logging.error(e)
        return None
