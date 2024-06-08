import os
import shutil
import glob
from dotenv import load_dotenv
import time

load_dotenv()

# env variables
outputfolder = os.getenv('OUTPUT_FOLDER')
documentsgamefolder = os.getenv('DOCUMENTS_GAME_FOLDER')

"""
ISSUES 
if a new autosave were to arrive during the procces it would break the ting
deoenst work if we dont have a starting save
if you change country the id seems to change
"""
class Save:
    def __init__(self, name, edited, saveid):
        self.name = name
        self.edited = edited
        self.id = saveid
        self.gameid = saveid[-8:] if saveid else None

    @staticmethod
    def getid(savelocation):
        max_retries = 5  # Number of retries
        initial_wait = 1  # Initial wait time in seconds

        for attempt in range(max_retries):
            try:
                with open(savelocation, "rb") as file:
                    id_bytes = file.read(23)
                    return id_bytes
            except PermissionError as e:
                wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                print(f"Attempt {attempt+1}: Permission denied: {savelocation} | Error: {e}. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
            except Exception as e:
                print(f"Error opening file: {e}")
                return None
        return None

    def display(self):
        print(f"Save Name: {self.name}")
        print(f"Save Edited: {self.edited}")

def Scaner(documentsgamefolder, lastsave, outputfolder):
    savegamesfolder = os.path.join(documentsgamefolder, "save games")
    autosave_files = glob.glob(os.path.join(savegamesfolder, "autosave.v3")) + \
                     glob.glob(os.path.join(savegamesfolder, "autosave_exit.v3"))
    if not autosave_files:
        print("No autosave files found.")
        return

    last_edited_file = max(autosave_files, key=os.path.getmtime)
    file_name = os.path.basename(last_edited_file)
    last_edited_timestamp = os.path.getmtime(last_edited_file)
    NewSave = Save(name=file_name, edited=last_edited_timestamp, saveid=Save.getid(last_edited_file))

    if NewSave.id and NewSave.edited > lastsave.edited and NewSave.gameid == lastsave.gameid and NewSave.id != lastsave.id:
        source = os.path.join(savegamesfolder, NewSave.name)
        destination = os.path.join(outputfolder, f"{NewSave.name}-{NewSave.edited}")
        shutil.copy(source, destination)
        print("Save successfully moved")
    else:
        print("Save not from correct campaign or save already in folder")

running = True
while running:
    files = glob.glob(os.path.join(outputfolder, "*"))
    if not files:
        print("No save files found in the save folder")
        time.sleep(10)  # Wait for 10 seconds before retrying
        continue

    last_edited_file = max(files, key=os.path.getmtime)
    file_name = os.path.basename(last_edited_file)
    oldsavelocation = os.path.join(outputfolder, file_name)
    last_edited_timestamp = os.path.getmtime(last_edited_file)
    lastsave = Save(name=file_name, edited=last_edited_timestamp, saveid=Save.getid(oldsavelocation))

    Scaner(documentsgamefolder, lastsave, outputfolder)
    time.sleep(5)  # Wait for 10 seconds before scanning again