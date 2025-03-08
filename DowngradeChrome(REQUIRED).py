import os
import shutil
import psutil
import subprocess
import requests
import time
from tqdm import tqdm
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import ctypes
import sys
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome"
UPDATE_PATH = r"C:\Program Files (x86)\Google\Update\GoogleUpdate.exe"
CHROME_DOWNLOAD_URL = "https://www.slimjet.com/chrome/download-chrome.php?file=files%2F103.0.5060.53%2FChromeStandaloneSetup.exe"
CHROME_INSTALLER = "ChromeStandaloneSetup.exe"

def is_elevated():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

def run_as_admin():
    if sys.argv[-1] != 'asadmin':
        script = sys.argv[0]
        params = " ".join(sys.argv[1:])
        subprocess.run(["python", script, *params, "asadmin"], shell=True)
        sys.exit()

def is_chrome_installed():
    return os.path.exists(CHROME_PATH)

def is_chrome_running():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            return True
    return False

def delete_chrome():
    if is_chrome_installed():
        console.print("[bold red]Deleting Chrome...[/bold red]")
        try:
            shutil.rmtree(CHROME_PATH)
            console.print("[green]Chrome deleted successfully.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error deleting Chrome: {e}[/bold red]")

def block_google_update():
    console.print("[bold yellow]Blocking Google Update in the firewall...[/bold yellow]")
    try:
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockGoogleUpdate", "dir=in", "program={}".format(UPDATE_PATH), "action=block"], check=True)
        console.print("[green]Firewall rule added successfully.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error adding firewall rule: {e}[/bold red]")

def download_chrome_installer():
    console.print("[bold cyan]Downloading Chrome Installer...[/bold cyan]")
    response = requests.get(CHROME_DOWNLOAD_URL, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(CHROME_INSTALLER, 'wb') as file, Progress() as progress:
        task = progress.add_task("[cyan]Downloading...", total=total_size)
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress.update(task, advance=len(data))

def install_chrome():
    console.print("[bold green]Installing Chrome...[/bold green]")
    try:
        subprocess.run([CHROME_INSTALLER, "/silent", "/install"], check=True)
        console.print("[green]Chrome installed successfully.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error installing Chrome: {e}[/bold red]")

def display_warnings():
    console.print(Panel("[bold red]!!! WARNING !!!\n\nIt is not recommended to use Chrome as your main browser for Guns.lol view bot usage.\nBrowsers like Opera GX, Arc, or Brave are safer from RATs and other security risks.\nThis process will delete your browser history and data if you continue using Chrome.\nProceeding will also block Chrome updates, ensuring Chrome will not automatically upgrade.\n\nProceeding with the deletion and installation of Chrome. Press 'Y' to continue or 'N' to cancel.[/bold red]", style="bold yellow"))

def create_tray_icon():
    def on_quit(icon, item):
        icon.stop()

    icon_image = Image.new('RGB', (64, 64), color=(0, 255, 0))
    icon_draw = ImageDraw.Draw(icon_image)
    icon_draw.text((10, 10), "Viewbot", fill=(255, 255, 255))

    icon = pystray.Icon("ChromeTool", icon_image, menu=pystray.Menu(item('Quit', on_quit)))
    icon.run()

def main():
    display_warnings()

    choice = Prompt.ask("Do you want to continue? (Y/N)", choices=["y", "n"])

    if choice != 'y':
        console.print("[bold red]Exiting tool. No changes were made.[/bold red]")
        return

    if is_chrome_installed() or is_chrome_running():
        delete_chrome()
        block_google_update()

    download_chrome_installer()
    install_chrome()

    console.print("[bold green]Chrome is ready to use for Guns.lol View Bot.[/bold green]")
    console.print("[bold yellow]Remember, using Chrome for this purpose is not recommended for your security.[/bold yellow]")

if __name__ == "__main__":
    if not is_elevated(): 
        run_as_admin() 
    create_tray_icon() 
    main()
