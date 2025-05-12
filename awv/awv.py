#!/usr/bin/env python3
# awv.py

# -------------------------------------
# Auto Website Visitor
# Version: 0.0.8
# Author: nayandas69
# Website: https://nayandas69.github.io/link-in-bio
# Email: nayanchandradas@hotmail.com
# Description: A simple script to automate website visits using Selenium WebDriver.
# This script allows users to specify a website URL, the number of visits, the interval between visits,
# and the browser to use. It also supports headless mode, proxy usage, and auto-scrolling.
# License: MIT License
# Last Updated: 2025-5-12
# -------------------------------------


import os
import sys
import math
import time
import random
import logging
import requests
from selenium import webdriver
from colorama import Fore, Style, init
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Initialize colorama (cuz we love colors, duh)
init(autoreset=True)

# Constants
REPO_URL = "https://github.com/nayandas69/auto-website-visitor"
LATEST_RELEASE_API = (
    "https://api.github.com/repos/nayandas69/auto-website-visitor/releases/latest"
)
CURRENT_VERSION = "0.0.8"
CACHE_DIR = os.path.expanduser("~/.browser_driver_cache")
MIN_INTERVAL_SECONDS = 1
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "visit_log.log")
AUTHOR = "Nayan Das"
WEBSITE = "https://nayandas69.github.io/link-in-bio"
EMAIL = "nayanchandradas@hotmail.com"

# Author Info (cuz credit is due, always)
AUTHOR_INFO = f"""
{Fore.CYAN}Author: {Fore.GREEN}{AUTHOR}
{Fore.CYAN}Version: {Fore.GREEN}{CURRENT_VERSION}
{Fore.CYAN}Website: {Fore.BLUE}{WEBSITE}
{Fore.CYAN}Email: {Fore.RED}{EMAIL}
"""

# Logging Setup (Cuz debugging shouldn't feel like detective work)
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
logging.getLogger("").addHandler(console_handler)


def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rWaiting {remaining}s before next visit... 💤")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line afterwards


# Auto Retry for Disconnects (Cuz Wi-Fi be acting sus)
def retry_on_disconnect(func):
    """Decorator to handle bad Wi-Fi vibes (aka no internet moments) and retry after 1 min."""

    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                logging.warning("Wi-Fi went poof. Retrying in 1 min...")
                print(f"{Fore.RED}No internet. Retrying in 1 minute...")
                time.sleep(60)

    return wrapper


# Proxy Validator (No sus proxies allowed)
def validate_proxy(proxy):
    """Ensures the proxy ain't sketchy."""
    try:
        if not proxy.startswith(("http://", "https://")):
            raise ValueError("Proxy must start with 'http://' or 'https://'")
        protocol, address = proxy.split("://")
        host, port = address.split(":")
        int(port)  # Making sure port is a real number
        return True
    except (ValueError, AttributeError):
        return False


# Log File Setup (Cuz we need a place to spill the tea)
def ensure_log_file():
    """Make sure the log file’s always ready to spill the tea."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w"):
            pass


ensure_log_file()


# User Input - Your Playground
def get_user_input():
    """This is where the vibes start: grab user input for max customization."""
    website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")
    while not website_url.startswith("http"):
        print(
            f"{Fore.RED}Invalid URL. Use something that starts with http:// or https://."
        )
        website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")

    visit_count = input(
        f"{Fore.CYAN}Enter the number of visits (0 for infinite): {Fore.WHITE}"
    )
    while not visit_count.isdigit():
        print(f"{Fore.RED}Numbers only, please!")
        visit_count = input(
            f"{Fore.CYAN}Enter the number of visits (0 for infinite): {Fore.WHITE}"
        )
    visit_count = int(visit_count)

    visit_interval = input(
        f"{Fore.CYAN}Enter visit interval in seconds (min {MIN_INTERVAL_SECONDS}s): {Fore.WHITE}"
    )
    while not visit_interval.isdigit() or int(visit_interval) < MIN_INTERVAL_SECONDS:
        print(
            f"{Fore.RED}Keep it chill with at least {MIN_INTERVAL_SECONDS} seconds between visits."
        )
        visit_interval = input(
            f"{Fore.CYAN}Enter visit interval in seconds (min {MIN_INTERVAL_SECONDS}s): {Fore.WHITE}"
        )
    visit_interval = int(visit_interval)

    browser = input(
        f"{Fore.CYAN}Choose your browser (chrome/firefox/edge): {Fore.WHITE}"
    ).lower()
    while browser not in ["chrome", "firefox", "edge"]:
        print(f"{Fore.RED}Pick a squad: 'chrome', 'firefox', or 'edge'.")
        browser = input(
            f"{Fore.CYAN}Choose your browser (chrome/firefox/edge): {Fore.WHITE}"
        ).lower()

    use_proxy = (
        input(f"{Fore.CYAN}Want to use a proxy? (y/n): {Fore.WHITE}").strip().lower()
        == "y"
    )
    proxy = None
    if use_proxy:
        proxy = input(
            f"{Fore.CYAN}Enter proxy URL (e.g., http://host:port): {Fore.WHITE}"
        )
        while not validate_proxy(proxy):
            print(f"{Fore.RED}Nah fam, that’s not it. Try again.")
            proxy = input(
                f"{Fore.CYAN}Enter proxy URL (e.g., http://host:port): {Fore.WHITE}"
            )

    headless = (
        input(f"{Fore.CYAN}Run it in headless mode? (y/n): {Fore.WHITE}")
        .strip()
        .lower()
        == "y"
    )

    auto_scroll = (
        input(f"{Fore.CYAN}Enable auto-scroll? (y/n): {Fore.WHITE}").strip().lower()
    )
    auto_scroll = auto_scroll == "y"

    # Enforce minimum 10s interval for auto-scroll
    if auto_scroll and visit_interval < 10:
        print(
            f"{Fore.RED}Auto-scroll requires at least 10 seconds interval. Turning it off."
        )
        auto_scroll = False

    return (
        website_url,
        visit_count,
        visit_interval,
        browser,
        proxy,
        headless,
        auto_scroll,
    )


# WebDriver Setup (Chrome, Firefox or Edge)
def create_driver(browser, headless, proxy=None):
    """Driver setup (cuz every mission needs a good ride)."""
    os.environ["WDM_CACHE"] = CACHE_DIR
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if proxy:
            options.set_preference("network.proxy.type", 1)
            protocol, address = proxy.split("://")
            host, port = address.split(":")
            options.set_preference("network.proxy.ssl", host)
            options.set_preference("network.proxy.ssl_port", int(port))

        return webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()), options=options
        )

    raise ValueError("Unsupported browser. Pick chrome, firefox or edge.")


# Auto Scroll - New & Improved
def auto_human_scroll(driver, total_scroll_time):
    """
    Simulates human-like scrolling with a mix of scroll behaviors:
    - Scrolls down and up
    - Scrolls to specific elements if found
    - Scrolls to random vertical positions
    - Includes pauses to simulate reading
    """
    if total_scroll_time < 10:
        logging.warning("Auto-scroll skipped: interval too short (<10s).")
        return

    start_time = time.time()
    end_time = start_time + total_scroll_time

    scroll_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    logging.info(f"Starting human-like scroll for {total_scroll_time} seconds...")

    while time.time() < end_time:
        action_type = random.choice(
            ["pagedown", "pageup", "random_scroll", "element_scroll", "pause_reading"]
        )

        if action_type == "pagedown":
            driver.find_element("tag name", "body").send_keys(Keys.PAGE_DOWN)
            logging.debug("Scrolled: PAGE DOWN")

        elif action_type == "pageup":
            driver.find_element("tag name", "body").send_keys(Keys.PAGE_UP)
            logging.debug("Scrolled: PAGE UP")

        elif action_type == "random_scroll":
            target_position = random.randint(0, scroll_height - viewport_height)
            driver.execute_script(f"window.scrollTo(0, {target_position});")
            logging.debug(f"Scrolled to random position: {target_position}")

        elif action_type == "element_scroll":
            try:
                elements = driver.find_elements(
                    By.TAG_NAME, "p"
                )  # paragraphs are common reading spots
                if elements:
                    element = random.choice(elements)
                    driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        element,
                    )
                    logging.debug("Scrolled to paragraph element.")
            except Exception as e:
                logging.debug(f"Element scroll failed: {e}")

        elif action_type == "pause_reading":
            read_time = random.uniform(2, 4)
            logging.debug(f"Pausing to read... ({read_time:.1f}s)")
            time.sleep(read_time)
            continue

        time.sleep(random.uniform(1.0, 2.5))  # Delay between actions

    logging.info("Finished human-like auto-scrolling.")


# Visit Website
def visit_website(driver, url, visit_number, auto_scroll, visit_interval):
    """Visits the site & scrolls like a human if enabled."""
    try:
        logging.info(f"Visit {visit_number}: Pulling up to {url}...")
        driver.get(url)
        if auto_scroll:
            auto_human_scroll(driver, total_scroll_time=visit_interval)
        logging.info(f"Visit {visit_number}: Success!")
        print(f"{Fore.GREEN}Visit {visit_number}: Successfully vibed at {url}.")
    except Exception as e:
        logging.error(f"Visit {visit_number} failed: {e}")
        print(f"{Fore.RED}Visit {visit_number} failed: {e}")


# Visit Task
def visit_task(url, visit_count, interval, browser, headless, auto_scroll, proxy):
    """Runs the whole visit mission."""
    driver = create_driver(browser, headless, proxy)
    try:
        visit_number = 1
        while visit_count == 0 or visit_number <= visit_count:  # Fix applied
            visit_website(driver, url, visit_number, auto_scroll, interval)
            countdown_timer(interval)
            visit_number += 1  # Increment visit number manually

        print(f"{Fore.GREEN}Mission accomplished. All visits done!")

    except KeyboardInterrupt:
        print(f"{Fore.RED}\nCTRL + C detected! Exiting safely...")
    finally:
        driver.quit()


# Check for Updates (Cuz FOMO is real)
@retry_on_disconnect
# Check for Updates
def check_for_update():
    print(f"{Fore.GREEN}Current Version: {CURRENT_VERSION}")
    print(f"{Fore.CYAN}Checking for updates...")
    try:
        response = requests.get(LATEST_RELEASE_API)
        response.raise_for_status()
        latest_version = response.json().get("tag_name", CURRENT_VERSION)

        if latest_version != CURRENT_VERSION:
            print(
                f"{Fore.YELLOW}New version available: {latest_version}! Check it here: {REPO_URL}"
            )
        else:
            print(f"{Fore.GREEN}You're up-to-date!")
    except requests.RequestException:
        print(f"{Fore.RED}Could not check for updates.")


# Help Menu (Cuz we all need a little guidance)
def show_help():
    """Help menu: the chill tour of what’s poppin’."""
    print(f"{Fore.YELLOW}Here’s how to slay with Auto Website Visitor:")
    print("1. Start - Automates website visits based on your vibes.")
    print("2. Check Update - Stay updated, stay relevant.")
    print("3. Help - Find out how to flex this tool.")
    print("4. Exit - Peace out.")
    print("Logs? Oh, they’re safe in the logs folder for ya.")
    print(
        "\nHaving issues, bugs, or errors? For assistance, please contact the developer:"
    )


# Exit App (Cuz every good thing must come to an end)
def exit_app():
    """Wave goodbye with style."""
    print(
        f"{Fore.YELLOW}Thanks for vibing with Auto Website Visitor! Catch you later! "
    )
    sys.exit(0)


# Start
def start():
    """Handles user input and kicks off the script."""
    while True:
        url, count, interval, browser, proxy, headless, auto_scroll = get_user_input()
        confirm = input(f"{Fore.YELLOW}Ready to roll? (y/n/edit): {Fore.WHITE}").lower()
        if confirm == "y":
            print(f"{Fore.GREEN}Here we gooooo!")
            visit_task(
                url, count, interval, browser, headless, auto_scroll, proxy
            )  # Now passes proxy too
            break
        elif confirm == "edit":
            print(f"{Fore.YELLOW}No worries! Let's update your inputs.")
        else:
            print(f"{Fore.RED}Aight, maybe next time.")
            break


# CLI Menu (Cuz we love options)
def main():
    """CLI menu, the HQ of this whole thing."""
    print(Fore.CYAN + "Auto Website Visitor" + Fore.WHITE)
    print(
        f"{Fore.CYAN}Welcome to Auto Website Visitor! Let’s get this automated party started."
    )
    while True:
        print(AUTHOR_INFO)
        print(f"{Fore.CYAN}Options:\n1. Start\n2. Check for Updates\n3. Help\n4. Exit")
        choice = input(f"{Fore.CYAN}Enter choice (1/2/3/4): {Fore.WHITE}").strip()
        if choice == "1":
            start()
        elif choice == "2":
            check_for_update()
        elif choice == "3":
            show_help()
        elif choice == "4":
            exit_app()
        else:
            print(f"{Fore.RED}Not a valid choice. Try again, champ.")


# Main Entry Point
if __name__ == "__main__":
    main()
