import logging

COLORS = {
    "INFO": "\033[92m",     # Vert
    "WARNING": "\033[93m",  # Jaune
    "ERROR": "\033[91m",    # Rouge
    "RESET": "\033[0m",     # Reset couleur
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, COLORS["RESET"])
        message = super().format(record)
        return f"{log_color}{message}{COLORS['RESET']}"

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG) 

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = ColorFormatter("[%(levelname)s] %(message)s")
ch.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(ch)
