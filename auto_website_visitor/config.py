#!/usr/bin/env python3

"""Configuration management for Auto Website Visitor."""

import os
import json
import yaml
from typing import Dict, Any, Optional, Tuple, Literal, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class VisitorSettings:
    """Core visitor settings."""

    # Core settings
    url: str = ""
    visit_count: int = 1
    interval: int = 5
    timeout: int = 30

    # Browser options
    browser: Literal["chrome", "firefox", "edge"] = "chrome"
    headless: bool = False
    user_agent: Optional[str] = None
    proxy: Optional[str] = None

    # Behavior settings
    auto_scroll: bool = False
    scroll_pause: float = 0.5
    max_scroll: int = 5
    random_delay: bool = False
    delay_range: Tuple[int, int] = (1, 5)

    # Scheduler settings
    schedule_enabled: bool = False
    schedule_type: Literal["interval", "cron"] = "interval"
    schedule_value: str = "1h"

    # Advanced options
    retry_attempts: int = 3
    retry_delay: int = 5
    log_level: str = "INFO"
    log_file: str = "auto_visitor.log"
    log_rotate: bool = True
    max_log_size: str = "1MB"
    backup_count: int = 3

    # Environment variables
    proxy_user: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_USER"))
    proxy_pass: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_PASS"))
    custom_headers: Optional[Dict[str, str]] = field(
        default_factory=lambda: (
            json.loads(os.getenv("CUSTOM_HEADERS", "{}"))
            if os.getenv("CUSTOM_HEADERS")
            else None
        )
    )


class Config:
    """Configuration manager for Auto Website Visitor."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.settings = VisitorSettings()

        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Load configuration from file.

        Args:
            config_path: Path to configuration file

        Raises:
            ValueError: If config file format is not supported
            FileNotFoundError: If config file doesn't exist
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        file_ext = Path(config_path).suffix.lower()

        with open(config_path, "r", encoding="utf-8") as f:
            if file_ext in [".yaml", ".yml"]:
                config_data = yaml.safe_load(f)
            elif file_ext == ".json":
                config_data = json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {file_ext}")

        self._update_settings(config_data)

    def save_config(self, config_path: str, format_type: str = "yaml") -> None:
        """Save current configuration to file.

        Args:
            config_path: Path to save configuration file
            format_type: Format to save (yaml or json)
        """
        config_data = asdict(self.settings)

        # Remove None values for cleaner config
        config_data = {k: v for k, v in config_data.items() if v is not None}

        with open(config_path, "w", encoding="utf-8") as f:
            if format_type.lower() == "yaml":
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            elif format_type.lower() == "json":
                json.dump(config_data, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format_type}")

    def _update_settings(self, config_data: Dict[str, Any]) -> None:
        """Update settings from configuration data.

        Args:
            config_data: Configuration data dictionary
        """
        for key, value in config_data.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)

    def update_from_args(self, **kwargs) -> None:
        """Update settings from command line arguments.

        Args:
            **kwargs: Keyword arguments to update
        """
        # Process CLI arguments and update settings

        for key, value in kwargs.items():
            if value is not None and hasattr(self.settings, key):
                setattr(self.settings, key, value)

    def validate(self) -> bool:
        """Validate current configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.settings.url:
            raise ValueError("URL is required")

        if not self.settings.url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        if self.settings.visit_count < 1:
            raise ValueError("Visit count must be at least 1")

        if self.settings.interval < 0:
            raise ValueError("Interval must be non-negative")

        if self.settings.timeout < 1:
            raise ValueError("Timeout must be at least 1 second")

        if self.settings.browser not in ["chrome", "firefox", "edge"]:
            raise ValueError("Browser must be one of: chrome, firefox, edge")

        if self.settings.schedule_type not in ["interval", "cron"]:
            raise ValueError("Schedule type must be 'interval' or 'cron'")

        return True

    def get_default_config_path(self) -> str:
        """Get default configuration file path.

        Returns:
            Default configuration file path
        """
        home_dir = Path.home()
        config_dir = home_dir / ".config" / "auto-website-visitor"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.yaml")

    def create_sample_config(self, config_path: str) -> None:
        """Create a sample configuration file.

        Args:
            config_path: Path to create sample configuration
        """
        # FIX: Create sample settings with proper default values
        # This ensures the sample config is created without validation issues
        sample_settings = VisitorSettings(
            url="https://example.com",
            visit_count=5,
            browser="chrome",
            headless=True,
            auto_scroll=True,
            schedule_enabled=False,
            log_level="INFO",
        )

        # Temporarily replace settings to save sample
        original_settings = self.settings
        self.settings = sample_settings
        self.save_config(config_path, "yaml")
        self.settings = original_settings
