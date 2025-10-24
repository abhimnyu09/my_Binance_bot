import logging
import sys

def setup_logger():
    """
    Sets up a structured logger that logs to both console and 'bot.log'.
    """
    # Create logger
    logger = logging.getLogger('BinanceBot')
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )

    # File handler (logs to bot.log)
    file_handler = logging.FileHandler('bot.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler (logs to stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Create a single logger instance to be imported by other modules
log = setup_logger()
