import logging

logging.getLogger().setLevel(logging.INFO)


def get_default_logger(name):
    logger = logging.getLogger(name)
    return logger
