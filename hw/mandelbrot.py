import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
import numpy as np

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


def create_mandelbrot_image(xmin=-2, xmax=1, ymin=-1.5, ymax=1.5, max_iter=50):
    try:
        x, y = np.meshgrid(np.linspace(xmin, xmax, SCREEN_WIDTH), np.linspace(ymin, ymax, SCREEN_HEIGHT))
        c = x + 1j * y
        img = np.zeros(c.shape, dtype=int)

        for i in range(max_iter):
            mask = np.abs(img) <= 2
            img[mask] = img[mask] * img[mask] + c[mask]
            img_count = np.where(mask, i, 0)

        r = (img_count % 8) * 32
        g = (img_count % 16) * 16
        b = (img_count % 32) * 8

        img_array = np.stack((r, g, b), axis=-1).astype(np.uint8)
        img = Image.fromarray(img_array, 'RGB')

        return img
    except BaseException as e:
        logging.error(e)
        return None
