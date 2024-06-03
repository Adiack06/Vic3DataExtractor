import os
import shutil
import glob

"""
ISSUES 
doesnt check saves have same game id? = 00000275 so the last 8 digits of the first line 
doesnt check if there is already a save with the same id
if a new autosave were to arrive during the procces it would break the ting
deoest work if we dont have a starting save
"""
class Save:
    def __init__(self, name, edited, saveid):
        self.name = name
        self.edited = edited
        self.id = saveid
        self.gameid = saveid[-8:]

    @staticmethod
    def getid(savelocation):
        with open(savelocation, "rb") as file:  # Open the file in binary mode
            id_bytes = file.read(23)  # Read the first 23 bytes
            return id_bytes
    def display(self):
        print(f"Save Name: {self.name}")
        print(f"Save Edited: {self.edited}")


def Scaner(documentsgamefolder, lastsave, outputfolder):
    savegamesfolder = os.path.join(documentsgamefolder, "save games")
    if glob.glob(os.path.join(savegamesfolder, "autosave.v3")):
        files = glob.glob(os.path.join(savegamesfolder, "autosave.v3"))
        savelocation = os.path.join(savegamesfolder, "autosave.v3")
    elif glob.glob(os.path.join(savegamesfolder, "autosave_exit.v3")):
        files = glob.glob(os.path.join(savegamesfolder, "autosave_exit.v3"))
        savelocation = os.path.join(savegamesfolder, "autosave_exit.v3")
    else:
        return

    last_edited_file = max(files, key=os.path.getmtime)
    file_name = os.path.basename(last_edited_file)
    last_edited_timestamp = os.path.getmtime(last_edited_file)
    NewSave = Save(name=file_name, edited=last_edited_timestamp, saveid=Save.getid(savelocation))

    if NewSave.edited > lastsave.edited and NewSave.gameid == lastsave.gameid and NewSave.id != lastsave.id:
        source = os.path.join(savegamesfolder, NewSave.name)
        destination = os.path.join(outputfolder, f"{NewSave.name}-{NewSave.edited}")
        shutil.copy(source, destination)
    else:
        print("save not from correct campaign or save already in folder")
running = True
while running is True:
    outputfolder= r""
    files = glob.glob(os.path.join(fr"{outputfolder}", "*"))

    if not files:
        raise FileNotFoundError("No save files found in the save folder")
    last_edited_file = max(files, key=os.path.getmtime)
    file_name = os.path.basename(last_edited_file)
    oldsavelocation= os.path.join(outputfolder,file_name)
    last_edited_timestamp = os.path.getmtime(last_edited_file)
    lastsave = Save(name=file_name, edited=last_edited_timestamp, saveid=Save.getid(oldsavelocation))


    Scaner(r"",lastsave,outputfolder)