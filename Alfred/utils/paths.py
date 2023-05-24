from typing import NoReturn
import os
from loguru import logger


def clear_paths(*paths) -> NoReturn:
    logger.info('Utils: clearing the path of the media file')
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
