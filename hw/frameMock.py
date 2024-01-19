import logging
import os
# from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from hw.file_operations import FileOperations
from hw.image_functions import ImageFunctions
from constants import ConfigConst
from hw.config_wrapper import Configs

DISPLAY_TYPE = "waveshare_epd.it8951"


# DISPLAY_TYPE = "omni_epd.mock"


class EInkFrameMock:
    def __init__(self, file_path=os.getcwd()):
        pass

    def run(self):
        pass

    def load_config(self):
        pass

    @staticmethod
    def set_rotate(width, height, rotate=0):
        pass

    def display_image_on_epd(self, display_image):
        return
