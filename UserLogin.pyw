# This program controls the User login.

# Future Concepts
# 1 - Incorporate an e-mail address to profile for password recovery.
#   - will require understanding of how to write and send an e-mail via python. Shouldn't be to complicated.
#   - My Famous Last Words
# 3 - Incorporate a date stamp for date of last login -  not sure necessary.


import sys
import sqlite3

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtCore, QtWidgets
from sqlite3 import Error
from pathlib import Path
from UserLoginUi import Ui_Dialog
from UPK import account_pathway, generate_key, check_characters_login, spacing_check
from StyleSheets import loginStyleSheet, titleStyleSheet, subtitleStyleSheet, generalError


class LoginForm(QDialog):
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self):
        super().__init__()
        # Initial Appearance
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.labelConfirmPassword.hide()
        self.ui.pushButtonSubmitProfile.hide()
        self.ui.pushButtonCancelProfile.hide()
        self.ui.lineEditConfirmPassword.hide()
        # Button Functionality
        self.ui.pushButtonLogin.clicked.connect(self.user_login)
        self.ui.pushButtonQuit.clicked.connect(self.quit_app)
        self.ui.pushButtonNewProfile.clicked.connect(self.new_profile)
        self.ui.pushButtonSubmitProfile.clicked.connect(self.submit_profile)
        self.ui.pushButtonCancelProfile.clicked.connect(self.cancel_profile)
        self.dbPathway = account_pathway("UAInformation.db")
        self.dbPathway = Path.cwd() / self.dbPathway[0]
        self.refUser = None
        self.count = None
        self.appearance("initial")
        self.setStyleSheet(loginStyleSheet)
        self.ui.labelTitle.setStyleSheet(titleStyleSheet)
        self.ui.labelSubTitle.setStyleSheet(subtitleStyleSheet)
        self.show()

    def appearance(self, condition):
        if condition == "initial":  # Start-Up // Cancel Profile
            self.setMaximumSize(QtCore.QSize(345, 230))
            self.resize(345, 230)
            self.ui.lineEditPassword.setStyleSheet(loginStyleSheet)
            self.ui.lineEditUserProfile.setStyleSheet(loginStyleSheet)
            self.ui.labelUserProfile.setGeometry(QtCore.QRect(51, 100, 91, 20))
            self.ui.lineEditUserProfile.setGeometry(QtCore.QRect(142, 100, 150, 20))
            self.ui.labelPassword.setGeometry(QtCore.QRect(51, 130, 91, 20))
            self.ui.lineEditPassword.setGeometry(QtCore.QRect(142, 130, 150, 20))
            self.ui.pushButtonLogin.setGeometry(QtCore.QRect(65, 160, 100, 25))
            self.ui.pushButtonSubmitProfile.setGeometry(QtCore.QRect(65, 160, 100, 25))
            self.ui.pushButtonQuit.setGeometry(QtCore.QRect(175, 160, 100, 25))
            self.ui.pushButtonCancelProfile.setGeometry(QtCore.QRect(175, 160, 100, 25))
            self.ui.pushButtonNewProfile.setGeometry(QtCore.QRect(65, 190, 210, 25))
            self.ui.labelResponse.setGeometry(QtCore.QRect(20, 260, 300, 41))
            self.ui.labelResponse.setText("")
        elif condition == "LogError":  # user_login
            self.ui.lineEditUserProfile.setStyleSheet(generalError)
            self.ui.lineEditPassword.setStyleSheet(generalError)
            self.ui.labelResponse.setStyleSheet(generalError)
            self.setMaximumSize(QtCore.QSize(345, 280))
            self.resize(345, 280)
            self.ui.labelUserProfile.setGeometry(QtCore.QRect(51, 100, 91, 20))
            self.ui.lineEditUserProfile.setGeometry(QtCore.QRect(142, 100, 150, 20))
            self.ui.labelPassword.setGeometry(QtCore.QRect(51, 130, 91, 20))
            self.ui.lineEditPassword.setGeometry(QtCore.QRect(142, 130, 150, 20))
            self.ui.pushButtonLogin.setGeometry(QtCore.QRect(65, 160, 100, 25))
            self.ui.pushButtonSubmitProfile.setGeometry(QtCore.QRect(65, 160, 100, 25))
            self.ui.pushButtonQuit.setGeometry(QtCore.QRect(175, 160, 100, 25))
            self.ui.pushButtonCancelProfile.setGeometry(QtCore.QRect(175, 160, 100, 25))
            self.ui.pushButtonNewProfile.setGeometry(QtCore.QRect(65, 190, 210, 25))
            self.ui.labelResponse.setGeometry(QtCore.QRect(20, 230, 300, 41))
        elif condition == "New":  # submit_profile
            self.setMaximumSize(QtCore.QSize(345, 275))
            self.resize(345, 275)
            self.ui.lineEditPassword.setStyleSheet(loginStyleSheet)
            self.ui.lineEditUserProfile.setStyleSheet(loginStyleSheet)
            self.ui.labelUserProfile.setGeometry(QtCore.QRect(20, 100, 141, 20))
            self.ui.lineEditUserProfile.setGeometry(QtCore.QRect(170, 100, 150, 20))
            self.ui.labelPassword.setGeometry(QtCore.QRect(20, 130, 141, 20))
            self.ui.lineEditPassword.setGeometry(QtCore.QRect(170, 130, 150, 20))
            self.ui.pushButtonLogin.setGeometry(QtCore.QRect(65, 200, 100, 25))
            self.ui.pushButtonSubmitProfile.setGeometry(QtCore.QRect(65, 200, 100, 25))
            self.ui.pushButtonQuit.setGeometry(QtCore.QRect(175, 200, 100, 25))
            self.ui.pushButtonCancelProfile.setGeometry(QtCore.QRect(175, 200, 100, 25))
            self.ui.pushButtonNewProfile.setGeometry(QtCore.QRect(65, 230, 210, 25))
            self.ui.labelResponse.setGeometry(QtCore.QRect(20, 260, 300, 41))
            self.ui.labelResponse.setText("")
        elif condition == "NewError":  # New_Profile_error
            self.setMaximumSize(QtCore.QSize(345, 310))
            self.resize(345, 310)
            self.ui.lineEditPassword.setStyleSheet(generalError)
            self.ui.lineEditConfirmPassword.setStyleSheet(generalError)
            self.ui.labelResponse.setStyleSheet(generalError)
            self.ui.labelUserProfile.setGeometry(QtCore.QRect(20, 100, 141, 20))
            self.ui.labelPassword.setGeometry(QtCore.QRect(20, 130, 141, 20))
            self.ui.pushButtonLogin.setGeometry(QtCore.QRect(65, 200, 100, 25))
            self.ui.pushButtonSubmitProfile.setGeometry(QtCore.QRect(65, 200, 100, 25))
            self.ui.pushButtonQuit.setGeometry(QtCore.QRect(175, 200, 100, 25))
            self.ui.pushButtonCancelProfile.setGeometry(QtCore.QRect(175, 200, 100, 25))
            self.ui.pushButtonNewProfile.setGeometry(QtCore.QRect(65, 230, 210, 25))
            self.ui.labelResponse.setGeometry(QtCore.QRect(20, 260, 300, 41))
        elif condition == "NewLabel":  # New_Profile_Accepted
            self.setMaximumSize(QtCore.QSize(345, 310))
            self.resize(345, 310)
            self.ui.lineEditPassword.setStyleSheet(loginStyleSheet)
            self.ui.lineEditUserProfile.setStyleSheet(loginStyleSheet)
            self.ui.labelResponse.setStyleSheet(loginStyleSheet)
            self.ui.labelUserProfile.setGeometry(QtCore.QRect(20, 100, 141, 20))
            self.ui.labelPassword.setGeometry(QtCore.QRect(20, 130, 141, 20))
            self.ui.pushButtonLogin.setGeometry(QtCore.QRect(65, 200, 100, 25))
            self.ui.pushButtonSubmitProfile.setGeometry(QtCore.QRect(65, 200, 100, 25))
            self.ui.pushButtonQuit.setGeometry(QtCore.QRect(175, 200, 100, 25))
            self.ui.pushButtonCancelProfile.setGeometry(QtCore.QRect(175, 200, 100, 25))
            self.ui.pushButtonNewProfile.setGeometry(QtCore.QRect(65, 230, 210, 25))
            self.ui.labelResponse.setGeometry(QtCore.QRect(20, 260, 300, 41))

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ Button Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Quit Application ------------------------------------------------------------------------------------------
    def quit_app(self):
        self.close()

    # --- -- User Login function. Used to bridge the UserLogin Dialog with the Alchemical_Finances Main window ---------
    def user_login(self):
        self.table_check()
        lookupStatement = "SELECT Profile, Password FROM Users WHERE Profile like '" + \
                          self.ui.lineEditUserProfile.text().lower() +\
                          "' and Password like '" + self.ui.lineEditPassword.text() + "'"
        # SELECT X, Y FROM Tablename WHERE X like 'X.data' + and Y like 'Y.data'
        conn = sqlite3.connect(self.dbPathway)
        cur = conn.cursor()
        cur.execute(lookupStatement)
        row = cur.fetchone()
        if row is None:
            self.ui.labelResponse.setText("Profile & Password Do Not Match.\n Create New User?")
            self.appearance("LogError")
            conn.close()
        else:
            print('hello')
            self.ui.labelResponse.setText("Welcome!")
            self.refUser = self.ui.lineEditUserProfile.text().lower()
            self.count = self.message_count()
            conn.close()
            self.accept()
            # User Financial Database will be created within the MainWindow.

    # --- -- Changes the dialog for the addition of a new Profile ------------------------------------------------------
    def new_profile(self):
        self.appearance("New")
        self.ui.labelConfirmPassword.show()
        self.ui.pushButtonSubmitProfile.show()
        self.ui.pushButtonSubmitProfile.setEnabled(True)
        self.ui.pushButtonCancelProfile.show()
        self.ui.pushButtonCancelProfile.setEnabled(True)
        self.ui.lineEditConfirmPassword.show()
        self.ui.pushButtonLogin.hide()
        self.ui.pushButtonLogin.setEnabled(False)
        self.ui.pushButtonQuit.hide()
        self.ui.pushButtonQuit.setEnabled(False)
        self.ui.labelUserProfile.setText("New Profile Name:")
        self.ui.labelPassword.setText("New Password:")
        self.ui.lineEditUserProfile.setText("")
        self.ui.lineEditPassword.setText("")
        self.ui.lineEditConfirmPassword.setText("")
        self.ui.lineEditUserProfile.setFocus()

    # --- -- 'Parent' Function for the addition of a new profile. ------------------------------------------------------
    # --- -- - Ensures passwords match and that it is over 6 characters ------------------------------------------------
    def submit_profile(self):
        if self.ui.lineEditPassword.text() != self.ui.lineEditConfirmPassword.text():
            self.ui.labelResponse.setText("Passwords Do Not Match")
            self.appearance("NewError")
        elif len(self.ui.lineEditPassword.text()) < 6:
            self.ui.labelResponse.setText("Password Rule:\n Greater Than 6 Characters")
            self.appearance("NewError")
        elif isinstance(self.ui.lineEditUserProfile.text(), str) is False:
            self.ui.labelResponse.setText("Profile Name can not be numerical")
            self.appearance("NewError")
        elif spacing_check(self.ui.lineEditUserProfile.text()) is False:
            self.ui.labelResponse.setText("Profile Name Formatted Wrong:\n No Blank Spaces")
            self.appearance("NewError")
        elif check_characters_login(self.ui.lineEditUserProfile.text()) is False:
            self.ui.labelResponse.setText("Profile Name must be numerical")
            self.appearance("NewError")
        elif check_characters_login(self.ui.lineEditPassword.text()) is False:
            self.ui.labelResponse.setText("Password must be alphanumeric")
            self.appearance("NewError")
        elif spacing_check(self.ui.lineEditPassword.text()) is False:
            self.ui.labelResponse.setText("Password Formatted Wrong:\n No Blank Spaces")
            self.appearance("NewError")
        else:
            if self.profile_check() is True:
                self.add_user()

    # --- -- Returns dialog back to initial state for login purposes ---------------------------------------------------
    def cancel_profile(self):
        self.appearance("initial")
        self.ui.labelConfirmPassword.hide()
        self.ui.pushButtonSubmitProfile.hide()
        self.ui.pushButtonSubmitProfile.setEnabled(False)
        self.ui.pushButtonCancelProfile.hide()
        self.ui.pushButtonCancelProfile.setEnabled(False)
        self.ui.lineEditConfirmPassword.hide()
        self.ui.pushButtonLogin.show()
        self.ui.pushButtonLogin.setEnabled(True)
        self.ui.pushButtonQuit.show()
        self.ui.pushButtonQuit.setEnabled(True)
        self.ui.labelUserProfile.setText("User Profile:")
        self.ui.labelPassword.setText("Password:")
        self.ui.lineEditUserProfile.setText("")
        self.ui.lineEditPassword.setText("")
        self.ui.lineEditConfirmPassword.setText("")

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ SQLite3 Functions                                                                                    ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Checks for existence of the Table and if User Profile already exists --------------------------------------
    def table_check(self):
        sQLTableCheck = "CREATE TABLE IF NOT EXISTS Users(Profile TEXT, Password TEXT," +\
                        " Number TEXT, Message INTEGER, Creation TEXT)"
        conn = sqlite3.connect(self.dbPathway)
        cur = conn.cursor()
        cur.execute(sQLTableCheck)
        conn.close()

    # --- -- Check for existence of a User Profile and Number. No Duplicates of Profile or Number ----------------------
    def profile_check(self):
        self.table_check()
        userCheck = "SELECT Profile FROM Users WHERE Profile = '" + self.ui.lineEditUserProfile.text().lower() + "'"
        conn = sqlite3.connect(self.dbPathway)
        cur = conn.cursor()
        cur.execute(userCheck)
        row = cur.fetchone()
        if row is None:
            conn.close()
            return True
        else:
            conn.close()
            self.ui.labelResponse.setText("User Profile Already Exists")
            self.appearance("NewError")

    # --- -- Found that the try clause was necessary. Unsure as to why this is the case. -------------------------------
    # --- -- - Generates User Key -> Adds user -------------------------------------------------------------------------
    def add_user(self):
        from datetime import datetime
        generateUserKey = generate_key()
        creationdate = datetime.now().strftime("%Y/%m/%d")
        SQLNewProfile = "INSERT INTO Users VALUES('" + self.ui.lineEditUserProfile.text().lower() + "', '" +\
                        self.ui.lineEditConfirmPassword.text() + "', '" + generateUserKey + "', '0', '" +\
                        creationdate + "')"
        try:
            conn = sqlite3.connect(self.dbPathway)
            with conn:
                cur = conn.cursor()
                cur.execute(SQLNewProfile)
                self.appearance("NewLabel")
                self.ui.labelResponse.setText("New User Created \n Hit Cancel: Then Login")
        except Error as e:
            self.ui.labelResponse.setText("Error Occurred: Please Retry")
        finally:
            conn.close()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ Welcome Message Related Functions                                                                    ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Initiated upon signing into the application ---------------------------------------------------------------
    def message_count(self):
        messageStatement = "SELECT Message FROM Users WHERE Profile= '" + self.refUser + "'"
        conn = sqlite3.connect(self.dbPathway)
        cur = conn.cursor()
        cur.execute(messageStatement)
        row = cur.fetchone()
        if row is None:
            conn.close()
        else:
            count = row[0]
            conn.close()
            if count == 0:
                messageCount = count + 1
                self.update_count(messageCount)
            else:
                pass
        return count

    # --- -- Changes the count for the message to ensure no repeated messages ------------------------------------------
    def update_count(self, count):
        updatedCount = count
        updateStatement = "UPDATE Users SET Message = " + str(updatedCount) + " WHERE Profile = '" + self.refUser + "'"
        # UPDATE Table name set X = 'y.data' WHERE Profile = 'z.data'
        try:
            conn = sqlite3.connect(self.dbPathway)
            with conn:
                cur = conn.cursor()
                cur.execute(updateStatement)
        finally:
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginForm()
    login.show()
    sys.exit(app.exec_())
