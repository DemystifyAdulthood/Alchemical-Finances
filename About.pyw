import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap
from AboutUi import Ui_Dialog
from StyleSheets import UniversalStyleSheet, aboutFrame


class AboutProgram(QDialog):
    remove_tab_about = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("About Page")
        self.setStyleSheet(UniversalStyleSheet)
        self.ui.FrameLogo.setStyleSheet(aboutFrame)
        self.ui.FrameProgram.setStyleSheet(aboutFrame)
        self.show()

        titleFont = QtGui.QFont()
        titleFont.setPointSize(36)
        titleFont.setWeight(75)
        titleFont.setBold(True)

        tagFont = QtGui.QFont()
        tagFont.setPointSize(28)
        tagFont.setWeight(50)
        tagFont.setItalic(True)

        aboutFont = QtGui.QFont()
        aboutFont.setPointSize(12)
        aboutFont.setWeight(50)

        self.ui.labelProgram.setText("""
 Alchemical Finances""")

        self.ui.labelProgram.setFont(titleFont)
        self.ui.labelProgram.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter)

        self.ui.labelTagLine.setText("""
-- Hands on Personal Finance --""")

        self.ui.labelTagLine.setFont(tagFont)
        self.ui.labelTagLine.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter)

        self.ui.labelVersion.setText("""
Current Version:        1.7""")

        self.ui.labelVersion.setFont(aboutFont)
        self.ui.labelVersion.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)

        self.ui.labelDeveloper.setText("""
Developed By:          Beaker Labs llc. [Coming Soon? Different Name?]""")

        self.ui.labelReleaseDate.setText("""
Release Date:           September 1st, 2019""")

        self.ui.labelSupport.setText("""
Support:                  Contact@demystifyAdulthood.com""")

        self.ui.labelDescription.setText("""
Background Information:
        
This project was brought to life to elevate my existing Microsoft(R)
Excel Financial Spreadsheets to their next level. Integrating in
native handling of receipts and invoices directly with the ledger 
without the fear of overloading the program. All, while maintaining 
a customizable ledger that allows the user to describe and
categorize their finances outside of the ridged structures of 
financial institutions. 
        
If during normal use of the program there are errors, or features you
would like to discuss feel free to reach out to the support e-mail
address.
""")

        self.logoImage = QPixmap('AF Logo.png')
        self.logoAdjustment = self.logoImage.scaled(381, 381, 1, 1)
        self.ui.labelLogo.setPixmap(self.logoAdjustment)

    # -- PyQt5 signal to remove ParentType Ledger from tabdic ----------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_about.emit("About")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = AboutProgram()
    lily.show()
    sys.exit(app.exec_())
