import logging

def setup_logger():

    # Create a logger
    logger = logging.getLogger(__name__)

    # Check if a StreamHandler already exists
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        # Create a StreamHandler for the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it on the console handler
        formatter = logging.Formatter('%(asctime)s-%(process)d-%(threadName)s-%(message)s')
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

    # Create a FileHandler for the log file
    file_handler = logging.FileHandler(filename='app.log', mode='w')
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it on the file handler
    formatter = logging.Formatter('%(asctime)s-%(process)d-%(threadName)s-%(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Optionally, set the logger level
    logger.setLevel(logging.DEBUG)

    return logger
