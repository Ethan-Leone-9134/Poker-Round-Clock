# From ChatGPT

import sys
import time

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QPushButton, QLabel, QTextEdit, \
     QCheckBox, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QScrollArea, QWidget, QComboBox
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import QCoreApplication, Qt
import mainRoundsStorage as sets


class MyWindow(QMainWindow):    # Creates figure window object
    def __init__(self):         # Names the figure window as "self"
        super().__init__()      # Gives figure window its properties
        self.screen = QDesktopWidget().screenGeometry()             # Find screen dimensions
        self.screen = [self.screen.width(), self.screen.height()]   # Window dimensions
        self.setGeometry(0, 0, self.screen[0], self.screen[1])      # Set figure dimensions to screen size
        self.setWindowTitle("Poker Clock")                          # Create figure window name
        self.setWindowIcon(QIcon(r"C:\Users\zaper\Downloads\pokerIcon.jpg"))

        ### Start Main Code ###

        # create push button
        self.button = QPushButton("Click me!", self)        # Create push button object
        self.button.setGeometry(100, 525, 200, 50)          # Set dimensions for pushbutton
        self.button.clicked.connect(self.closeShop)   # Sets callback



        self.topBoxes()
        self.timeBoxes()
        self.roundBoxes()


        ### End Main Code ###

    def closeShop(self):      # Define button callback
        with open('roundTest.py', 'r') as file:
            lines = file.readlines()
        print(lines)
        file.close()

        # Get color names
        colors = []
        for box in self.colorBoxes:
            colors.append(box.toPlainText())
        colors = '", "'.join(colors)
        # print(colors)

        # Get color values
        values = []
        for box in self.numBoxes:
            values.append(box.toPlainText())
        values = ',   '.join(values)
        # print(colors)
        print('chips = [["'+colors+'"],')
        print('         ['+values+']]')

        # Get color quantity

        # Get time
        print('minPerRnd = '+self.minBox.text())

        # Get rounds
        print('rounds = [')
        with self.roundBoxCollection[3] as currLine:
            print(1)
            for i in range(5):
                print(2)
                print(currLine.text())
                with currLine[0] as currBox:
                    print(currBox.text())

        print()

    def topBoxes(self):
        self.colorBoxes = []      # Boxes that contain chip colors
        self.numBoxes = []        # Boxes that contain ship values
        mainLay = QHBoxLayout()

        for i in range(len(sets.chips[0])):
            tempLayout = QVBoxLayout()                          # Initialize layout
            frame = QFrame(self)                                # Generate Frame
            frame.setFrameShape(QFrame.Box)                     # Set Frame Shape
            frame.setLineWidth(2)                               # Set border width
            # frame.setStyleSheet("background-color: "+sets.chips[0][i])        # Set background color
            frame.setStyleSheet("background-color: red")        # Set background color

            tempBut = QTextEdit(sets.chips[0][i], frame)        # Create color box
            tempBut.setAlignment(Qt.AlignCenter)                # Center align color
            self.colorBoxes.append(tempBut)                     # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            tempBut = QTextEdit(str(sets.chips[1][i]), frame)   # Create value box
            tempBut.setAlignment(Qt.AlignCenter)                # Center align values
            self.numBoxes.append(tempBut)                       # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            tempBut = QTextEdit(str(sets.chips[2][i]), frame)   # Create quantity box
            tempBut.setAlignment(Qt.AlignCenter)                # Center align values
            # self.numBoxes.append(tempBut)                       # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            tempBut = QLabel(frame)                             # Create value box
            chipSum = str(getNumber(sets.chips[1][i]) * sets.chips[2][i])  # Find value of total
            tempBut.setText(chipSum)                            # Set label to sum
            tempBut.setAlignment(Qt.AlignCenter)                # Center align values
            # self.numBoxes.append(tempBut)                       # Add box to collecting variable
            tempLayout.addWidget(tempBut)                       # Add box to layout/frame

            frame.setLayout(tempLayout)                         # Add layout to frame
            frame.setMaximumHeight(200)
            # frame.setMaximumWidth(100)
            # frame.setGeometry(i*125+25, 25, 100, 200)           # Add dimensions to frame
            mainLay.addWidget(frame)

        scroll = QScrollArea(self)                      # Create scroll area
        scroll.setWidgetResizable(True)
        widget = QWidget()
        widget.setLayout(mainLay)
        scroll.setWidget(widget)
        scroll.setGeometry(100, 50, 650, 260)
        # self.setLayout(mainLay)


    def timeBoxes(self):

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

    def roundDropDown(self):
        mainTypeDropDown = QComboBox()
        mainTypeDropDown.addItem("Round")
        mainTypeDropDown.addItem("Color-Up")
        mainTypeDropDown.addItem("Unlock")
        mainTypeDropDown.addItem("Break")
        return mainTypeDropDown


    def roundBoxes(self):
        self.roundBoxCollection = []                                # Initialize round data holder
        vBox = QVBoxLayout()                                        # Initialize line box layout

            ####### Create a chip trade in calculator

        for r in range(len(sets.rounds)-1):                         # For each line
            r = r + 1                                                   # Ignore first line
            hBox = QHBoxLayout()                                        # Initialize line
            tempBut = self.roundDropDown()                                  # Round Type Box
            tempBut.setCurrentIndex(0)
            self.roundBoxCollection.append(tempBut)                     # Add to variable
            hBox.addWidget(tempBut)                                     # Add to line

            tempBut = QLineEdit(str(sets.rounds[r][1]), self)         # Round Value Box
            tempBut.setMaximumWidth(125)
            tempBut.setAlignment(Qt.AlignCenter)
            self.roundBoxCollection.append(tempBut)                     # Add to variable
            hBox.addWidget(tempBut)                                     # Add to line

            for c in range(len(sets.rounds[0])-2):                      # For each value of chips
                tempBut = QCheckBox(str(sets.chips[1][c]), self)            # Create checkbox
                tempBut.setChecked(sets.rounds[r][c + 2])                   # Set check value
                self.roundBoxCollection.append(tempBut)                     # Add to variable
                hBox.addWidget(tempBut)                                     # Add to line

            vBox.addLayout(hBox)                                        # Add line to the rest

        scroll = QScrollArea(self)                      # Create scroll area
        scroll.setWidgetResizable(True)
        widget = QWidget()
        widget.setLayout(vBox)
        scroll.setWidget(widget)
        scroll.setGeometry(800, 50, 1000, 900)

    # def closeShop(self):

def getNumber(numText):
    numText.replace("B", "MK")
    numText.replace("b", "MK")
    numText.replace("M", "KK")
    numText.replace("m", "KK")
    numText.replace("k", "K")
    numComma = numText.count("K")
    sigNum = int(numText.replace("K", ""))
    result = sigNum * 1000 ** numComma
    return result





if __name__ == '__main__':          # If statement locks the following code to this script file
    alpha = time.time()
    app = QApplication(sys.argv)    #
    window = MyWindow()
    window.show()
    print("Completed in {} secs".format(round(time.time()-alpha, 4)))
    sys.exit(app.exec_())
