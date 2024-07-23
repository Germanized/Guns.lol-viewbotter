import chromedriver_autoinstaller
import undetected_chromedriver as uc
import random
import time
import sys
import os
import signal
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Paths to the Chrome executable
CHROME_EXECUTABLE_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Path to your Chrome executable

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
]

# Target URL
target_url = "https://guns.lol/pronhubstar"

# ANSI color codes for styling
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_logo():
    logo = f"""
{bcolors.HEADER}
  ____                   _       _   _  ___ _ _
 / ___|_   _ _ __  ___  | | ___ | | | |/ (_) | | __ _
| |  _| | | | '_ \/ __| | |/ _ \| | | ' /| | | |/ _` |
| |_| | |_| | | | \__ \_| | (_) | | | . \| | | | (_| |
 \____|\__,_|_| |_|___(_)_|\___/|_| |_|\_\_|_|_|\__,_|
{bcolors.ENDC}
    """
    print(logo)

def load_proxies_from_file(file_path):
    proxies = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("http://") or line.startswith("https://"):
                    proxies.append(line)
    except FileNotFoundError:
        print(f"{bcolors.FAIL}Proxy file not found: {file_path}{bcolors.ENDC}")
        sys.exit()
    return proxies

def get_random_proxy(proxies):
    proxy_url = random.choice(proxies)
    return {"http": proxy_url, "https": proxy_url}

def get_random_user_agent():
    return random.choice(user_agents)

def get_chrome_options():
    options = uc.ChromeOptions()
    options.binary_location = CHROME_EXECUTABLE_PATH  # Set the path to your Chrome executable
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')  # Set a default window size
    options.add_argument(f'--user-agent={get_random_user_agent()}')  # Set a random user agent
    return options

def simulate_view(proxies):
    proxy = get_random_proxy(proxies)
    options = get_chrome_options()
    options.add_argument(f'--proxy-server={proxy["http"]}')  # Set the proxy

    driver = None
    success = False
    reason = None
    try:
        # Install the correct version of ChromeDriver
        chromedriver_autoinstaller.install()  # Automatically install ChromeDriver for the current Chrome version

        driver = uc.Chrome(
            options=options,
            version_main=103  # Set the version of ChromeDriver to match Chrome version 106
        )
        driver.get(target_url)

        # Wait until the page is fully loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Ensure the page is scrolled to the top
        driver.execute_script("window.scrollTo(0, 0);")

        # Get the page dimensions
        body = driver.find_element(By.TAG_NAME, "body")
        body_width = body.size['width']
        body_height = body.size['height']

        # Calculate the center of the page
        x_center = body_width / 2
        y_center = body_height / 2

        # Perform a click action in the middle of the page
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(body, x_center, y_center).click().perform()

        # Check for successful view simulation
        print(f"{bcolors.OKGREEN}View simulated successfully! | Proxy: {proxy['http']} | User-Agent: {get_random_user_agent()}{bcolors.ENDC}")
        success = True
    except Exception as e:
        print(f"{bcolors.FAIL}Failed to simulate view: {e}{bcolors.ENDC}")
        reason = str(e)
    finally:
        if driver:
            driver.quit()  # Make sure to close the browser instance
        # Ensure the Chrome process is terminated
        kill_chrome_process()
    
    return success, reason

def kill_chrome_process():
    """Terminate any remaining Chrome processes."""
    try:
        # List all Chrome processes
        chrome_processes = subprocess.check_output('tasklist', shell=True).decode()
        if 'chrome.exe' in chrome_processes:
            subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'])
            print(f"{bcolors.WARNING}Terminated remaining Chrome processes.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}Failed to terminate Chrome processes: {e}{bcolors.ENDC}")

def start_view_botting(num_views, delay, proxies):
    hits = 0
    misses = 0
    for _ in range(num_views):
        success, reason = simulate_view(proxies)
        if success:
            hits += 1
        else:
            misses += 1
        # Update CMD window title
        set_cmd_title(f"Hits: {hits} Misses: {misses} - Last Error: {reason}")
        time.sleep(delay)

def show_menu(proxies):
    while True:
        print(f"{bcolors.OKCYAN}View Botter Menu{bcolors.ENDC}")
        print("1. Start View Botting")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            try:
                num_views = int(input("Enter the number of views to simulate: "))
                delay = float(input("Enter the delay between requests (in seconds): "))
                start_view_botting(num_views, delay, proxies)
            except ValueError:
                print(f"{bcolors.WARNING}Invalid input. Please enter numeric values.{bcolors.ENDC}")
        elif choice == '2':
            print(f"{bcolors.OKGREEN}Exiting...{bcolors.ENDC}")
            sys.exit()
        else:
            print(f"{bcolors.WARNING}Invalid choice. Please try again.{bcolors.ENDC}")

def set_cmd_title(title):
    os.system(f'title {title}')

if __name__ == "__main__":
    print_logo()
    
    # Set the CMD window title
    set_cmd_title("Github.com/germanized")
    
    # Load proxies from the 'proxy.txt' file
    proxies = load_proxies_from_file('proxy.txt')  # Updated to 'proxy.txt'
    show_menu(proxies)
