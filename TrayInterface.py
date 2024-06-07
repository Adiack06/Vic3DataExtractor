from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

def create_image():
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (0, 0, 63, 63),
        fill=(255, 0, 0))
    return image

def close_application(icon, item):
    icon.stop()
    pass

def start_scanner(icon, item):
    pass

def select_starting_save(icon, item):
    pass

def working(icon, item):

    pass

def settings(icon, item):
    pass

icon = pystray.Icon("V3Extractor", create_image(), "Test Tray", menu=pystray.Menu(
    item("Close Application", close_application),
    item("Start Scanner", start_scanner),
    item("Select Starting Save", select_starting_save),
    item("Working?", working),
    item("Settings", settings)
))

icon.run()
