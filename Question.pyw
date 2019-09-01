# A Dialog window that was created to allow for the user to Add/Remove Account SubTypes combobox.
# Was not designed to be modular. However I plan to revisit to see if additional flexibility can be built in.

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog
from QuestionUi import Ui_Question
from UPK import specific_sql_statement, obtain_sql_list
from StyleSheets import UniversalStyleSheet


class ATypeQuestion(QDialog):
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, database, parentType):
        super().__init__()
        self.ui = Ui_Question()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.parentType = parentType
        self.setStyleSheet(UniversalStyleSheet)
        self.show()
        self.ui.pushButtonAdd.clicked.connect(lambda: self.addType("AccountSubType"))
        self.ui.pushButtonRemove.clicked.connect(lambda: self.removeType("SubType", "AccountSubType", "ParentType"))
        self.ui.pushButtonCancel.clicked.connect(self.close)

    def addType(self, tablename):
        type, ok = QInputDialog.getText(self, 'Add', 'Enter Account Type:')
        if ok and type != '':
            addStatement = "INSERT INTO " + tablename + " VALUES('" + type + "', '" + self.parentType + "')"
            specific_sql_statement(addStatement, self.refUserDB)
        else:
            pass

    def removeType(self, colone, tablename, coltwo):
        typeStatement = "SELECT " + colone + " FROM " + tablename + " WHERE " + coltwo + "='" + self.parentType + "'"
        typeTuple = obtain_sql_list(typeStatement, self.refUserDB)
        typeList = []
        for account in typeTuple:
            typeList.append(account[0])
        print(typeList)
        type, ok = QInputDialog.getItem(self, "Remove", "Choose Account Type: ", typeList, 0, False)
        if ok and type:
            deleteStatement = "DELETE FROM " + tablename + " WHERE " + colone + " ='" + type + "' and " + coltwo + " ='" + self.parentType + "'"
            specific_sql_statement(deleteStatement, self.refUserDB)
        else:
            pass

    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = ATypeQuestion('i143yl2233l.db', 'Bank')
    lily.show()
    sys.exit(app.exec_())
