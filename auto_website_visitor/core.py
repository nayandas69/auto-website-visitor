#!/usr/bin/env python3

"""Core functionality for Auto Website Visitor."""

import time
from typing import Optional

from .config import VisitorSettings
from .logger import VisitorLogger
from .browser import BrowserManager


class AutoWebsiteVisitor:
    """Main class for automated website visiting."""

    def __init__(self, settings: VisitorSettings):
        """Initialize Auto Website Visitor.

        Args:
            settings: Visitor configuration settings
        """
        self.settings = settings
        self.logger = VisitorLogger(settings)
        self.browser_manager: Optional[BrowserManager] = None
        self.visit_count = 0
        self.success_count = 0
        self.failure_count = 0

    def run(self) -> bool:
        """Run the website visitor.

        Returns:
            True if all visits completed successfully, False otherwise
        """
        self.logger.info("Starting Auto Website Visitor")
        self.logger.info(f"Target URL: {self.settings.url}")
        self.logger.info(f"Visit count: {self.settings.visit_count}")
        self.logger.info(f"Browser: {self.settings.browser}")
        self.logger.info(f"Headless mode: {self.settings.headless}")

        try:
            with BrowserManager(self.settings, self.logger) as browser:
                self.browser_manager = browser

                for visit_num in range(1, self.settings.visit_count + 1):
                    self.logger.info(
                        f"Starting visit {visit_num}/{self.settings.visit_count}"
                    )

                    success = self._perform_visit_with_retry()

                    if success:
                        self.success_count += 1
                        self.logger.success(
                            f"✓ Visit {visit_num}/{self.settings.visit_count} completed successfully"
                        )
                    else:
                        self.failure_count += 1
                        self.logger.failure(
                            f"✗ Visit {visit_num}/{self.settings.visit_count} failed"
                        )

                    self.visit_count += 1

                    # Wait between visits (except for the last one)
                    if (
                        visit_num < self.settings.visit_count
                        and self.settings.interval > 0
                    ):
                        self.logger.info(
                            f"Waiting {self.settings.interval} seconds before next visit"
                        )
                        time.sleep(self.settings.interval)

                self._log_summary()
                return self.failure_count == 0

        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
        finally:
            self.browser_manager = None

    def _perform_visit_with_retry(self) -> bool:
        """Perform a single visit with retry logic.

        Returns:
            True if visit was successful, False otherwise
        """
        for attempt in range(1, self.settings.retry_attempts + 1):
            try:
                if self.browser_manager.visit_website():
                    return True
                else:
                    if attempt < self.settings.retry_attempts:
                        self.logger.warning(
                            f"Visit attempt {attempt} failed, retrying in {self.settings.retry_delay} seconds"
                        )
                        time.sleep(self.settings.retry_delay)
                    else:
                        self.logger.error(
                            f"All {self.settings.retry_attempts} attempts failed"
                        )
                        return False
            except Exception as e:
                self.logger.error(f"Visit attempt {attempt} failed with error: {e}")
                if attempt < self.settings.retry_attempts:
                    self.logger.info(f"Retrying in {self.settings.retry_delay} seconds")
                    time.sleep(self.settings.retry_delay)
                else:
                    return False

        return False

    def _log_summary(self) -> None:
        """Log execution summary."""
        self.logger.info("=== Execution Summary ===")
        self.logger.info(f"Total visits: {self.visit_count}")
        self.logger.info(f"Successful visits: {self.success_count}")
        self.logger.info(f"Failed visits: {self.failure_count}")

        if self.visit_count > 0:
            success_rate = (self.success_count / self.visit_count) * 100
            self.logger.info(f"Success rate: {success_rate:.1f}%")

    def get_stats(self) -> dict:
        """Get visitor statistics.

        Returns:
            Dictionary containing visitor statistics
        """
        return {
            "total_visits": self.visit_count,
            "successful_visits": self.success_count,
            "failed_visits": self.failure_count,
            "success_rate": (
                (self.success_count / self.visit_count * 100)
                if self.visit_count > 0
                else 0
            ),
        }
