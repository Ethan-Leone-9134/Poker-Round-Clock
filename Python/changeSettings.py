"""
Author      : Ethan Leone
Date        : 05/06/2023
Description : Generates an application for a Poker tournament clock settings window
"""

import sys
import time
import os

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QPushButton, QLabel, QTextEdit, \
     QCheckBox, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QScrollArea, QWidget, QComboBox
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import QCoreApplication, Qt
import mainRoundsStorage as sets


class settingsWindow(QMainWindow):                # Creates figure window object
    def __init__(self):                             # Names the figure window as "self"
        super().__init__()                                  # Gives figure window its properties
        self.screen = QDesktopWidget().screenGeometry()                 # Find screen dimensions
        self.winSize = [self.screen.width(), self.screen.height()]      # Window dimensions
        self.setGeometry(0, 0, self.winSize[0], self.winSize[1])        # Set figure dimensions to screen size
        self.setWindowTitle("Poker Clock")                              # Create figure window name
        self.setWindowIcon(QIcon(getPath("pokerIcon.jpg")))             # Set window icon

        self.topBoxes()         # Generate the chip boxes
        self.timeSaveBoxes()    # Generate the time ans save boxes
        self.roundBoxes()       # Generate the rounds grid


    def closeShop(self):      # Define button callback
        with open(getPath('mainRoundsStorage.py'), 'r') as file:
            # file.write()
            lines = file.readlines()
        file.close()

        # Get color names
        colors = []
        for box in self.colorBoxes:
            colors.append(box.toPlainText())
        colors = '", "'.join(colors)

        # Get color values
        values = []
        for box in self.numBoxes:
            values.append('"' + box.toPlainText() + '"')
        values = ',   '.join(values)

        # Get color quantity
        # Get color values
        quantities = []
        for box in self.quantityBoxes:
            quantities.append('"' + box.toPlainText() + '"')
        quantities = ',   '.join(quantities)

        # Get time
        roundTime = self.minBox.text()
        
        # Get rounds
        roundText = 'rounds = ['

        for currLine in self.roundBoxCollection:
            roundText += '["' + (currLine[0].currentText()) + '", '
            roundText += '"' + (currLine[1].text()) +'"'
            for i in range(len(currLine)-2):
                i = i + 2
                roundText += ',  ' + str(int(currLine[i].isChecked()))
            roundText += "], \n          "
        roundText += ']'

        with open(getPath('mainRoundsStorage.py'), 'w') as file:
            file.write('chips = [["'+colors+'"],\n')
            file.write('         ['+values+'],\n')
            file.write('         ['+quantities+']]\n')
            # file.write('         [20,   20,    10,    5, 0, 0]]\n')
            file.write('minPerRnd = ' + roundTime + '\n')
            file.write(roundText)
            file.close()

        self.close()


    def topBoxes(self):
        self.colorBoxes = []      # Boxes that contain chip colors
        self.numBoxes = []        # Boxes that contain ship values
        self.quantityBoxes = []   # Boxes that contain quantity values
        mainLay = QHBoxLayout()

        for i in range(len(sets.chips[0])):
            tempLayout = QVBoxLayout()                          # Initialize layout
            frame = QFrame(self)                                # Generate Frame
            frame.setFrameShape(QFrame.Box)                     # Set Frame Shape
            frame.setLineWidth(2)                               # Set border width

            currColor = sets.chips[0][i]                        # Find the background color
            fontColor = backCheck(currColor)                    # Find the font color
            frame.setStyleSheet("background-color: "+currColor
                                +"; color: "+fontColor)         # Set background color
            
            tempBut = QTextEdit(currColor, frame)               # Create color box
            tempBut.setAlignment(Qt.AlignCenter)                # Center align color
            tempBut.setFont(QFont("Arial", 11))                 # Set font
            self.colorBoxes.append(tempBut)                     # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            tempBut = QTextEdit(str(sets.chips[1][i]), frame)   # Create value box
            tempBut.setAlignment(Qt.AlignCenter)                # Center align values
            tempBut.setFont(QFont("Arial", 11))                 # Set font
            self.numBoxes.append(tempBut)                       # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            tempBut = QTextEdit(str(sets.chips[2][i]), frame)   # Create quantity box
            tempBut.setAlignment(Qt.AlignCenter)                # Center align values
            tempBut.setFont(QFont("Arial", 11))                 # Set font
            self.quantityBoxes.append(tempBut)                  # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            tempBut = QLabel(frame)                             # Create value box
            chipSum = str(getNumber(sets.chips[1][i]) * getNumber(sets.chips[2][i]))  # Find value of total
            tempBut.setText(chipSum)                            # Set label to sum
            tempBut.setAlignment(Qt.AlignCenter)                # Center align values
            tempBut.setFont(QFont("Arial", 11))                 # Set font
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            frame.setLayout(tempLayout)                         # Add layout to frame
            frame.setMaximumHeight(200)
            # frame.setMaximumWidth(100)
            mainLay.addWidget(frame)

        scroll = QScrollArea(self)                      # Create scroll area
        scroll.setWidgetResizable(True)
        widget = QWidget()
        widget.setLayout(mainLay)
        scroll.setWidget(widget)
        scroll.setGeometry(100, 50, 650, 260)


    def timeSaveBoxes(self):

        frame = QFrame(self)                                # Generate Frame
        frame.setFrameShape(QFrame.Box)                     # Set Frame Shape
        frame.setLineWidth(2)                               # Set border width
        frame.setStyleSheet("background-color: cyan")       # Set background color

        minLabel = QLabel("Minutes Per Round: ", frame)     # Generate label
        minLabel.setFont(QFont("Arial", 10))                # Format label font

        self.minBox = QLineEdit(frame)                      # Generate Input Box
        self.minBox.setText(str(round(sets.minPerRnd, 2)))  # Set the important text
        self.minBox.setFont(QFont("Arial", 12))             # Set font
        self.minBox.setStyleSheet('background-color:white') # Set background color
        self.minBox.setMinimumHeight(40)                    # Add height
        self.minBox.setMaximumWidth(80)                     # Add width
        self.minBox.setAlignment(Qt.AlignCenter)            # Center Text Position

        frame_layout = QHBoxLayout()                        # Generate layout
        frame_layout.addWidget(minLabel)                    # Add label to layout
        frame_layout.addWidget(self.minBox)                 # Add input box to layout
        frame.setLayout(frame_layout)                       # Add layout to the frame
        frame.setGeometry(200, 400, 300, 75)                # Set the geometry of the frame

        # Set the main window layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        self.saveButton = QPushButton("Save and Return!", self)     # Create save button object
        self.saveButton.setGeometry(150, 525, 200, 50)              # Set dimensions for pushbutton
        self.saveButton.clicked.connect(self.closeShop)             # Sets callback


    def roundBoxes(self):
        self.roundBoxCollection = collection()                      # Initialize round data holder
        vBox = QVBoxLayout()                                        # Initialize line box layout

            ####### Create a chip trade-in calculator

        for r in range(len(sets.rounds)):                         # For each line
            hBox = QHBoxLayout()                                        # Initialize line
            tempBut = self.roundDropDown(sets.rounds[r][0])                  # Round Type Box
            self.roundBoxCollection.set(r, 0, tempBut)                     # Add to variable
            hBox.addWidget(tempBut)                                     # Add to line

            tempBut = QLineEdit(str(sets.rounds[r][1]), self)         # Round Value Box
            tempBut.setMaximumWidth(125)
            tempBut.setAlignment(Qt.AlignCenter)
            self.roundBoxCollection.set(r, 1, tempBut)                     # Add to variable
            hBox.addWidget(tempBut)                                     # Add to line

            for c in range(len(sets.rounds[0])-2):                      # For each value of chips
                tempBut = QCheckBox(str(sets.chips[1][c]), self)            # Create checkbox
                tempBut.setChecked(sets.rounds[r][c + 2])                   # Set check value
                self.roundBoxCollection.set(r, c + 2, tempBut)                     # Add to variable
                hBox.addWidget(tempBut)                                     # Add to line

            vBox.addLayout(hBox)                                        # Add line to the rest

        scroll = QScrollArea(self)                      # Create scroll area
        scroll.setWidgetResizable(True)
        widget = QWidget()
        widget.setLayout(vBox)
        scroll.setWidget(widget)
        scroll.setGeometry(800, 50, 1000, 900)


    def roundDropDown(self, name):
        mainTypeDropDown = QComboBox()
        mainTypeDropDown.addItem("Round")
        mainTypeDropDown.addItem("Color-Up")
        mainTypeDropDown.addItem("Unlock")
        mainTypeDropDown.addItem("Break")
        
        if name == "Round":
            mainTypeDropDown.setCurrentIndex(0)
        elif name == "Color-Up":
            mainTypeDropDown.setCurrentIndex(1)
        elif name == "Unlock":
            mainTypeDropDown.setCurrentIndex(2)
        elif name == "Break":
            mainTypeDropDown.setCurrentIndex(3)
        
        return mainTypeDropDown



def backCheck(backColor: str) -> str:
    color = QColor(backColor)
    triple = ((color.red(), color.green(), color.blue()))
    if ((triple[0]*0.299 + triple[1]*0.587 + triple[1]*0.114) > 186): # Code taken from https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        fontColor = "black"
    else:
        fontColor = "white"
    return fontColor
    

def getNumber(numText: str) -> float: 
    numText.replace("B", "MK")
    numText.replace("b", "MK")
    numText.replace("M", "KK")
    numText.replace("m", "KK")
    numText.replace("k", "K")
    numComma = numText.count("K")
    sigNum = int(numText.replace("K", ""))
    result = sigNum * 1000 ** numComma
    return result


def getPath(fileName: str) -> str:
    file_path = os.path.abspath(__file__)                       # Get the absolute path of the current file
    dir_path = os.path.dirname(file_path)                       # Get the directory containing the current file
    image_path = os.path.join(dir_path, fileName)        # Construct the full path to the image file using the current folder name
    return image_path


class collection(list):
    def set(self, row, col, value):             # ChatGPT generated
        if row >= len(self):
            self.extend([[] for _ in range(row - len(self) + 1)])
        if col >= len(self[row]):
            self[row].extend([None for _ in range(col - len(self[row]) + 1)])
        self[row][col] = value
    


if __name__ == '__main__':          # If statement locks the following code to this script file
    alpha = time.time()
    app = QApplication(sys.argv)
    window = settingsWindow()
    window.show()
    print("Completed in {} secs".format(round(time.time()-alpha, 4)))
    sys.exit(app.exec_())
