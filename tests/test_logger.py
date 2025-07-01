#!/usr/bin/env python3

"""Tests for logging functionality."""

import pytest
import tempfile
import os
import logging
from auto_website_visitor.logger import setup_logger, VisitorLogger, _parse_size
from auto_website_visitor.config import VisitorSettings


class TestSetupLogger:
    """Test setup_logger function."""
    
    def test_basic_logger_setup(self):
        """Test basic logger setup."""
        logger = setup_logger("test_logger")
        
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1  # Console handler only
    
    def test_logger_with_file(self):
        """Test logger setup with file handler."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            logger = setup_logger("test_logger", log_file=f.name)
            
            assert len(logger.handlers) == 2  # Console + file handlers
            
            # Test logging
            logger.info("Test message")
            
            # Check file content
            with open(f.name, 'r') as log_file:
                content = log_file.read()
                assert "Test message" in content
            
            os.unlink(f.name)
    
    def test_logger_levels(self):
        """Test different logging levels."""
        debug_logger = setup_logger("debug_logger", log_level="DEBUG")
        error_logger = setup_logger("error_logger", log_level="ERROR")
        
        assert debug_logger.level == logging.DEBUG
        assert error_logger.level == logging.ERROR
    
    def test_console_output_disabled(self):
        """Test logger with console output disabled."""
        logger = setup_logger("test_logger", console_output=False)
        
        assert len(logger.handlers) == 0  # No handlers


class TestParseSizeFunction:
    """Test _parse_size function."""
    
    def test_parse_kb(self):
        """Test parsing KB sizes."""
        assert _parse_size("1KB") == 1024
        assert _parse_size("500KB") == 512000
        assert _parse_size("1.5KB") == 1536
    
    def test_parse_mb(self):
        """Test parsing MB sizes."""
        assert _parse_size("1MB") == 1048576
        assert _parse_size("2.5MB") == 2621440
    
    def test_parse_gb(self):
        """Test parsing GB sizes."""
        assert _parse_size("1GB") == 1073741824
    
    def test_parse_bytes(self):
        """Test parsing raw bytes."""
        assert _parse_size("1024") == 1024
        assert _parse_size("500") == 500


class TestVisitorLogger:
    """Test VisitorLogger class."""
    
    def test_visitor_logger_init(self):
        """Test VisitorLogger initialization."""
        settings = VisitorSettings(log_level="DEBUG")
        visitor_logger = VisitorLogger(settings)
        
        assert visitor_logger.logger.level == logging.DEBUG
    
    def test_visitor_logger_methods(self):
        """Test VisitorLogger logging methods."""
        settings = VisitorSettings()
        visitor_logger = VisitorLogger(settings)
        
        # These should not raise exceptions
        visitor_logger.info("Info message")
        visitor_logger.warning("Warning message")
        visitor_logger.error("Error message")
        visitor_logger.debug("Debug message")
        visitor_logger.critical("Critical message")
    
    def test_visitor_logger_with_file(self):
        """Test VisitorLogger with file logging."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            settings = VisitorSettings(log_file=f.name)
            visitor_logger = VisitorLogger(settings)
            
            visitor_logger.info("Test file logging")
            
            # Check file content
            with open(f.name, 'r') as log_file:
                content = log_file.read()
                assert "Test file logging" in content
            
            os.unlink(f.name)