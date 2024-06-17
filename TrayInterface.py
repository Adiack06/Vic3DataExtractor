import pystray
from tkinter import filedialog
from pystray import MenuItem as Item, Menu
from PIL import Image, ImageDraw
import threading
from scan import *
from Extractor import *
from dotenv import load_dotenv

load_dotenv()
'''
issue
no error shown to user if there isn't a starting save
'''

# env variables
outputfolder = os.getenv('OUTPUT_FOLDER')
documentsgamefolder = os.getenv('DOCUMENTS_GAME_FOLDER')

threads = []
stop_event = threading.Event()
# Create an icon image
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [(width // 2, 0), (width, height // 2)],
        fill=color2)
    dc.rectangle(
        [(0, height // 2), (width // 2, height)],
        fill=color2)

    return image

# Functions to handle menu items
def start_scanner(icon, item):
    global threads, stop_event
    if not any(thread.name == "Scanner" and thread.is_alive() for thread in threads):
        stop_event.clear()  # Reset the stop event
        scanner_thread = threading.Thread(target=scanner, args=(documentsgamefolder, outputfolder, stop_event), name="Scanner")
        threads.append(scanner_thread)
        scanner_thread.start()

def stop_scanner(icon, item):
    global stop_event
    stop_event.set()
    for thread in threads:
        if thread.name == "Scanner":
            thread.join()  # Ensure the thread has finished
    threads[:] = [thread for thread in threads if thread.is_alive()]
    stop_event.clear()
    pass

def melt_saves(icon, item):
    global saves_to_melt ,threads
    if saves_to_melt:
        stop_event.clear()  # Reset the stop event
        melter_thread = threading.Thread(target=meltsaves, args=(saves_to_melt, outputfolder),name="Scanner")
        threads.append(melter_thread)
        melter_thread.start()
    else:
        print("No saves selected to melt.")
def select_saves(icon, item):
    global saves_to_melt
    saves_to_melt = filedialog.askopenfilenames(filetypes=[("Saves", ".v3")])
    pass


def select_starting_save(icon, item):
    starting_save = filedialog.askopenfilename(filetypes=[("Save files", "*.v3")])

    if starting_save:
        destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
        os.makedirs(destination, exist_ok=True)
        shutil.copy(starting_save, destination)
def settings(icon, item):
    pass

def lock_to_mp(icon, item):
    pass

def link_with_web(icon, item):
    pass

def close_application(icon, item):
    stop_scanner(icon, item)
    icon.stop()

# Create menu
menu = Menu(
    Item('Start Scanner', start_scanner),
    Item('Select Starting Save', select_starting_save),
    Item('Stop Scanner', stop_scanner),
    Item('Melt Saves', Menu(
        Item('Select Saves', select_saves),
        Item('Progress %', lambda icon, item: None),
        Item('Melt Saves', melt_saves)
    )),
    Item('Settings', Menu(
        Item('Link with Web', link_with_web),
        Item('Lock to MP', lock_to_mp)
    )),
    Item('Close Application', close_application)
)

# Create icon
icon = pystray.Icon("my_tray_icon", create_image(64, 64, 'black', 'white'), "My Tray Icon", menu)

# Run the icon
icon.run()
