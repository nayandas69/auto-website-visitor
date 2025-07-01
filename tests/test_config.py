#!/usr/bin/env python3

"""Tests for configuration management."""

import pytest
import tempfile
import os
from auto_website_visitor.config import Config, VisitorSettings


class TestVisitorSettings:
    """Test VisitorSettings dataclass."""
    
    def test_default_settings(self):
        """Test default settings values."""
        settings = VisitorSettings()
        
        assert settings.url == ""
        assert settings.visit_count == 1
        assert settings.interval == 5
        assert settings.timeout == 30
        assert settings.browser == "chrome"
        assert settings.headless is False
        assert settings.auto_scroll is False
        assert settings.schedule_enabled is False
        assert settings.retry_attempts == 3
        assert settings.log_level == "INFO"
    
    def test_custom_settings(self):
        """Test custom settings values."""
        settings = VisitorSettings(
            url="https://test.com",
            visit_count=10,
            browser="firefox",
            headless=True
        )
        
        assert settings.url == "https://test.com"
        assert settings.visit_count == 10
        assert settings.browser == "firefox"
        assert settings.headless is True


class TestConfig:
    """Test Config class."""
    
    def test_init_without_config(self):
        """Test initialization without config file."""
        config = Config()
        assert isinstance(config.settings, VisitorSettings)
        assert config.config_path is None
    
    def test_load_yaml_config(self):
        """Test loading YAML configuration."""
        yaml_content = """
url: https://test.com
visit_count: 5
browser: firefox
headless: true
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            f.flush()
            
            config = Config(f.name)
            
            assert config.settings.url == "https://test.com"
            assert config.settings.visit_count == 5
            assert config.settings.browser == "firefox"
            assert config.settings.headless is True
            
            os.unlink(f.name)
    
    def test_load_json_config(self):
        """Test loading JSON configuration."""
        json_content = """{
    "url": "https://test.com",
    "visit_count": 3,
    "browser": "edge",
    "headless": false
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(json_content)
            f.flush()
            
            config = Config(f.name)
            
            assert config.settings.url == "https://test.com"
            assert config.settings.visit_count == 3
            assert config.settings.browser == "edge"
            assert config.settings.headless is False
            
            os.unlink(f.name)
    
    def test_save_yaml_config(self):
        """Test saving YAML configuration."""
        config = Config()
        config.settings.url = "https://save-test.com"
        config.settings.visit_count = 7
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config.save_config(f.name, "yaml")
            
            # Load and verify
            new_config = Config(f.name)
            assert new_config.settings.url == "https://save-test.com"
            assert new_config.settings.visit_count == 7
            
            os.unlink(f.name)
    
    def test_validation_success(self):
        """Test successful validation."""
        config = Config()
        config.settings.url = "https://valid.com"
        config.settings.visit_count = 5
        
        assert config.validate() is True
    
    def test_validation_missing_url(self):
        """Test validation with missing URL."""
        config = Config()
        config.settings.url = ""
        
        with pytest.raises(ValueError, match="URL is required"):
            config.validate()
    
    def test_validation_invalid_url(self):
        """Test validation with invalid URL."""
        config = Config()
        config.settings.url = "invalid-url"
        
        with pytest.raises(ValueError, match="URL must start with"):
            config.validate()
    
    def test_validation_invalid_visit_count(self):
        """Test validation with invalid visit count."""
        config = Config()
        config.settings.url = "https://test.com"
        config.settings.visit_count = 0
        
        with pytest.raises(ValueError, match="Visit count must be at least 1"):
            config.validate()
    
    def test_update_from_args(self):
        """Test updating settings from arguments."""
        config = Config()
        
        config.update_from_args(
            url="https://args-test.com",
            visit_count=15,
            browser="firefox",
            invalid_arg="should_be_ignored"
        )
        
        assert config.settings.url == "https://args-test.com"
        assert config.settings.visit_count == 15
        assert config.settings.browser == "firefox"
        # Invalid args should be ignored
        assert not hasattr(config.settings, 'invalid_arg')