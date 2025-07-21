# utils/logger.py
import logging
import sys

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name and log level.
    
    Args:
        name (str): Name of the logger.
        level (int, optional): Logging level. Defaults to logging.INFO.
    
    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if logger already has one.
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Example usage:
if __name__ == "__main__":
    log = setup_logger("neurotask")
    log.info("Logger is set up and running.")
