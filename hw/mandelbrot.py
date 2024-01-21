import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

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


def create_mandelbrot_image(xmin=-2, xmax=1, ymin=-1.5, ymax=1.5, max_iter=80):
    try:

        img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), 'black')
        pixels = img.load()

        for x in range(SCREEN_WIDTH):
            for y in range(SCREEN_HEIGHT):
                # Map pixel coordinates to the complex plane
                c_real = xmin + (x / (SCREEN_WIDTH - 1)) * (xmax - xmin)
                c_imag = ymin + (y / (SCREEN_HEIGHT - 1)) * (ymax - ymin)

                # Check if the point is in the Mandelbrot set
                color_value = mandelbrot(complex(c_real, c_imag), max_iter)

                # Map the iteration count to a color
                r = (color_value % 8) * 32
                g = (color_value % 16) * 16
                b = (color_value % 32) * 8

                pixels[x, y] = (r, g, b)

        return img
    except BaseException as e:
        logging.error(e)
        return None
