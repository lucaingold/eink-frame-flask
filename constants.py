#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Enums for constants to be used throughout pycasso

import logging
from enum import Enum


class ConfigConst(Enum):
    # Default settings that are loaded from config
    # Relative path to config
    CONFIG_PATH = ".config"
    CONFIG_PATH_EG = "examples/.config"

    # Defaults
    # File Settings
    FILE_SAVE_IMAGE = 1
    FILE_EXTERNAL_IMAGE_LOCATION = "images/external"
    FILE_GENERATED_IMAGE_LOCATION = "images/generated"
    FILE_IMAGE_FORMAT = "png"
    FILE_FONT_FILE = "resources/fonts/Font.ttc"
    FILE_SUBJECTS_FILE = "prompts/subjects.txt"
    FILE_ARTISTS_FILE = "prompts/artists.txt"
    FILE_PROMPTS_FILE = "prompts/prompts.txt"
    FILE_SUBJECTS_EG = "examples/prompts/subjects-example.txt"
    FILE_ARTISTS_EG = "examples/prompts/artists-example.txt"
    FILE_PROMPTS_EG = "examples/prompts/prompts-example.txt"
    FILE_RESIZE_EXTERNAL = True

    # Text Settings
    TEXT_ADD_TEXT = False
    TEXT_PARSE_FILE_TEXT = False
    TEXT_PARSE_RANDOM_TEXT = True
    TEXT_PARSE_BRACKETS = "\"()\"\n\"[]\"\n\"{}\""
    TEXT_PARSE_BRACKETS_LIST = ["()", "[]", "{}"]
    TEXT_PREAMBLE_REGEX = ".*- "
    TEXT_ARTIST_REGEX = " by "
    TEXT_REMOVE_TEXT = "\"()\"\n\"[]\"\n\"{}\""
    TEXT_REMOVE_TEXT_LIST = [", digital art", "A painting of"]
    TEXT_BOX_TO_FLOOR = True
    TEXT_BOX_TO_EDGE = True
    TEXT_ARTIST_LOC = 10
    TEXT_ARTIST_SIZE = 14
    TEXT_TITLE_LOC = 30
    TEXT_TITLE_SIZE = 20
    TEXT_PADDING = 10
    TEXT_OPACITY = 150
    TEXT_OVERRIDE_TEXT = False
    TEXT_OVERRIDE_PATH = "prompts/override.txt"

    # Icon Settings
    ICON_COLOR = "auto"
    ICON_PADDING = 10
    ICON_CORNER = "nw"
    ICON_SIZE = 20
    ICON_WIDTH = 3
    ICON_GAP = 5
    ICON_OPACITY = 150
    ICON_PATH = "resources/icons/"
    SHOW_BATTERY_ICON = True
    SHOW_PROVIDER_ICON = True
    SHOW_STATUS_ICON = True

    # Automatic Prompt Construction Settings
    PROMPT_MODES_COUNT = 2
    PROMPT_MODE = 1
    PROMPT_PREAMBLE = ""
    PROMPT_CONNECTOR = " by "
    PROMPT_POSTSCRIPT = ", digital art, trending on artstation"

    # Display Settings
    DISPLAY_TYPE = "omni_epd.mock"

    # Logging Settings
    LOGGING_FILE = "einkframe.log"
    LOGGING_LEVEL = logging.DEBUG

    # Generation Settings
    GENERATION_ROTATE = 0
    GENERATION_INFILL = False
    GENERATION_INFILL_PERCENT = 10

    # Post Settings
    POST_CONNECTOR = " in the style of "
    POST_TO_MASTODON = False
    MASTODON_APP_NAME = "new_app"
    MASTODON_BASE_URL = 'https://mastodon.social'
    MASTODON_CLIENT_CRED_PATH = "m_client.secret"
    MASTODON_USER_CRED_PATH = "m_user.secret"

    # PiJuice Settings
    USE_PIJUICE = False
    SHUTDOWN_ON_BATTERY = True
    SHUTDOWN_ON_EXCEPTION = False
    WAIT_TO_RUN = 30
    CHARGE_DISPLAY = 15

    # Debug Settings
    TEST_EPD_WIDTH = 1600
    TEST_EPD_HEIGHT = 1200


class PropertiesConst(Enum):
    FILE_PREAMBLE = "einkframe - "
    ARTIST = "artist"
    TITLE = "title"
    PROMPT = "prompt"


class PromptModeConst(Enum):
    RANDOM = 0
    SUBJECT_ARTIST = 1
    PROMPT = 2


class DisplayShapeConst(Enum):
    SQUARE = 0
    CROSS = 1
    TRIANGLE = 2
    CIRCLE = 3


class ImageConst(Enum):
    CONVERT_MODE = "RGB"
    DRAW_MODE = "RGBA"
    SUPPORTED_MODES = ["RGB", "RGBA"]


class EPDConst(Enum):
    COLOR = "color"
    BW = "bw"
    YELLOW = "yellow"
    RED = "red"
    PALETTE = "palette"
    FOUR_COLOR = "4color"
    FOUR_GRAY = "gray4"


class IconConst(Enum):
    LOC_TOP_LEFT = "nw"
    LOC_TOP_RIGHT = "ne"
    LOC_BOTTOM_LEFT = "sw"
    LOC_BOTTOM_RIGHT = "se"

    BACKGROUND_DARK_LIMIT = 127


class IconFileConst(Enum):
    ICON_BATTERY_20 = ("battery.png", 10)
    ICON_BATTERY_40 = ("battery-1.png", 20)
    ICON_BATTERY_60 = ("battery-2.png", 30)
    ICON_BATTERY_80 = ("battery-3.png", 40)
    ICON_BATTERY_100 = ("battery-4.png", 50)
    ICON_BATTERY_ERROR = ("battery-off.png", 60)
    ICON_BATTERY_WEAK = ("battery-eco.png", 65)
    ICON_BATTERY_CHARGE = ("battery-charging-2.png", 70)

    ICON_TEST = ("stethoscope.png", 97)
    ICON_EXTERNAL = ("circle-letter-e.png", 100)
    ICON_HISTORIC = ("circle-letter-h.png", 110)
    ICON_STABLE = ("circle-letter-s.png", 120)
    ICON_DALLE = ("circle-letter-d.png", 130)
    ICON_AUTOMATIC = ("circle-letter-a.png", 140)

    ICON_TEST_FAIL = ("stethoscope-off.png", 67)
    ICON_EXTERNAL_FAIL = ("hexagon-letter-e.png", 70)
    ICON_HISTORIC_FAIL = ("hexagon-letter-h.png", 75)
    ICON_STABLE_FAIL = ("hexagon-letter-s.png", 80)
    ICON_DALLE_FAIL = ("hexagon-letter-d.png", 85)
    ICON_AUTOMATIC_FAIL = ("hexagon-letter-a.png", 90)

    ICON_EXCEPTION = ("heart-broken.png", 200)