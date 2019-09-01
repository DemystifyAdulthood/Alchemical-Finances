# This program determines the Message the user gets upon logging into the program. Essentially a welcome message.

import sys
import sqlite3

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap
from WelcomeMessageUi import Ui_Dialog
from pathlib import Path
from UPK import account_pathway
from StyleSheets import UniversalStyleSheet, welcomeStylesheet


class Message(QDialog):

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, messageCount, user):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.userCount = messageCount
        self.refUser = user
        self.dbPathway = account_pathway("UAInformation.db")
        self.dbPathway = Path.cwd() / self.dbPathway[0]
        self.show()
        self.ui.pushButtonClose.clicked.connect(self.close_message)
        self.disp_welcome()
        self.ui.pushButtonNext.clicked.connect(self.disp_welcome)
        self.setStyleSheet(UniversalStyleSheet)
        self.ui.frame.setStyleSheet(welcomeStylesheet)

        titleFont = QtGui.QFont()
        titleFont.setPointSize(18)
        titleFont.setWeight(75)

        messageFont = QtGui.QFont()
        messageFont.setPointSize(12)
        messageFont.setWeight(50)

        reminderFont = QtGui.QFont()
        reminderFont.setPointSize(12)
        reminderFont.setWeight(75)

        signitureFont = QtGui.QFont()
        signitureFont.setPointSize(14)
        signitureFont.setItalic(True)
        signitureFont.setWeight(50)

        self.ui.labelWelcome.setFont(titleFont)
        self.ui.labelMessage.setFont(messageFont)
        self.ui.labelReminder.setFont(reminderFont)
        self.ui.labelSigniture.setFont(signitureFont)
    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ The core function - Display message                                                                  ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    def disp_welcome(self):
        if self.userCount == 0:
            self.ui.labelMessage.setText("""Welcome """ + self.refUser.capitalize() + """,

I am glad you have chosen to give my first major Python project a whirl. It has been a nerdy financial passion project and one I hope to continue to grow and build with your help.

Please let me know if things need to be tweaked or just not intuitive. If you are confused or unsure, please check the help tab for additional notes and upcoming features.

As this is your first time logging into this program be sure to save your password somewhere. As currently there is no recovery system in place. 
""")
            self.ui.labelReminder.setText("""
  ** Please be patient upon closing this window,  
       as creating your account will take a moment. **
""")
            self.ui.labelSigniture.setText("")
            self.ui.labelLogo.setText("")
            self.refresh_count(self.refUser)

        elif self.userCount == 1:
            self.ui.labelWelcome.setText("Welcome Back " + self.refUser.capitalize())
            self.ui.labelMessage.setText("""          
Thank you for continuing to use this program as your financial ledger. Feedback is always welcome and will help me continue to improve the system.

As a solo programmer I can not promise updates or new features to appear quickly. Just keep an eye out as I will try to provide information when available.
""")
            self.ui.labelReminder.setText("")
            self.ui.labelSigniture.setText("""
Your Grateful Programmer,
Mystified Adult
Contact@demystifyAdulthood.com       
""")
            logoImage = QPixmap('AF Logo.png')
            logoAdjustment = logoImage.scaled(90, 90, 1, 1)
            self.ui.labelLogo.setPixmap(logoAdjustment)
            self.ui.pushButtonNext.hide()
        else:
            pass

    def close_message(self):
        self.accept()

    # --- Replaced native close event. This allowed me to transition from between objects smoothly ---------------------
    def closeEvent(self, event):
        event.ignore()
        self.accept()

    # --- User Messages-------------------------------------------------------------------------------------------------
    def refresh_count(self, user):
        messageStatement = "SELECT Message FROM Users WHERE Profile= '" + user + "'"
        conn = sqlite3.connect(self.dbPathway)
        cur = conn.cursor()
        cur.execute(messageStatement)
        row = cur.fetchone()
        self.userCount = row[0]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = "lily"
    molly = Message(0, user)
    molly.show()
    sys.exit(app.exec_())
