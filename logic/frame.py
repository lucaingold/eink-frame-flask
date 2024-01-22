import logging
import os
from omni_epd import displayfactory, EPDNotFoundError
from constants import ConfigConst

DISPLAY_TYPE = "waveshare_epd.it8951"


class EInkFrame:
    def __init__(self, file_path=os.getcwd()):

        self.file_path = file_path

        # Config Dictionary for omni-epd
        self.config_dict = {}

        # EPD
        self.epd = None

        # Image
        self.image_base = None
        self.image_display = None
        self.width = ConfigConst.TEST_EPD_WIDTH.value
        self.height = ConfigConst.TEST_EPD_HEIGHT.value
        pass

    def run(self):
        logging.info("einkframe has started")
        try:
            self.epd = displayfactory.load_display_driver(DISPLAY_TYPE, self.config_dict)
            self.epd.width = 1600
            self.epd.height = 1200
            image_rotate = 0
            # Set width and height for einkframe program
            self.width, self.height = self.set_rotate(self.epd.width, self.epd.height, image_rotate)
        except EPDNotFoundError:
            logging.error(f"Couldn't find {DISPLAY_TYPE}")
            exit()

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            exit()

        except BaseException as e:
            logging.error(e)
            exit()

    pass

    @staticmethod
    def set_rotate(width, height, rotate=0):
        if (rotate / 90) % 2 == 1:
            temp = width
            width = height
            height = temp
        return width, height

    def display_image_on_epd(self, display_image):
        self.image_display = display_image.copy()
        logging.info("Prepare epaper")
        self.epd.prepare()
        self.epd.display(self.image_display)
        logging.info("Send epaper to sleep")
        self.epd.sleep()
        self.epd.close()
        return
