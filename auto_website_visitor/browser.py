#!/usr/bin/env python3

"""Browser management for Auto Website Visitor."""

import time
import random
import os
import shutil
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .config import VisitorSettings
from .logger import VisitorLogger


class BrowserManager:
    """Manages browser instances and automation."""

    def __init__(self, settings: VisitorSettings, logger: VisitorLogger):
        """Initialize browser manager.

        Args:
            settings: Visitor settings
            logger: Logger instance
        """
        self.settings = settings
        self.logger = logger
        self.driver: Optional[webdriver.Remote] = None
        self._check_browser_availability()

    def _check_browser_availability(self) -> None:
        """Check if the selected browser is available and install/update drivers if needed."""
        browser_name = self.settings.browser.lower()

        # Check if browser executable exists
        browser_paths = {
            "chrome": [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ],
            "firefox": [
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
                "/usr/bin/firefox",
                "/Applications/Firefox.app/Contents/MacOS/firefox",
            ],
            "edge": [
                "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
                "/usr/bin/microsoft-edge",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            ],
        }

        browser_found = False
        if browser_name in browser_paths:
            for path in browser_paths[browser_name]:
                if os.path.exists(path):
                    browser_found = True
                    self.logger.info(
                        f"✓ {browser_name.title()} browser found at: {path}"
                    )
                    break

        if not browser_found:
            self.logger.failure(f"✗ {browser_name.title()} browser not found!")
            self.logger.info(f"Please install {browser_name.title()} browser:")
            if browser_name == "chrome":
                self.logger.info("  Download from: https://www.google.com/chrome/")
            elif browser_name == "firefox":
                self.logger.info("  Download from: https://www.mozilla.org/firefox/")
            elif browser_name == "edge":
                self.logger.info("  Download from: https://www.microsoft.com/edge/")
            raise WebDriverException(f"{browser_name.title()} browser is not installed")

        # Check and setup WebDriver with caching
        self._setup_webdriver_cache()

    def _setup_webdriver_cache(self) -> None:
        """Setup WebDriver with intelligent caching and updates."""
        browser_name = self.settings.browser.lower()

        try:
            self.logger.info(f"🔍 Checking {browser_name} WebDriver cache...")

            if browser_name == "chrome":
                # Check cache first, then download/update if needed
                driver_path = ChromeDriverManager().install()
                self.logger.success(f"✓ Chrome WebDriver ready: {driver_path}")

            elif browser_name == "firefox":
                driver_path = GeckoDriverManager().install()
                self.logger.success(f"✓ Firefox WebDriver ready: {driver_path}")

            elif browser_name == "edge":
                driver_path = EdgeChromiumDriverManager().install()
                self.logger.success(f"✓ Edge WebDriver ready: {driver_path}")

        except Exception as e:
            self.logger.failure(f"✗ WebDriver setup failed: {e}")
            self.logger.info("Attempting to clear cache and retry...")

            # Clear webdriver cache and retry
            try:
                cache_dir = os.path.expanduser("~/.wdm")
                if os.path.exists(cache_dir):
                    shutil.rmtree(cache_dir)
                    self.logger.info("🗑️ WebDriver cache cleared")

                # Retry after cache clear
                if browser_name == "chrome":
                    driver_path = ChromeDriverManager().install()
                elif browser_name == "firefox":
                    driver_path = GeckoDriverManager().install()
                elif browser_name == "edge":
                    driver_path = EdgeChromiumDriverManager().install()

                self.logger.success(
                    f"✓ WebDriver installed successfully after cache clear"
                )

            except Exception as retry_error:
                self.logger.failure(
                    f"✗ WebDriver installation failed even after cache clear: {retry_error}"
                )
                raise WebDriverException(
                    f"Could not setup WebDriver for {browser_name}: {retry_error}"
                )

    def create_driver(self) -> webdriver.Remote:
        """Create and configure WebDriver instance.

        Returns:
            Configured WebDriver instance

        Raises:
            WebDriverException: If driver creation fails
        """
        try:
            if self.settings.browser == "chrome":
                return self._create_chrome_driver()
            elif self.settings.browser == "firefox":
                return self._create_firefox_driver()
            elif self.settings.browser == "edge":
                return self._create_edge_driver()
            else:
                raise ValueError(f"Unsupported browser: {self.settings.browser}")
        except Exception as e:
            self.logger.error(f"Failed to create {self.settings.browser} driver: {e}")
            raise WebDriverException(f"Driver creation failed: {e}")

    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create Chrome WebDriver."""
        options = ChromeOptions()

        if self.settings.headless:
            options.add_argument("--headless")

        # Common Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")

        # User agent
        if self.settings.user_agent:
            options.add_argument(f"--user-agent={self.settings.user_agent}")

        # Proxy configuration
        if self.settings.proxy:
            proxy_config = self._format_proxy()
            options.add_argument(f"--proxy-server={proxy_config}")

        # Custom headers
        if self.settings.custom_headers:
            for key, value in self.settings.custom_headers.items():
                options.add_argument(f"--header={key}:{value}")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create Firefox WebDriver."""
        options = FirefoxOptions()

        if self.settings.headless:
            options.add_argument("--headless")

        # User agent
        if self.settings.user_agent:
            options.set_preference(
                "general.useragent.override", self.settings.user_agent
            )

        # Proxy configuration
        if self.settings.proxy:
            proxy_parts = self.settings.proxy.split(":")
            if len(proxy_parts) >= 2:
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.http", proxy_parts[0])
                options.set_preference("network.proxy.http_port", int(proxy_parts[1]))
                options.set_preference("network.proxy.ssl", proxy_parts[0])
                options.set_preference("network.proxy.ssl_port", int(proxy_parts[1]))

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    def _create_edge_driver(self) -> webdriver.Edge:
        """Create Edge WebDriver."""
        options = EdgeOptions()

        if self.settings.headless:
            options.add_argument("--headless")

        # Common Edge options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # User agent
        if self.settings.user_agent:
            options.add_argument(f"--user-agent={self.settings.user_agent}")

        # Proxy configuration
        if self.settings.proxy:
            proxy_config = self._format_proxy()
            options.add_argument(f"--proxy-server={proxy_config}")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    def _format_proxy(self) -> str:
        """Format proxy configuration.

        Returns:
            Formatted proxy string
        """
        proxy = self.settings.proxy

        # Handle authenticated proxy
        if self.settings.proxy_user and self.settings.proxy_pass:
            if "@" not in proxy:
                proxy = f"{self.settings.proxy_user}:{self.settings.proxy_pass}@{proxy}"

        return proxy

    def visit_website(self) -> bool:
        """Visit the configured website.

        Returns:
            True if visit was successful, False otherwise
        """
        if not self.driver:
            self.driver = self.create_driver()

        try:
            self.logger.info(f"Visiting: {self.settings.url}")

            # Set page load timeout
            self.driver.set_page_load_timeout(self.settings.timeout)

            # Navigate to URL
            self.driver.get(self.settings.url)

            # Wait for page to load
            WebDriverWait(self.driver, self.settings.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Auto scroll if enabled
            if self.settings.auto_scroll:
                self._auto_scroll()

            # Random delay if enabled
            if self.settings.random_delay:
                delay = random.randint(*self.settings.delay_range)
                self.logger.debug(f"Random delay: {delay} seconds")
                time.sleep(delay)

            self.logger.success("✓ Website visit completed successfully")
            return True

        except TimeoutException:
            self.logger.failure(f"✗ Timeout loading page: {self.settings.url}")
            return False
        except WebDriverException as e:
            self.logger.failure(f"✗ WebDriver error: {e}")
            return False
        except Exception as e:
            self.logger.failure(f"✗ Unexpected error during visit: {e}")
            return False

    def _auto_scroll(self) -> None:
        """Perform automatic scrolling on the page."""
        try:
            self.logger.debug("Starting auto-scroll")

            for i in range(self.settings.max_scroll):
                # Scroll down
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(self.settings.scroll_pause)

                # Check if we've reached the bottom
                current_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if i > 0 and current_height == self._last_height:
                    self.logger.debug("Reached bottom of page")
                    break

                self._last_height = current_height

            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(self.settings.scroll_pause)

            self.logger.debug("Auto-scroll completed")

        except Exception as e:
            self.logger.warning(f"Auto-scroll failed: {e}")

    def close(self) -> None:
        """Close the browser driver."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.debug("Browser driver closed")
            except Exception as e:
                self.logger.warning(f"Error closing driver: {e}")
            finally:
                self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
