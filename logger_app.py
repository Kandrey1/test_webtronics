import logging

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

info_handler = logging.FileHandler(".logs.log", mode='w', encoding="utf-8")
info_formatter = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
info_handler.setFormatter(info_formatter)
logger.addHandler(info_handler)
