#!/usr/bin/env python3

"""Logging configuration for Auto Website Visitor."""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "auto_website_visitor",
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_rotate: bool = True,
    max_log_size: str = "1MB",
    backup_count: int = 3,
    console_output: bool = True
) -> logging.Logger:
    """Set up logger with file and console handlers.
    
    Args:
        name: Logger name
        log_level: Logging level
        log_file: Log file path
        log_rotate: Enable log rotation
        max_log_size: Maximum log file size
        backup_count: Number of backup files to keep
        console_output: Enable console output
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        if log_rotate:
            # Parse max_log_size
            size_bytes = _parse_size(max_log_size)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=size_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
        else:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def _parse_size(size_str: str) -> int:
    """Parse size string to bytes.
    
    Args:
        size_str: Size string (e.g., "1MB", "500KB")
        
    Returns:
        Size in bytes
    """
    size_str = size_str.upper().strip()
    
    if size_str.endswith('KB'):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith('MB'):
        return int(float(size_str[:-2]) * 1024 * 1024)
    elif size_str.endswith('GB'):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
    else:
        # Assume bytes
        return int(size_str)


class VisitorLogger:
    """Logger wrapper for Auto Website Visitor."""
    
    def __init__(self, settings):
        """Initialize logger with settings.
        
        Args:
            settings: VisitorSettings instance
        """
        self.logger = setup_logger(
            log_level=settings.log_level,
            log_file=settings.log_file,
            log_rotate=settings.log_rotate,
            max_log_size=settings.max_log_size,
            backup_count=settings.backup_count
        )
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self.logger.debug(message)
    
    def critical(self, message: str) -> None:
        """Log critical message."""
        self.logger.critical(message)