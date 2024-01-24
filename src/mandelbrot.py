import logging

import numpy
import numpy as np
from PIL import Image
from flask import current_app
import math


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


def create_mandelbrot_image(xmin=-2, xmax=1, ymin=-1.5, ymax=1.5, max_iter=100):
    try:
        screen_width = current_app.config['SCREEN_WIDTH']
        screen_height = current_app.config['SCREEN_HEIGHT']

        # image size
        WIDTH = 512
        HEIGHT = 512

        print(WIDTH)
        print(HEIGHT)
        pix = numpy.zeros((HEIGHT, WIDTH, 3), dtype=numpy.uint8)

        # For each pixel in our little display...
        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                zoom = 0.3

                # The z in the mandelbrot set is an imaginary number, made up of
                # a real number and an imaginary component
                real = (float(x) / float(WIDTH)) * (1.0 / zoom) + -2.1
                imaginary = (float(y) / float(HEIGHT)) * (1.0 / zoom) + -1.6

                # This is the constant, which is the 'c' element of the main equation (z=z2+c)
                const_real = real
                const_imaginary = imaginary
                z2 = 0.0

                for iteration in range(0, max_iter):
                    temp_real = real

                    # Calculate z=z2+c
                    real = (temp_real * temp_real) - (imaginary * imaginary) + const_real
                    imaginary = 2.0 * temp_real * imaginary + const_imaginary
                    z2 = real * real + imaginary * imaginary

                    # If z2 exceeds 4.0 before we hit MAX_ITER then we exit the loop and the current pixel
                    # does not belong to the mandelbrot set
                    if z2 > 4.0:
                        break

                # Plot the current pixel. If it's in the mandelbrot set then do nothing.
                if z2 > 4.0:
                    c = iteration * 15 % 255
                    if c > 50:
                        pix.itemset((y, x, 2), c)
                    else:
                        pix.itemset((y, x, 2), 50)

        mandelbrot = Image.fromarray(pix, 'RGB')
        mandelbrot.save("mandelbrot.jpeg")
    except Exception as e:
        raise Exception(e)
