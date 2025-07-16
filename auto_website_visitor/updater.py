#!/usr/bin/env python3

"""Auto-update functionality for Auto Website Visitor."""

import requests
import subprocess
import sys
from typing import Optional, Tuple
from packaging import version

from .logger import VisitorLogger


class AutoUpdater:
    """Handles automatic updates for the package."""

    def __init__(self, logger: VisitorLogger, current_version: str = "3.0.0"):
        """Initialize auto updater.

        Args:
            logger: Logger instance
            current_version: Current package version
        """
        self.logger = logger
        self.current_version = current_version
        self.pypi_url = "https://pypi.org/pypi/auto-website-visitor/json"

    def check_for_updates(self) -> Optional[str]:
        """Check for available updates.

        Returns:
            Latest version if update available, None otherwise
        """
        try:
            self.logger.info("Checking for updates...")

            response = requests.get(self.pypi_url, timeout=10)
            response.raise_for_status()

            data = response.json()
            latest_version = data["info"]["version"]

            if version.parse(latest_version) > version.parse(self.current_version):
                self.logger.info(
                    f"Update available: {self.current_version} -> {latest_version}"
                )
                return latest_version
            else:
                self.logger.info("No updates available")
                return None

        except requests.RequestException as e:
            self.logger.warning(f"Failed to check for updates: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            return None

    def update_package(self, target_version: Optional[str] = None) -> bool:
        """Update the package to the latest or specified version.

        Args:
            target_version: Specific version to update to (optional)

        Returns:
            True if update was successful, False otherwise
        """
        try:
            package_spec = "auto-website-visitor"
            if target_version:
                package_spec += f"=={target_version}"

            self.logger.info(f"Updating package: {package_spec}")

            # Run pip install --upgrade
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", package_spec],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                self.logger.info("Package updated successfully")
                self.logger.info(
                    "Please restart the application to use the new version"
                )
                return True
            else:
                self.logger.error(f"Update failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.error("Update timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error during update: {e}")
            return False

    def get_version_info(self) -> Tuple[str, Optional[str]]:
        """Get current and latest version information.

        Returns:
            Tuple of (current_version, latest_version)
        """
        latest_version = self.check_for_updates()
        return self.current_version, latest_version

    def auto_update_if_available(self) -> bool:
        """Automatically update if a new version is available.

        Returns:
            True if update was performed, False otherwise
        """
        latest_version = self.check_for_updates()
        if latest_version:
            return self.update_package(latest_version)
        return False
