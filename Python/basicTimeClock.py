# Import necessary packages
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
import time
import math

### Start Figure Window Code ###
class MyWindow(QMainWindow):    # Creates figure window object
    def __init__(self):         # Names the figure window as "self"
        super().__init__()      # Gives figure window its properties
        screen = QDesktopWidget().screenGeometry()    # Find screen dimensions
        self.setGeometry(0, 0, screen.width(), screen.height())     # Set figure dimensions to screen size
        # self.showMaximized()
        # set window name and size
        self.setWindowTitle("Poker Clock")          # Create figure window name

        ##### Start Main Code #####

        self.valid = 1               # Loop condition for clock
        self.remTime = 20*60         # Time remaining in current round
        self.roundMinutes = 20       # Minutes per round

        self.createPushButtons()    # Create the push buttons

        # create timeClock
        self.timeClock = QLabel("", self)
        self.showTime(self.remTime)
        self.timeClock.setGeometry(200, 100, 200, 200)
        self.timeClock.setFont(QFont("Arial", 12))

    #####  End main code  #####
    ##### Start functions #####


    def showTime(self, seconds):
        minsLeft = math.floor(seconds/60)       # Calculate remaining whole minutes
        secLeft = seconds - minsLeft*60         # Calculate remaining seconds
        if seconds <= 0:                        # If time is up
            self.nextRound()                        # End current round
        if secLeft < 10:                        # If seconds has only 1 digit
            secLeft = "0" + str(secLeft)            # Give leading zero
        else:
            secLeft = str(secLeft)
        self.timeClock.setText(str(minsLeft)+":"+secLeft)
        QCoreApplication.processEvents()

    def mainLoop(self):
        while self.valid:    # While the loop condition is true
            start = time.time()     # Find time at start of iteration
            while time.time() < start + 1:       # Run nested-loop for one second
                QCoreApplication.processEvents()         # As a delay, update all boxes
            if self.valid:          # Ensure loop condition still true
                self.nextSec()           # Update time
            print(self.remTime)
            print(self.valid)

    def createPushButtons(self):    # Function to create all push button objects

        ### Round change ###
        # create backRoundButton
        self.backRoundButton = QPushButton("<", self)           # Create push button object
        self.backRoundButton.setGeometry(100, 100, 50, 50)      # Set dimensions for pushbutton
        self.backRoundButton.clicked.connect(self.backRound)    # Sets callback

        # create nextRoundButton
        self.nextRoundButton = QPushButton(">", self)           # Create push button object
        self.nextRoundButton.setGeometry(100, 200, 50, 50)      # Set dimensions for pushbutton
        self.nextRoundButton.clicked.connect(self.nextRound)    # Sets callback

        ### Second Change ###
        # create backSecondButton
        self.backSecButton = QPushButton("+", self)             # Create push button object
        self.backSecButton.setGeometry(100, 300, 50, 50)        # Set dimensions for pushbutton
        self.backSecButton.clicked.connect(self.backSec)        # Sets callback

        # create nextSecondButton
        self.nextSecButton = QPushButton("-", self)             # Create push button object
        self.nextSecButton.setGeometry(100, 400, 50, 50)        # Set dimensions for pushbutton
        self.nextSecButton.clicked.connect(self.nextSec)        # Sets callback

        ### Minute Change ###
        # create backMinuteButton
        self.backSecButton = QPushButton("+", self)             # Create push button object
        self.backSecButton.setGeometry(300, 300, 50, 50)        # Set dimensions for pushbutton
        self.backSecButton.clicked.connect(self.backMin)        # Sets callback

        # create nextMinuteButton
        self.nextSecButton = QPushButton("-", self)             # Create push button object
        self.nextSecButton.setGeometry(300, 400, 50, 50)        # Set dimensions for pushbutton
        self.nextSecButton.clicked.connect(self.nextMin)        # Sets callback

        # create playPauseButton
        self.playPauseButton = QPushButton("⏵", self)           # Create push button
        self.playPauseButton.setGeometry(200, 400, 50, 50)      # Set dimensions for pushbutton
        self.playPauseButton.clicked.connect(self.playPause)    # Sets callback

    #####   End Normal Functions   #####
    ##### Start Callback Functions #####

    def backRound(self):            # Define button callback
        print("Back 1 Round")       # Say that the button was clicked
        self.timeClock.setText("Reverse")

    def nextRound(self):
        print("Next 1 Round")
        self.timeClock.setText("Forward")

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
        if self.playPauseButton.text() == "⏵":
            self.playPauseButton.setText("▐▐")
            self.mainLoop()
        elif self.playPauseButton.text() == "▐▐":
            self.valid = 0
            self.playPauseButton.setText("⏵")

    ##### End callback functions #####
### End Figure window code ###


if __name__ == '__main__':          # If statement locks the foloowing code to this script file, rather than being called somewhere else
    app = QApplication(sys.argv)    #
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
