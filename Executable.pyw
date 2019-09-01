"""
As the current file name states. This file is to execute the entire program. I will refer to it as my nexus Point
  Porcelainoffering = QDialog for User Login
  Zophran = QDialog for Messages
  Porcelaingod = QMainWindow for the programs main hub.
"""

import sys

from PyQt5.QtWidgets import QDialog, QApplication
from UserLogin import LoginForm
from AlchemicalFinances import AFBackbone
from WelcomeMessage import Message


if __name__ == "__main__":
    app = QApplication(sys.argv)
    porcelainoffering = LoginForm()
    if porcelainoffering.exec_() == QDialog.Accepted:
        user = porcelainoffering.refUser
        messageCount = porcelainoffering.count
        zophran = Message(messageCount, user)
        if zophran.exec_() == QDialog.Accepted:
            porcelaingod = AFBackbone(user, messageCount)
            porcelaingod.show()
            sys.exit(app.exec_())
