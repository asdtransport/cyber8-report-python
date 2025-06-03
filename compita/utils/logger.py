"""
Logging configuration for the Cyber8 report generator.
"""
import os
import logging
from datetime import datetime

def setup_logger(name, log_level=logging.INFO):
    """
    Set up a logger with the specified name and log level.
    
    Args:
        name (str): The name of the logger.
        log_level (int): The log level to use.
        
    Returns:
        logging.Logger: The configured logger.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create file handler
    log_file = f"logs/{name}_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    return logger
