"""
Author      : Ethan Leone
Date        : 05/06/2023
Description : Generates an application for a Poker tournament clock
"""

# Import necessary packages
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import QCoreApplication, Qt
import time
import mainRoundsStorage as sets
import math
import os
import changeSettings


### Start Figure Window Code ###
class clockApplication(QMainWindow):                # Creates figure window object
    def __init__(self):                             # Names the figure window as "self"
        super().__init__()                                  # Gives figure window its properties
        self.screen = QDesktopWidget().screenGeometry()             # Find screen dimensions
        self.winSize = [self.screen.width(), self.screen.height()]   # Window dimensions
        self.setGeometry(0, 0, self.winSize[0], self.winSize[1])      # Set figure dimensions to screen size
        self.setWindowTitle("Poker Clock")                          # Create figure window name
        
        file_path = os.path.abspath(__file__)                       # Get the absolute path of the current file
        dir_path = os.path.dirname(file_path)                       # Get the directory containing the current file
        image_path = os.path.join(dir_path, "pokerIcon.jpg")        # Construct the full path to the image file using the current folder name
        self.setWindowIcon(QIcon(image_path))

        ##### Start Main Code #####

        self.valid = 0                  # Loop condition for clock
        self.remTime = 60               # Time remaining in current round
        self.currentRound = 0           # Set current round

        self.guiColors = "border: 2px dashed red; background-color: #a6a6a6"

        alpha = time.time()
        self.createLabels()             # Create time and round displays
        self.createPushButtons()        # Create the push buttons
        self.nextRound()                # Set displays to first round
        delta = time.time()
        print(delta-alpha)


    #####  End main code  #####
    ##### Start functions #####


    def showTime(self, seconds):

        if seconds <= 0 and ("/" in self.roundLabel.text()):       # If time is up
            self.timeClock.setText("0:00")
            self.valid = 0
            self.playPauseButton.setText("⏵")
            self.remTime = 0
        else:
            minsLeft = math.floor(seconds / 60)  # Calculate remaining whole minutes
            secLeft = seconds - minsLeft * 60  # Calculate remaining seconds
            if secLeft < 10:                        # If seconds has only 1 digit
                secLeft = "0" + str(secLeft)            # Give leading zero
            else:
                secLeft = str(secLeft)                  # Change num2str
            self.timeClock.setText(str(minsLeft)+":"+secLeft)   # Set timeClock display
        QCoreApplication.processEvents()

        if self.remTime < 1:
            self.nextSecButton.setEnabled(False)
        if self.remTime > 0:
            self.nextSecButton.setEnabled(True)
        if self.remTime < 60:
            self.nextMinButton.setEnabled(False)
        if self.remTime > 59:
            self.nextMinButton.setEnabled(True)

    def mainLoop(self):
        startingRound = self.roundLabel.text()
        while self.valid:    # While the loop condition is true
            start = time.time()     # Find time at start of iteration
            while time.time() < start + 1:       # Run nested-loop for one second
                QCoreApplication.processEvents()         # As a delay, update all boxes
            if self.valid:          # Ensure loop condition still true
                self.nextSec()           # Update time
        # if self.roundLabel.text() == startingRound:

    def changeRound(self):
        self.changeChipValues()                 # Change chips
        self.valid = 0

        ## Change main round details
        if sets.rounds[self.currentRound][0] == "Round":    # If this round is a blind
            self.roundLabel.setText(sets.rounds[self.currentRound][1])
            self.remTime = round(sets.minPerRnd * 60)  # Reset time
            self.showTime(self.remTime)  # Display new time
            self.timeClock.setFont(QFont("Arial", 175))
            self.backSecButton.setEnabled(True)
            self.backMinButton.setEnabled(True)
        # elif sets.rounds[self.currentRound][0] == "Color-Up":    # If this round is a color-up
        else:
            self.roundLabel.setText(sets.rounds[self.currentRound][0])
            self.remTime = 0
            self.timeClock.setText(sets.rounds[self.currentRound][1])
            self.timeClock.setFont(QFont("Arial", 125))
            self.backSecButton.setEnabled(False)
            self.backMinButton.setEnabled(False)


        if self.currentRound == len(sets.rounds):     # If last round is over
            pass
        elif self.currentRound == len(sets.rounds)-1:     # If last round
            self.nextRoundButton.setEnabled(False)       # Disable nextRound
            self.nextRoundLabel.setText("FINAL ROUND")  # Change next round details
        else:
            self.nextRoundLabel.setText("NEXT: " + sets.rounds[self.currentRound + 1][1])  # Change next round details
        if self.currentRound == 2:  # To enable backRound
            self.backRoundButton.setEnabled(True)
        self.playPauseButton.setText("⏵")

    def createPushButtons(self):    # Function to create all push button objects

        clockDim = [self.timeClock.x(), self.timeClock.y(), self.timeClock.width(), self.timeClock.height()]
        roundDim = [self.roundLabel.x(), self.roundLabel.y(), self.roundLabel.width(), self.roundLabel.height()]
        buttonFont = QFont("Arial", 20)


        ### Round change ###
        # create backRoundButton
        self.backRoundButton = QPushButton("<", self)           # Create push button object
        self.backRoundButton.setGeometry(roundDim[0]-100, roundDim[1]+25, 75, 75)      # Set dimensions for pushbutton
        self.backRoundButton.clicked.connect(self.backRound)    # Sets callback
        self.backRoundButton.setFont(buttonFont)                # Sets font

        self.nextRoundButton = QPushButton(">", self)           # Create nextRoundButton
        self.nextRoundButton.setGeometry(roundDim[0]-100, roundDim[1]+125, 75, 75)
        self.nextRoundButton.clicked.connect(self.nextRound)
        self.nextRoundButton.setFont(buttonFont)

        ### Second Change ###
        self.backSecButton = QPushButton("+", self)             # Create backSecondButton
        self.backSecButton.setGeometry(clockDim[0]+clockDim[2]+25, clockDim[1]+25, 75, 75)
        self.backSecButton.clicked.connect(self.backSec)
        self.backSecButton.setFont(buttonFont)

        self.nextSecButton = QPushButton("-", self)             # Create nextSecondButton
        self.nextSecButton.setGeometry(clockDim[0]+clockDim[2]+25, clockDim[1]+clockDim[3]-100, 75, 75)
        self.nextSecButton.clicked.connect(self.nextSec)
        self.nextSecButton.setFont(buttonFont)

        ### Minute Change ###
        self.backMinButton = QPushButton("+", self)             # Create backMinuteButton
        self.backMinButton.setGeometry(clockDim[0]-100, clockDim[1]+25, 75, 75)
        self.backMinButton.clicked.connect(self.backMin)
        self.backMinButton.setFont(buttonFont)
        # self.backSecButton.setStyleSheet("Border: 2px solid black; Background-Color: white")

        self.nextMinButton = QPushButton("-", self)             # Create nextMinuteButton
        self.nextMinButton.setGeometry(clockDim[0]-100, clockDim[1]+clockDim[3]-100, 75, 75)
        self.nextMinButton.clicked.connect(self.nextMin)
        self.nextMinButton.setFont(buttonFont)

        self.playPauseButton = QPushButton("⏵", self)           # Create playPauseButton
        self.playPauseButton.setGeometry(clockDim[0]+round(clockDim[2]/2)-50, clockDim[1]+clockDim[3]+25, 100, 100)
        self.playPauseButton.clicked.connect(self.playPause)
        self.playPauseButton.setFont(QFont("Arial", 25))

    def createLabels(self):

        self.timeClock = QLabel("TIME", self)                   # Create time clock
        self.timeClock.setGeometry(150, 400, 1000, 350)         # Set Position
        self.timeClock.setFont(QFont("Arial", 175))             # Set Font
        self.timeClock.setAlignment(Qt.AlignCenter)             # Set Alignment

        self.roundLabel = QLabel("SB/BB", self)                 # Create round display
        self.roundLabel.setGeometry(150, 25, 1000, 100)
        self.roundLabel.setFont(QFont("Arial", 50))
        self.roundLabel.setAlignment(Qt.AlignCenter)

        self.nextRoundLabel = QLabel("NEXT ROUND", self)        # Create next round display
        self.nextRoundLabel.setGeometry(150, 125, 1000, 100)
        self.nextRoundLabel.setFont(QFont("Arial", 40))
        self.nextRoundLabel.setAlignment(Qt.AlignCenter)
        nextPal = QPalette()                                    # Create color palette
        nextPal.setColor(QPalette.WindowText, Qt.darkGray)      # Create color value
        self.nextRoundLabel.setPalette(nextPal)                 # Set color value

        self.chipDisplay = QLabel("CHIP VALUES", self)          # Create chip value box
        self.chipDisplay.setGeometry(1300, 50, 500, 900)
        self.chipDisplay.setFont(QFont("Arial", 100))
        self.chipDisplay.setAlignment(Qt.AlignCenter)

        self.timeClock.setStyleSheet(self.guiColors)
        self.roundLabel.setStyleSheet(self.guiColors)
        self.nextRoundLabel.setStyleSheet(self.guiColors)
        self.chipDisplay.setStyleSheet(self.guiColors)

    def changeChipValues(self):
        roundLine = sets.rounds[self.currentRound]      # Round information
        lineLength = len(roundLine)                     # Amount of values in round info
        numChips = sum((roundLine[2:lineLength]))        # Amount of chip values to display
        # 4 - 100 # 3 - 150 # 2 - 125 # 1 - 100
        percent = 100 if numChips == 1 else 43*numChips**3 - 423.55*numChips**2 + 1324.4*numChips - 1173
        htmlText = ['<p style="line-height:'+str(round(percent, 2))+'%">']     # HTML Variable
        for i in range(lineLength-2):                   # For each possible chip value
            if roundLine[i+2]:                           # If chip at "i" will be displayed
                htmlText.append('<font color="'+sets.chips[0][i]+'">'+sets.chips[1][i])   # Create html for this line
        htmlText[0] = htmlText[0] + htmlText[1]         # Line spacing and first value
        del htmlText[1]                                 # Delete first number (included in first)
        htmlText = '<br>'.join(htmlText)                # Join with line break
        self.chipDisplay.setText(htmlText)              # Set display text



    #####   End Normal Functions   #####
    ##### Start Callback Functions #####


    def backRound(self):            # Define button callback
        self.currentRound = self.currentRound - 1   # Increase current round number
        self.changeRound()                          # Function to change round for gui

        if self.currentRound == 1:                      # If in first round
            self.backRoundButton.setEnabled(False)       # Disable backRound

        if self.currentRound == len(sets.rounds)-2:
            self.nextRoundButton.setEnabled(True)

    def nextRound(self):
        self.currentRound = self.currentRound + 1   # Increase current round number
        self.changeRound()  # Function to change round for gui

    def nextSec(self):                      # Define button callback
        self.remTime = self.remTime - 1     # Increment time
        self.showTime(self.remTime)         # Display new time

    def backSec(self):                      # Define button callback
        self.remTime = self.remTime + 1     # Increment time
        self.showTime(self.remTime)         # Display new time

    def nextMin(self):                      # Define button callback
        self.remTime = self.remTime - 60    # Increment time
        self.showTime(self.remTime)         # Display new time

    def backMin(self):                      # Define button callback
        self.remTime = self.remTime + 60    # Increment time
        self.showTime(self.remTime)         # Display new time

    def playPause(self):
        if self.playPauseButton.text() == "⏵":   # If button was play
            if not((self.currentRound+1 == len(sets.rounds)) & (self.remTime == 0)):    # Effectively locks last round
                if self.remTime == 0:                           # If the round was over
                    self.nextRound()                                # Go to next round
                if self.remTime != 0:  # If time has been added for a round
                    self.valid = 1  # Validate loop
                    self.playPauseButton.setText("▐▐")  # Change button
                    self.mainLoop()  # Tick the clock
                else:  # If still no time
                    self.playPauseButton.setText("⏵")  # Change button back

        elif self.playPauseButton.text() == "▐▐":
            self.valid = 0
            self.playPauseButton.setText("⏵")

    ##### End callback functions #####
### End Figure window code ###


if __name__ == '__main__':          # If statement locks the foloowing code to this script file, rather than being called somewhere else
    app = QApplication(sys.argv)    #
    window = clockApplication()
    window.show()
    sys.exit(app.exec_())
