import logging

formatter=logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")


def config_logger(logger_name, filename, level=logging.INFO) -> logging.Logger:
    handler=logging.FileHandler(filename)
    handler.setFormatter(formatter)
    logger=logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger