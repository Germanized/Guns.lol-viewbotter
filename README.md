# Guns.lol Killa Script

## Description

This script simulates views on a target URL using proxies and random user agents. It uses Selenium with Chrome to automate browser interactions. The script is designed to run headless, meaning no browser window will appear. It includes functionalities to handle proxies, simulate clicks, and manage Chrome processes.

## Author

This script is developed by Germanized.

## Requirements

- Python 3.x
- Google Chrome installed
- Required Python packages (install using `pip install -r requirements.txt`)

### Required Python Packages

- chromedriver-autoinstaller
- undetected-chromedriver
- selenium

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using the following command:

   ```bash
   pip install chromedriver-autoinstaller undetected-chromedriver selenium
Ensure Google Chrome is installed on your system.
Place your proxy list in a file named proxy.txt in the same directory as the script.
Configuration
File: proxy.txt
The proxy.txt file should contain a list of proxies in the following format:


http://proxy1:port
http://proxy2:port
https://proxy3:port
Script Settings
CHROME_EXECUTABLE_PATH: Path to your Google Chrome executable. Default is C:\Program Files\Google\Chrome\Application\chrome.exe.
version_main=103 <--------- change this to your chrome version in the script
target_url: The URL you want to simulate views on. Default is https://guns.lol/germanizd.

## Usage
Run the script:


python view_botter.py
Follow the on-screen menu:

Select 1 to start view botting.
Enter the number of views to simulate.
Enter the delay between requests (in seconds).
The script will start simulating views and display the results in the terminal.

## Functions
print_logo
Prints the script's logo.

## load_proxies_from_file(file_path)
Loads proxies from the specified file.

## get_random_proxy(proxies)
Returns a random proxy from the list of proxies.

## get_random_user_agent
Returns a random user agent from the predefined list.

## get_chrome_options
Sets up Chrome options for headless browsing and returns the options.

## simulate_view(proxies)
Simulates a view using a random proxy and user agent. Handles browser interactions.

## kill_chrome_process
Terminates any remaining Chrome processes.

## start_view_botting(num_views, delay, proxies)
Starts the view botting process with the specified number of views and delay between requests.

## show_menu(proxies)
Displays the menu for user interaction.

## set_cmd_title(title)
Sets the title of the command prompt window.

## Disclaimer
This script is for educational purposes only. The author is not responsible for any misuse of this script.
