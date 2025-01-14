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
CURRENT_VERSION = "0.0.2"
CACHE_DIR = os.path.expanduser("~/.browser_driver_cache")
MIN_INTERVAL_SECONDS = 5

# Author Information with color
AUTHOR_INFO = f"""
{Fore.CYAN}Author: {Fore.GREEN}Nayan Das
{Fore.CYAN}Version: {Fore.GREEN}{CURRENT_VERSION}
{Fore.CYAN}Website: {Fore.BLUE}https://socialportal.nayanchandradas.com
{Fore.CYAN}Email: {Fore.RED}nayanchandradas@hotmail.com
"""

# Setup logging
log_file = 'logs/visit_log.log'
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.getLogger('').addHandler(console_handler)

def ensure_log_file():
    """Ensure the log file exists."""
    if not os.path.exists(log_file):
        with open(log_file, 'w'):
            pass

ensure_log_file()

def retry_on_disconnect(func):
    """Decorator to retry a function if the internet is disconnected."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                logging.warning("No internet connection detected. Retrying in 1 minute...")
                time.sleep(60)
                print(f"{Fore.RED}No internet. Ensure a connection and retry in a minute.")
                return
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

def get_user_input():
    """Prompt user for all necessary details."""
    website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")

    # Validate URL
    while not website_url.startswith("http"):
        print(f"{Fore.RED}Invalid URL. Please enter a valid URL starting with http:// or https://.")
        website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")

    visit_count = input(f"{Fore.CYAN}Enter the number of visits (enter 0 for unlimited visits): {Fore.WHITE}")
    while not visit_count.isdigit():
        print(f"{Fore.RED}Invalid input for visit count. Please enter a number.")
        visit_count = input(f"{Fore.CYAN}Enter the number of visits (enter 0 for unlimited visits): {Fore.WHITE}")
    visit_count = int(visit_count) if visit_count.isdigit() else 0

    visit_interval_seconds = input(f"{Fore.CYAN}Enter the visit interval in seconds (minimum {MIN_INTERVAL_SECONDS} seconds): {Fore.WHITE}")
    while not visit_interval_seconds.isdigit() or int(visit_interval_seconds) < MIN_INTERVAL_SECONDS:
        print(f"{Fore.RED}Invalid input. Interval must be at least {MIN_INTERVAL_SECONDS} seconds.")
        visit_interval_seconds = input(f"{Fore.CYAN}Enter the visit interval in seconds (minimum {MIN_INTERVAL_SECONDS} seconds): {Fore.WHITE}")
    visit_interval_seconds = int(visit_interval_seconds)

    browser = input(f"{Fore.CYAN}Choose browser (chrome/firefox): {Fore.WHITE}").lower()
    while browser not in ["chrome", "firefox"]:
        print(f"{Fore.RED}Invalid browser choice. Please choose 'chrome' or 'firefox'.")
        browser = input(f"{Fore.CYAN}Choose browser (chrome/firefox): {Fore.WHITE}").lower()

    headless = input(f"{Fore.CYAN}Run in headless mode? (y/n): {Fore.WHITE}").strip().lower() == 'y'
    
    use_proxy = input(f"{Fore.CYAN}Do you want to use a proxy? (y/n): {Fore.WHITE}").strip().lower() == 'y'
    proxy = None
    if use_proxy:
        proxy = input(f"{Fore.CYAN}Enter your proxy URL (e.g., http://123.45.67.89:8080): {Fore.WHITE}")
        while not validate_proxy(proxy):
            print(f"{Fore.RED}Invalid proxy format. Please use the format http://host:port.")
            proxy = input(f"{Fore.CYAN}Enter your proxy URL (e.g., http://123.45.67.89:8080): {Fore.WHITE}")

    return website_url, visit_count, visit_interval_seconds, browser, headless, proxy

def create_driver(browser, headless, proxy=None):
    """Create a web driver based on the user's choice of browser, headless mode, and proxy."""
    os.environ['WDM_CACHE'] = CACHE_DIR

    options = None
    driver = None

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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
            options.set_preference("network.proxy.ssl", host)
            options.set_preference("network.proxy.ssl_port", int(port))

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    return driver

def visit_website(driver, url, visit_number):
    """Perform a website visit and log the result."""
    try:
        logging.info(f"Initiating visit {visit_number} to {url}.")
        driver.get(url)
        logging.info(f"Visit {visit_number}: Successfully visited {url}.")
        print(f"{Fore.GREEN}Visit {visit_number}: Successfully visited {url}.")
    except Exception as e:
        logging.error(f"Visit {visit_number} failed: {str(e)}")
        print(f"{Fore.RED}Visit {visit_number} failed: {str(e)}")

def visit_task(website_url, visit_count, visit_interval_seconds, browser, headless, proxy):
    """Execute the website visit task based on user inputs."""
    driver = create_driver(browser, headless, proxy)

    visit_number = 1
    while visit_count == 0 or visit_number <= visit_count:
        visit_website(driver, website_url, visit_number)
        if visit_count != 0 and visit_number >= visit_count:
            break
        visit_number += 1
        print(f"{Fore.YELLOW}Waiting for {visit_interval_seconds} seconds before the next visit...\n")
        time.sleep(visit_interval_seconds)

    print(f"{Fore.GREEN}Visit task completed successfully!")
    driver.quit()

@retry_on_disconnect
def check_for_update():
    """Check the GitHub API for the latest release and compare it with the user's current version."""
    print(f"{Fore.CYAN}Checking for updates...")
    try:
        response = requests.get(LATEST_RELEASE_API)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release.get("tag_name", "Unknown")
        whats_new = latest_release.get("body", "No information provided.")

        print(f"{Fore.GREEN}Your Current Version: {CURRENT_VERSION}")

        if latest_version != CURRENT_VERSION:
            print(f"{Fore.YELLOW}Latest Version Available: {latest_version}")
            print(f"{Fore.BLUE}What's New:\n{Style.BRIGHT}{whats_new}\n")

            choice = input(f"{Fore.YELLOW}Would you like to update to the latest version? (y/n): ").strip().lower()
            if choice == 'y':
                print(f"{Fore.CYAN}Download the latest .exe file here: {REPO_URL}/releases/latest")
                print(f"{Fore.CYAN}If using via pip, run: {Fore.GREEN}pip install --upgrade auto-website-visitor")
            elif choice == 'n':
                print(f"{Fore.YELLOW}New version {latest_version} is waiting for you!")
            else:
                print(f"{Fore.RED}Invalid choice. Please select 'y' or 'n'.")
        else:
            print(f"{Fore.GREEN}You are already using the latest version: {CURRENT_VERSION}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error while checking for updates: {e}")

def show_help():
    """Display help information about the app."""
    print(f"{Fore.YELLOW}How to use this CLI Auto Website Visitor:")
    print("1. Start - Initiates website visits based on your input.")
    print("2. Check Update - Checks for the latest version from the repository.")
    print("3. Help - Shows instructions for using the application.")
    print("4. Exit - Exits the application with a goodbye message.")
    print("Logs are maintained for your convenience.")
    print("For issues or suggestions, please contact the author:")

def exit_app():
    """Exit the program with a goodbye message.""" 
    print("Thank you for using Auto Website Visitor!")
    print("For more information, visit the author's website.")
    print("Goodbye!")
    sys.exit(0)

def start():
    """Start the visit task after gathering user inputs."""
    website_url, visit_count, visit_interval_seconds, browser, headless, proxy = get_user_input()

    print(f"\n{Fore.CYAN}You have entered the following details:")
    print(f"Website URL: {Fore.GREEN}{website_url}")
    print(f"Visit Count: {Fore.GREEN}{visit_count if visit_count != 0 else 'Unlimited'}")
    print(f"Visit Interval: {Fore.GREEN}{visit_interval_seconds} seconds")
    print(f"Browser: {Fore.GREEN}{browser}")
    print(f"Headless Mode: {Fore.GREEN}{headless}")
    if proxy:
        print(f"Using Proxy: {Fore.GREEN}{proxy}")
    else:
        print(f"Not using any proxy.")

    confirmation = input(f"{Fore.YELLOW}Do you want to start with these details? (y/n): {Fore.WHITE}").strip().lower()

    if confirmation == "y":
        print(f"{Fore.GREEN}Starting the visits...\n")
        visit_task(website_url, visit_count, visit_interval_seconds, browser, headless, proxy)
    else:
        print(f"{Fore.RED}Operation aborted by user.")

def main():
    """Main CLI menu for user to select options."""
    while True:
        print(AUTHOR_INFO)
        print(f"{Fore.CYAN}Please choose an option:")
        print(f"{Fore.YELLOW}1. Start")
        print(f"{Fore.YELLOW}2. Check Update")
        print(f"{Fore.YELLOW}3. Help")
        print(f"{Fore.YELLOW}4. Exit")
        choice = input(f"{Fore.CYAN}Enter your choice (1/2/3/4): ")

        if choice == "1":
            start()
        elif choice == "2":
            check_for_update()
        elif choice == "3":
            show_help()
        elif choice == "4":
            exit_app()
            break
        else:
            print(f"{Fore.RED}Invalid choice, please try again.")

if __name__ == "__main__":
    main()
