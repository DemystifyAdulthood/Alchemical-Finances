import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from CategoriesDialogUi import Ui_Dialog
from sqlite3 import Error
from UPK import check_characters, first_character_check
from StyleSheets import UniversalStyleSheet


class TransactionForm(QDialog):
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, database, parentType):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ Class Global Variables                                                                           ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        self.refUserDB = database
        self.accountType = parentType

        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ QDialog Functionality and initial Appearance                                                     ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        self.ui.lineEditMethod.setEnabled(False)
        self.ui.labelHeader.setText(parentType + " Accounts")
        self.fill_widget(self.ui.listWidgetCategory, "Method", "Categories", "ParentType")
        self.ui.pushButtonNew.clicked.connect(self.new_category)
        self.ui.pushButtonNewSubmit.clicked.connect(self.submit_new)
        self.ui.pushButtonEdit.clicked.connect(self.edit_category)
        self.ui.pushButtonEditSubmit.clicked.connect(self.submit_edit)
        self.ui.pushButtonDelete.clicked.connect(self.delete_category)
        self.ui.pushButtonCancel.clicked.connect(self.cancel_category)
        self.ui.listWidgetCategory.setCurrentRow(0)
        self.disp_current_category()
        self.ui.listWidgetCategory.itemClicked.connect(self.disp_current_category)
        self.setStyleSheet(UniversalStyleSheet)
        self.show()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ Button Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    def new_category(self):
        self.new_method_buttons()

    def submit_new(self):
        if self.syntax_check(self.ui.lineEditMethod.text().title()) is True:
            newStatement = "INSERT INTO Categories VALUES('" + self.ui.lineEditMethod.text() + "', '" + self.accountType + "')"
            self.category_sql(newStatement)
            self.reset_widgets()
        else:
            self.ui.labelError.setText("Error 41: Invalid Input")

    def edit_category(self):
        self.edit_method_buttons()

    def submit_edit(self):
        if self.syntax_check(self.ui.lineEditMethod.text().title()) is True:
            editStatement = "UPDATE Categories SET Method='" + self.ui.lineEditMethod.text() + "' WHERE Method='" + self.ui.listWidgetCategory.currentItem().text() + "'"
            self.category_sql(editStatement)
            self.reset_widgets()
        else:
            self.ui.labelError.setText("Error 51: Invalid Input")

    def delete_category(self):
        question = "Are you sure you want to delete this Transaction Method?"
        reply = QMessageBox.question(self, "Confirmation", question, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            deleteStatement = "DELETE FROM Categories WHERE Method ='" + self.ui.lineEditMethod.text() + "' AND ParentType ='" + self.accountType + "'"
            self.category_sql(deleteStatement)
            self.ui.listWidgetCategory.clear()
            self.fill_widget(self.ui.listWidgetCategory, "Method", "Categories", "ParentType")
            self.ui.lineEditMethod.setText("")
            self.ui.listWidgetCategory.setCurrentRow(0)
            self.disp_current_category()
        else:
            pass

    def cancel_category(self):
        self.reset_widgets()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ QDialog Appearance changing functions                                                                ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    def reset_widgets(self):
        self.ui.labelModifier.setText("Selected Transaction Method:")
        self.ui.lineEditMethod.setEnabled(False)
        self.ui.pushButtonNew.setEnabled(True)
        self.ui.pushButtonNew.show()
        self.ui.pushButtonNewSubmit.setEnabled(False)
        self.ui.pushButtonNewSubmit.hide()
        self.ui.pushButtonEdit.setEnabled(True)
        self.ui.pushButtonEdit.show()
        self.ui.pushButtonEditSubmit.setEnabled(False)
        self.ui.pushButtonEditSubmit.hide()
        self.ui.pushButtonDelete.setEnabled(True)
        self.ui.pushButtonDelete.show()
        self.ui.pushButtonCancel.setEnabled(False)
        self.ui.pushButtonCancel.hide()
        self.ui.lineEditMethod.setText("")
        self.ui.listWidgetCategory.clear()
        self.fill_widget(self.ui.listWidgetCategory, "Method", "Categories", "ParentType")
        self.ui.listWidgetCategory.setCurrentRow(0)
        self.disp_current_category()

    def new_method_buttons(self):
        self.ui.labelModifier.setText("Input New Transaction Method:")
        self.ui.lineEditMethod.setEnabled(True)
        self.ui.pushButtonNew.setEnabled(False)
        self.ui.pushButtonNew.hide()
        self.ui.pushButtonNewSubmit.setEnabled(True)
        self.ui.pushButtonNewSubmit.show()
        self.ui.pushButtonEdit.setEnabled(False)
        self.ui.pushButtonEdit.show()
        self.ui.pushButtonEditSubmit.setEnabled(False)
        self.ui.pushButtonEditSubmit.hide()
        self.ui.pushButtonDelete.setEnabled(False)
        self.ui.pushButtonDelete.hide()
        self.ui.pushButtonCancel.setEnabled(True)
        self.ui.pushButtonCancel.show()
        self.ui.lineEditMethod.setText("")
        self.ui.lineEditMethod.setFocus()

    def edit_method_buttons(self):
        self.ui.labelModifier.setText("Alter Transaction Method:")
        self.ui.lineEditMethod.setEnabled(True)
        self.ui.pushButtonNew.setEnabled(False)
        self.ui.pushButtonNew.show()
        self.ui.pushButtonNewSubmit.setEnabled(False)
        self.ui.pushButtonNewSubmit.hide()
        self.ui.pushButtonEdit.setEnabled(False)
        self.ui.pushButtonEdit.hide()
        self.ui.pushButtonEditSubmit.setEnabled(True)
        self.ui.pushButtonEditSubmit.show()
        self.ui.pushButtonDelete.setEnabled(False)
        self.ui.pushButtonDelete.hide()
        self.ui.pushButtonCancel.setEnabled(True)
        self.ui.pushButtonCancel.show()
        self.ui.lineEditMethod.setFocus()

    # --- General Dialog Functions ---------------------------------------------------------------------------------
    def disp_current_category(self):
        if self.ui.listWidgetCategory.currentItem() is None:
            selection = ""
        else:
            selection = self.ui.listWidgetCategory.currentItem().text()
        self.ui.lineEditMethod.setText(selection)

    def syntax_check(self, question):
        if check_characters(question) is False:
            return False
        elif question == "" or question == " ":
            return False
        elif first_character_check(question) is False:
            return False
        elif self.check_duplicate(question) is False:
            return False
        elif isinstance(question, str) is False:
            return False
        else:
            return True

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ SQLite3Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    def category_sql(self, statement):
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(statement)
        except Error:
            self.ui.labelHeader.setText("Error Deleting Category")
        finally:
            conn.close()

    def check_duplicate(self, category):
        statement = "SELECT Method, ParentType FROM Categories WHERE Method ='" + category + "' AND ParentType ='" + self.accountType + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(statement)
                row = cur.fetchone()
                if row is None:
                    return True
                else:
                    return False
        except Error:
            self.ui.labelError.setText("Error: 196")
        finally:
            conn.close()

    def fill_widget(self, combobox, col, tablename, coltwo):
        listStatement = "SELECT " + col + " FROM " + tablename + " WHERE " + coltwo + "= '" + self.accountType + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                conn.row_factory = lambda cursor, row: row[0]
                cur = conn.cursor()
                cur.execute(listStatement)
                comboTuple = cur.fetchall()
        except Error:
            self.ui.labelError.setText("Error: 210")
        finally:
            conn.close()
        combobox.addItems(comboTuple)

    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    sys.excepthook = sys.__excepthook__
    app = QApplication(sys.argv)
    database = "174l7y9i3l3.db"
    parentType = "Bank"
    lily = TransactionForm(database, parentType)
    lily.show()
    sys.exit(app.exec_())
