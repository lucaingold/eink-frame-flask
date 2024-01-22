import logging
import os
from omni_epd import displayfactory, EPDNotFoundError
from constants import ConfigConst
from hw.config_wrapper import Configs

DISPLAY_TYPE = "waveshare_epd.it8951"
# DISPLAY_TYPE = "omni_epd.mock"


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

        # Load config or set defaults
        # self.config = self.load_config()

        pass

    def run(self):
        logging.info("einkframe has begun")
        try:
            # self.config_dict["VCOM"] = -2.27
            self.epd = displayfactory.load_display_driver(DISPLAY_TYPE, self.config_dict)
            # If display is mock, apply height and width to it

            self.epd.width = 1600
            self.epd.height = 1200

            image_rotate = 0

            # Set width and height for einkframe program
            self.width, self.height = self.set_rotate(self.epd.width, self.epd.height, image_rotate)

            # draw = ImageDraw.Draw(self.image_display, "RGBA")
            # self.add_text_to_image(draw, 'resources/fonts/Font.ttc', self.image_display.height, self.width,
            #                        'Title', 'Text', 30, 10, 10, 150, 20, 14, True, True,
            #                        crop_left, crop_right)






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

    def load_config(self):
        # Loads config from file provided to it or sets defaults
        config = None

        try:
            config_path = ConfigConst.CONFIG_PATH.value

            config = Configs(config_path=config_path, path=self.file_path)

            self.config_dict = config.read_config()

            log_file = ConfigConst.LOGGING_FILE.value

            # Set up logging
            if config.log_file is not None and config.log_file != "":
                log_file = os.path.join(self.file_path, config.log_file)

            logging.basicConfig(level=config.log_level, filename=log_file,
                                format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            logging.info("Config loaded")

        except IOError as e:
            logging.error(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            exit()

        return config

    @staticmethod
    def set_rotate(width, height, rotate=0):
        if (rotate / 90) % 2 == 1:
            temp = width
            width = height
            height = temp
        return width, height

    def display_image_on_epd(self, display_image):

        self.image_display = display_image.copy()

        # result.resize((w, h))
        # if self.image_display.mode not in ["RGB", "RGBA"]:
        #     self.image_display = self.image_display.convert("RGB")

        # Rotate image back to save
        # display_image = display_image.rotate(-0, expand=1)
        # display_image = display_image.rotate(-0, expand=1)
        # display_image = display_image.rotate(90, expand=1)

        logging.info("Prepare epaper")
        self.epd.prepare()

        self.epd.display(self.image_display)

        logging.info("Send epaper to sleep")
        self.epd.sleep()
        self.epd.close()
        return
