"""
Author      : Ethan Leone
Date        : 12/27/2023
Description : Opens the "current.py" file to produce the reference to the appropriate file
"""

import os 
import importlib

def getPath(fileName: str) -> str:
    file_path = os.path.abspath(__file__)                       # Get the absolute path of the current file
    dir_path = os.path.dirname(file_path)                       # Get the directory containing the current file
    image_path = os.path.join(dir_path, fileName)        # Construct the full path to the image file using the current folder name
    return image_path

with open(getPath('roundFiles\current.txt'), 'r') as file:
    # file.write()
    lines = file.readlines()
file.close()
currentSave = 'rounds'+lines[0]
currentMod = importlib.import_module(f"roundFiles.{currentSave}")