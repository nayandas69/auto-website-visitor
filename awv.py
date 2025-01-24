import os
import time
import logging
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

# Initialize colorama (cuz we love colors, duh 🌈)
init(autoreset=True)

# Constants (AKA the VIPs of this script)
REPO_URL = "https://github.com/nayandas69/auto-website-visitor"
LATEST_RELEASE_API = "https://api.github.com/repos/nayandas69/auto-website-visitor/releases/latest"
CURRENT_VERSION = "0.0.4"
CACHE_DIR = os.path.expanduser("~/.browser_driver_cache")  # Browser driver cache for quicker setups
MIN_INTERVAL_SECONDS = 5  # Minimum interval to keep it lowkey, ya know 😎
LOG_DIR = "logs"  # Logs folder so we don’t lose receipts
LOG_FILE = os.path.join(LOG_DIR, "visit_log.log")

# Author Info (cuz credit is due, always)
AUTHOR_INFO = f"""
{Fore.CYAN}Author: {Fore.GREEN}Nayan Das
{Fore.CYAN}Version: {Fore.GREEN}{CURRENT_VERSION}
{Fore.CYAN}Website: {Fore.BLUE}https://socialportal.nayanchandradas.com
{Fore.CYAN}Email: {Fore.RED}nayanchandradas@hotmail.com
"""

# Logging Config (keeping it professional AND cool)
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
    """Decorator to handle bad Wi-Fi vibes (aka no internet moments) and retry."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                logging.warning("Wi-Fi went poof. Retrying in 1 min...")
                print(f"{Fore.RED}No internet. Retrying in 1 minute...")
                time.sleep(60)
    return wrapper

def validate_proxy(proxy):
    """Proxy checker so you don’t enter sus URLs."""
    try:
        if not proxy.startswith(('http://', 'https://')):
            raise ValueError("Proxy must start with 'http://' or 'https://'!")
        protocol, address = proxy.split('://')
        host, port = address.split(':')
        int(port)  # Just checking if port’s a number
        return True
    except (ValueError, AttributeError):
        return False

def ensure_log_file():
    """Make sure the log file’s always ready to spill the tea."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w'):
            pass
ensure_log_file()

def get_user_input():
    """This is where the vibes start: grab user input for max customization."""
    website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")
    while not website_url.startswith("http"):
        print(f"{Fore.RED}Invalid URL. Use something that starts with http:// or https://.")
        website_url = input(f"{Fore.CYAN}Enter the website URL: {Fore.WHITE}")

    visit_count = input(f"{Fore.CYAN}Enter the number of visits (0 for infinite): {Fore.WHITE}")
    while not visit_count.isdigit():
        print(f"{Fore.RED}Numbers only, please!")
        visit_count = input(f"{Fore.CYAN}Enter the number of visits (0 for infinite): {Fore.WHITE}")
    visit_count = int(visit_count)

    visit_interval = input(f"{Fore.CYAN}Enter visit interval in seconds (min {MIN_INTERVAL_SECONDS}s): {Fore.WHITE}")
    while not visit_interval.isdigit() or int(visit_interval) < MIN_INTERVAL_SECONDS:
        print(f"{Fore.RED}Keep it chill with at least {MIN_INTERVAL_SECONDS} seconds between visits.")
        visit_interval = input(f"{Fore.CYAN}Enter visit interval in seconds (min {MIN_INTERVAL_SECONDS}s): {Fore.WHITE}")
    visit_interval = int(visit_interval)

    browser = input(f"{Fore.CYAN}Choose your browser (chrome/firefox): {Fore.WHITE}").lower()
    while browser not in ["chrome", "firefox"]:
        print(f"{Fore.RED}Pick a squad: 'chrome' or 'firefox'.")
        browser = input(f"{Fore.CYAN}Choose your browser (chrome/firefox): {Fore.WHITE}").lower()

    headless = input(f"{Fore.CYAN}Run it in headless mode? (y/n): {Fore.WHITE}").strip().lower() == 'y'

    use_proxy = input(f"{Fore.CYAN}Want to use a proxy? (y/n): {Fore.WHITE}").strip().lower() == 'y'
    proxy = None
    if use_proxy:
        proxy = input(f"{Fore.CYAN}Enter proxy URL (e.g., http://host:port): {Fore.WHITE}")
        while not validate_proxy(proxy):
            print(f"{Fore.RED}Nah fam, that’s not it. Try again.")
            proxy = input(f"{Fore.CYAN}Enter proxy URL (e.g., http://host:port): {Fore.WHITE}")

    return website_url, visit_count, visit_interval, browser, headless, proxy

def create_driver(browser, headless, proxy=None):
    """Driver setup (cuz every mission needs a good ride)."""
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
    raise ValueError("Unsupported browser. Pick chrome or firefox.")

def visit_website(driver, url, visit_number):
    """Pull up to the URL and do the deed."""
    try:
        logging.info(f"Visit {visit_number}: Hitting up {url}.")
        driver.get(url)
        logging.info(f"Visit {visit_number}: All good in the hood.")
        print(f"{Fore.GREEN}Visit {visit_number}: Successfully visited {url}.")
    except Exception as e:
        logging.error(f"Visit {visit_number} flopped: {e}")
        print(f"{Fore.RED}Visit {visit_number} flopped: {e}")

def visit_task(url, visit_count, interval, browser, headless, proxy):
    """Run the actual mission (aka visiting the website)."""
    driver = create_driver(browser, headless, proxy)
    try:
        visit_number = 1
        while visit_count == 0 or visit_number <= visit_count:
            visit_website(driver, url, visit_number)
            visit_number += 1
            if visit_count and visit_number > visit_count:
                break
            print(f"{Fore.YELLOW}Taking a {interval}s power nap before the next run...")
            time.sleep(interval)
        print(f"{Fore.GREEN}Mission accomplished. All visits done!")
    finally:
        driver.quit()

@retry_on_disconnect
def check_for_update():
    """Check GitHub for updates cuz FOMO is real."""
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
            print(f"{Fore.BLUE}What’s New:\n{Style.BRIGHT}{whats_new}")
        else:
            print(f"{Fore.GREEN}You’re already on the latest and greatest.")
    except requests.RequestException as e:
        logging.error(f"Update check failed: {e}")
        print(f"{Fore.RED}Could not check for updates: {e}")

def show_help():
    """Help menu: the chill tour of what’s poppin’."""
    print(f"{Fore.YELLOW}Here’s how to slay with Auto Website Visitor:")
    print("1. Start - Automates website visits based on your vibes.")
    print("2. Check Update - Stay updated, stay relevant.")
    print("3. Help - Find out how to flex this tool.")
    print("4. Exit - Peace out.")
    print("Logs? Oh, they’re safe in the logs folder for ya.")

def exit_app():
    """Wave goodbye with style."""
    print(f"{Fore.YELLOW}Thanks for vibing with Auto Website Visitor! Catch you later! ")
    sys.exit(0)

def start():
    """Start the whole deal: grab input, do the magic."""
    url, count, interval, browser, headless, proxy = get_user_input()
    confirm = input(f"{Fore.YELLOW}Ready to roll? (y/n): {Fore.WHITE}").lower()
    if confirm == 'y':
        print(f"{Fore.GREEN}Here we gooooo!")
        visit_task(url, count, interval, browser, headless, proxy)
    else:
        print(f"{Fore.RED}Aight, maybe next time.")

def main():
    """CLI menu, the HQ of this whole thing."""
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
            print(f"{Fore.RED}Not a valid choice. Try again, champ.")

if __name__ == "__main__":
    main()
