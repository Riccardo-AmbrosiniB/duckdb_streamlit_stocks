import logging
import os


# Function to configure the logger
def setup_logger(name=__name__, log_file=None, level=logging.INFO) -> logging.Logger:
    # Create a custom logger
    logger = logging.getLogger(name)

    # If logger has handlers, return it (avoid adding multiple handlers to the same logger)
    if logger.hasHandlers():
        return logger

    # Set the logging level
    logger.setLevel(level)

    # Create formatters and add them to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
