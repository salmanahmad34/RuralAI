import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import settings

def get_logger(name: str) -> logging.Logger:
    """Retrieve a configured logger instance with console and file rotational handlers."""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if already configured
    if logger.hasHandlers():
        return logger
        
    # Read log level from configurations
    log_level_str = settings.log_level.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    # Common formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler: check and generate logs folder
    log_dir = "logs"
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            # Fallback to current directory if permission issue
            log_dir = "."
            
    log_file_path = os.path.join(log_dir, "app.log")
    try:
        # 5MB log file limit with 3 backups
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Unable to initialize File Logger at {log_file_path}: {e}")

    return logger
