import shutil
import sys
import sqlite3


from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QInputDialog
from PyQt5 import QtCore, QtWidgets
from sqlite3 import Error
from pathlib import Path
from ArchiveUi import Ui_Dialog
from Receipt import Receipt
from UPK import obtain_sql_value, switch_sql_tables, modify_for_sql, receipt_pathway, disp_ledgerV1, disp_ledgerV2
from StyleSheets import UniversalStyleSheet


class Archive(QDialog):
    remove_tab_archive = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, database, user):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Archive")
        self.setStyleSheet(UniversalStyleSheet)
        self.show()

    # --- Class Global Variables --------------------------------------------------------------------------------
        self.refUserDB = database
        self.refUser = user

        self.widgetlist = [self.ui.comboBoxA, self.ui.tableWidgetL1]

        self.buttonlist = [self.ui.pushButtonRestore, self.ui.pushButtonDelete, self.ui.pushButtonDisplay]

        self.parentType_dict = {"Bank": "Bank_Account_Details", "Equity": "Equity_Account_Details",
                                "Retirement": "Retirement_Account_Details", "CD": "CD_Account_Details",
                                "Treasury": "Treasury_Account_Details", "Debt": "Debt_Account_Details",
                                "Credit": "Credit_Account_Details", "Cash": "Cash_Account_Details"}
        # Fill QCombobox
        self.fill_combobox(self.widgetlist[0])
        self.display_ledger()

        # QPushbutton - Restore
        self.widgetlist[0].currentIndexChanged.connect(self.display_ledger)
        self.buttonlist[0].clicked.connect(self.restore_account)
        self.buttonlist[1].clicked.connect(self.delete_account)
        self.buttonlist[2].clicked.connect(self.display_receipt)

        # QPushbutton - Delete
        # QPushbutton - Display Receipt

        # Restore function
        # Delete function
        # Display Receipt Function
        # Fill / Refresh QCombobox
        # Display Account Function
        # Display proper ledger Function

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------General Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    def restore_account(self):
        switch_sql_tables("Account_Summary", "Account_Archive", "ID", self.widgetlist[0].currentText(), self.refUserDB)
        self.widgetlist[0].clear()
        self.fill_combobox(self.widgetlist[0])
        self.display_ledger()

    def delete_account(self):
        ledger_name = self.widgetlist[0].currentText()
        modified_ledger_name = modify_for_sql(ledger_name)

        parentType_statement = "SELECT ParentType FROM Account_Archive WHERE ID='" + ledger_name + "'"
        parentType_value = obtain_sql_value(parentType_statement, self.refUserDB)
        parentType_value = parentType_value[0]
        details_table = self.parentType_dict[parentType_value]

        delete_message = "Selecting 'YES' will permanently delete this account and all associated information"
        confirm = QMessageBox.warning(self, 'Confirm', delete_message, QMessageBox.Yes, QMessageBox.No)

        receipt_directory_path = Path.cwd() / 'Receipts' / parentType_value / modified_ledger_name

        if confirm == QMessageBox.Yes:
            delete_archive = "DELETE FROM Account_Archive WHERE ID = '" + ledger_name + "'"
            delete_details = "DELETE FROM " + details_table + " WHERE Account_Name ='" + ledger_name + "'"
            delete_ledger = "DROP TABLE IF EXISTS " + modified_ledger_name
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(delete_archive)
                    cur.execute(delete_details)
                    cur.execute(delete_ledger)
            except Error:
                print("Error: Archive 86")
            finally:
                conn.close()
                shutil.rmtree(receipt_directory_path)
                self.widgetlist[0].clear()
                self.fill_combobox(self.widgetlist[0])
                self.widgetlist[1].clear()
                self.display_ledger()
        else:
            pass

    def display_receipt(self):
        ledger = self.widgetlist[0].currentText()
        ledger_sql = modify_for_sql(ledger)

        parentType_statement = "SELECT ParentType FROM Account_Archive WHERE ID='" + ledger + "'"
        parentType_value = obtain_sql_value(parentType_statement, self.refUserDB)
        parentType_value = parentType_value[0]

        inputText1 = "Select Row"
        inputText2 = "Enter Row#: "
        row = self.user_selection_input(self.widgetlist[1], inputText1, inputText2)
        if row == -1:
            pass
        else:
            file_Name_Statement = "SELECT Receipt FROM " + ledger_sql + " WHERE RowID = " + str(row)
            file_Name = obtain_sql_value(file_Name_Statement, self.refUserDB)
            file_Name = file_Name[0]

            if file_Name == "":
                noReceipt = "Sorry, No Receipt Uploaded"
                self.input_error_msg(noReceipt)
            else:
                file_pathway = receipt_pathway(parentType_value, ledger, file_Name, self.refUser)
                pathway = Path.cwd() / file_pathway
                ion = Receipt(str(pathway), file_Name)
                if ion.exec_() == QDialog.Accepted:
                    pass

    def display_ledger(self):
        ledger = self.widgetlist[0].currentText()
        if ledger == "":
            pass
        else:
            parentType_statement = "SELECT ParentType FROM Account_Archive WHERE ID='" + ledger + "'"
            parentType_value = obtain_sql_value(parentType_statement, self.refUserDB)
            parentType_value = parentType_value[0]

            type1 = ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit"]
            type2 = ["Equity", "Retirement"]

            if parentType_value in type1:
                disp_ledgerV1(self.widgetlist[0], self.widgetlist[1], self.refUserDB)
            elif parentType_value in type2:
                disp_ledgerV2(self.widgetlist[0], self.widgetlist[1], self.refUserDB)
            else:
                error = "Ledger Type Doesn't Exist"
                self.input_error_msg(error)

    def display_info(self):
        # might not need function
        pass

    # --- -- Error Message ---------------------------------------------------------------------------------------------
    def input_error_msg(self, message):
        reply = QMessageBox.warning(self, 'Input Error', message, QMessageBox.Ok, QMessageBox.NoButton)
        if reply == QMessageBox.Ok:
            pass
        else:
            pass

    # -- Fill Combobox -------------------------------------------------------------------------------------------------
    def fill_combobox(self, combobox):
        combo_sql_statement = "SELECT ID FROM Account_Archive"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                conn.row_factory = lambda cursor, row: row[0]
                cur = conn.cursor()
                cur.execute(combo_sql_statement)
                comboTuple = cur.fetchall()
        except Error:
            print("Error Archive: 182")
        finally:
            conn.close()
        combobox.addItems(comboTuple)
        combobox.model().sort(0)
        combobox.setCurrentIndex(0)

    # --- -- Input Dialog to obtain which row to select // Select//Update//Delete --------------------------------------
    def user_selection_input(self, tableWidget, text1, text2):
        row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
        if ok and row:
            return row
        else:
            row = 0
            return row

    # -- PyQt5 signal to remove ParentType Ledger from tabdic ----------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_archive.emit("Archive")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = Archive("data/account/0cdio570sd64r7.db")
    lily.show()
    sys.exit(app.exec_())