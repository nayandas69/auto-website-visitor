import os
import time
import logging
import threading
import requests
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import sys

# Initialize colorama
init(autoreset=True)

# Constants
REPO_URL = "https://github.com/nayandas69/auto-website-visitor"
LATEST_RELEASE_API = "https://api.github.com/repos/nayandas69/auto-website-visitor/releases/latest"
CURRENT_VERSION = "0.0.3"
CACHE_DIR = os.path.expanduser("~/.browser_driver_cache")
MIN_INTERVAL_SECONDS = 5
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "visit_log.log")

# Author Information
AUTHOR_INFO = f"""
{Fore.CYAN}Author: {Fore.GREEN}Nayan Das
{Fore.CYAN}Version: {Fore.GREEN}{CURRENT_VERSION}
{Fore.CYAN}Website: {Fore.BLUE}https://socialportal.nayanchandradas.com
{Fore.CYAN}Email: {Fore.RED}nayanchandradas@hotmail.com
"""

# Logging Configuration
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger("").addHandler(console_handler)

def retry_on_disconnect(func):
    """Decorator to retry a function if the internet is disconnected."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                logging.warning("No internet connection detected. Retrying in 1 minute...")
                print(f"{Fore.RED}No internet. Retrying in 1 minute...")
                time.sleep(60)
    return wrapper

def validate_proxy(proxy):
    """Validate the format of the proxy."""
    try:
        if not proxy.startswith(('http://', 'https://')):
            raise ValueError("Proxy must start with 'http://' or 'https://'!")
        protocol, address = proxy.split('://')
        host, port = address.split(':')
        int(port)  # Ensure port is numeric
        return True
    except (ValueError, AttributeError):
        return False

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def ensure_log_file():
    """Ensure the log file exists."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w'):
            pass
ensure_log_file()

def get_user_input():
    """Prompt user for all necessary details."""
    website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")
    while not website_url.startswith("http"):
        print(f"{Fore.RED}Invalid URL. Please enter a valid URL starting with http:// or https://.")
        website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")

    visit_count = input(f"{Fore.CYAN}Enter the number of visits (0 for unlimited): {Fore.WHITE}")
    while not visit_count.isdigit():
        print(f"{Fore.RED}Invalid input. Please enter a number.")
        visit_count = input(f"{Fore.CYAN}Enter the number of visits (0 for unlimited): {Fore.WHITE}")
    visit_count = int(visit_count)

    visit_interval = input(f"{Fore.CYAN}Enter visit interval in seconds (minimum {MIN_INTERVAL_SECONDS}s): {Fore.WHITE}")
    while not visit_interval.isdigit() or int(visit_interval) < MIN_INTERVAL_SECONDS:
        print(f"{Fore.RED}Invalid interval. Must be at least {MIN_INTERVAL_SECONDS} seconds.")
        visit_interval = input(f"{Fore.CYAN}Enter visit interval in seconds (minimum {MIN_INTERVAL_SECONDS}s): {Fore.WHITE}")
    visit_interval = int(visit_interval)

    browser = input(f"{Fore.CYAN}Choose browser (chrome/firefox): {Fore.WHITE}").lower()
    while browser not in ["chrome", "firefox"]:
        print(f"{Fore.RED}Invalid choice. Select 'chrome' or 'firefox'.")
        browser = input(f"{Fore.CYAN}Choose browser (chrome/firefox): {Fore.WHITE}").lower()

    headless = input(f"{Fore.CYAN}Run in headless mode? (y/n): {Fore.WHITE}").strip().lower() == 'y'

    use_proxy = input(f"{Fore.CYAN}Do you want to use a proxy? (y/n): {Fore.WHITE}").strip().lower() == 'y'
    proxy = None
    if use_proxy:
        proxy = input(f"{Fore.CYAN}Enter proxy URL (e.g., http://host:port): {Fore.WHITE}")
        while not validate_proxy(proxy):
            print(f"{Fore.RED}Invalid proxy format. Use http://host:port.")
            proxy = input(f"{Fore.CYAN}Enter proxy URL (e.g., http://host:port): {Fore.WHITE}")

    return website_url, visit_count, visit_interval, browser, headless, proxy

def create_driver(browser, headless, proxy=None):
    """Create a web driver instance based on user inputs."""
    os.environ['WDM_CACHE'] = CACHE_DIR
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if proxy:
            options.set_preference("network.proxy.type", 1)
            protocol, address = proxy.split('://')
            host, port = address.split(':')
            options.set_preference("network.proxy.http", host)
            options.set_preference("network.proxy.http_port", int(port))
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    raise ValueError("Unsupported browser.")

def visit_website(driver, url, visit_number):
    """Perform a visit to the website."""
    try:
        logging.info(f"Visit {visit_number}: Navigating to {url}.")
        driver.get(url)
        logging.info(f"Visit {visit_number}: Success.")
        print(f"{Fore.GREEN}Visit {visit_number}: Successfully visited {url}.")
    except Exception as e:
        logging.error(f"Visit {visit_number} failed: {e}")
        print(f"{Fore.RED}Visit {visit_number} failed: {e}")

def visit_task(url, visit_count, interval, browser, headless, proxy):
    """Execute the website visits based on user input."""
    driver = create_driver(browser, headless, proxy)
    try:
        visit_number = 1
        while visit_count == 0 or visit_number <= visit_count:
            visit_website(driver, url, visit_number)
            visit_number += 1
            if visit_count and visit_number > visit_count:
                break
            print(f"{Fore.YELLOW}Waiting {interval}s before next visit...")
            time.sleep(interval)
        print(f"{Fore.GREEN}All visits completed successfully.")
    finally:
        driver.quit()

@retry_on_disconnect
def check_for_update():
    """Check the repository for updates."""
    print(f"{Fore.CYAN}Checking for updates...")
    try:
        response = requests.get(LATEST_RELEASE_API)
        response.raise_for_status()
        latest = response.json()
        latest_version = latest.get("tag_name", CURRENT_VERSION)
        whats_new = latest.get("body", "No details provided.")

        print(f"{Fore.GREEN}Current Version: {CURRENT_VERSION}")
        if latest_version != CURRENT_VERSION:
            print(f"{Fore.YELLOW}New Version Available: {latest_version}")
            print(f"{Fore.BLUE}What's New:\n{Style.BRIGHT}{whats_new}")
        else:
            print(f"{Fore.GREEN}You have the latest version.")
    except requests.RequestException as e:
        logging.error(f"Update check failed: {e}")
        print(f"{Fore.RED}Could not check for updates: {e}")

def show_help():
    """Display help information about the app."""
    print(f"{Fore.YELLOW}How to use Auto Website Visitor:")
    print("1. Start - Automates website visits based on user inputs.")
    print("2. Check Update - Ensures you have the latest version.")
    print("3. Help - Displays usage instructions.")
    print("4. Exit - Closes the application.")
    print("Logs are stored for reference.")
    print("For suggestions, contact the author!")

def exit_app():
    """Exit the program with a goodbye message."""
    print(f"{Fore.YELLOW}Thank you for using Auto Website Visitor!\nGoodbye!")
    sys.exit(0)

def start():
    """Gather input and start the visit task."""
    url, count, interval, browser, headless, proxy = get_user_input()
    confirm = input(f"{Fore.YELLOW}Confirm to start? (y/n): {Fore.WHITE}").lower()
    if confirm == 'y':
        print(f"{Fore.GREEN}Starting...")
        visit_task(url, count, interval, browser, headless, proxy)
    else:
        print(f"{Fore.RED}Aborted.")

def main():
    """Main CLI entry point."""
    while True:
        print(AUTHOR_INFO)
        print(f"{Fore.CYAN}Options:\n1. Start\n2. Check for Updates\n3. Help\n4. Exit")
        choice = input(f"{Fore.CYAN}Enter choice (1/2/3/4): {Fore.WHITE}").strip()
        if choice == '1':
            start()
        elif choice == '2':
            check_for_update()
        elif choice == '3':
            show_help()
        elif choice == '4':
            exit_app()
        else:
            print(f"{Fore.RED}Invalid choice.")

if __name__ == "__main__":
    main()
