import logging

logging.getLogger().setLevel(logging.INFO)


def get_default_logger(clazz):
    logger = logging.getLogger(clazz.__name__)
    return logger
