# Ledger Design for Bank, CD, TB, Cash, Debt, Credit Card
# Structured to allow for future modification for other uses.

import sys
import sqlite3
import os


from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog, QApplication, QInputDialog
from PyQt5.QtCore import QDate
from PyQt5 import QtCore, QtWidgets
from sqlite3 import Error
from pathlib import Path, PurePath
from shutil import copy
from AccountsDialog import Accounts
from CategoriesDialog import TransactionForm
from Receipt import Receipt
from Ledger1Ui import Ui_Dialog
from UPK import receipt_pathway, obtain_sql_value, modify_for_sql, check_characters, specific_sql_statement,\
    decimal_places, add_comma, remove_comma, disp_ledgerV1
from StyleSheets import UniversalStyleSheet, uFrameStyleSheet, uTitleStyleSheet


class LedgerV1(QDialog):
    refresh_signal = QtCore.pyqtSignal(str)
    remove_tab = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, database, parentType, user):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parentType)
        self.setStyleSheet(UniversalStyleSheet)
        self.show()

        # --- Class Global Variables -----------------------------------------------------------------------------------
        self.refUserDB = database
        self.parentType = parentType
        self.refUser = user

        self.widgetlist = [self.ui.comboBoxL1, self.ui.tableWidgetL1, self.ui.dateEditL1,
                           self.ui.lineEditL1TM, self.ui.lineEditL1TD, self.ui.comboBoxL1C,
                           self.ui.lineEditL1Debit, self.ui.lineEditL1Credit, self.ui.textEditL1Notes,
                           self.ui.radioButtonL1Pending, self.ui.radioButtonL1Posted, self.ui.lineEditReceiptL1]
        # 12 widgets
        self.buttonlist = [self.ui.pushButtonNewL1, self.ui.pushButtonCatL1, self.ui.pushButtonUploadL1,
                           self.ui.pushButtonDisplayL1, self.ui.pushButtonAddL1, self.ui.pushButtonSelectL1,
                           self.ui.pushButtonUpdateL1, self.ui.pushButtonDeleteL1, self.ui.pushButtonClearL1,
                           self.ui.pushButtonRClearL1, self.ui.pushButtonRDeleteL1, self.ui.pushButtonSearchL1,
                           self.ui.pushButtonDispRangL1]

        self.parentType_dict = {"Bank": "Bank_Account_Details", "Equity": "Equity_Account_Details",
                                "Retirement": "Retirement_Account_Details", "CD": "CD_Account_Details",
                                "Treasury": "Treasury_Account_Details", "Debt": "Debt_Account_Details",
                                "Credit": "Credit_Account_Details", "Cash": "Cash_Account_Details"}

        # --- Prepare Widgets for use ----------------------------------------------------------------------------------
        self.fill_combobox(self.widgetlist[0], "ID", "Account_Summary", "ParentType", self.parentType)
        self.fill_combobox(self.widgetlist[5], "Method", "Categories", "ParentType", self.parentType)

        self.ui.frameLeft.setStyleSheet(uFrameStyleSheet)
        self.ui.frameMiddle.setStyleSheet(uFrameStyleSheet)
        self.ui.frameRight.setStyleSheet(uFrameStyleSheet)
        self.ui.labelStaticL12.setStyleSheet(uTitleStyleSheet)
        self.ui.labelL1NV.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable1A.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable1B.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable2A.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable2B.setStyleSheet(uTitleStyleSheet)

        # --- Ledger Button Functions ----------------------------------------------------------------------------------
        # --- -- Prepares Functionality of the Ledger Variant 1 --------------------------------------------------------
        self.widgetlist[0].currentIndexChanged.connect(self.disp_current_ledger)    # Account Combobox
        self.buttonlist[0].clicked.connect(self.accounts_dialog)                    # Modify Button Account Combobox
        self.buttonlist[1].clicked.connect(self.categories_dialog)                  # Modify Button Category Combobox
        self.buttonlist[4].clicked.connect(self.add_transaction)                    # Add Transaction Button
        self.buttonlist[5].clicked.connect(self.select_transaction)                 # Select Button
        self.buttonlist[6].clicked.connect(self.update_transaction)                 # Update Button
        self.buttonlist[7].clicked.connect(self.delete_transaction)                 # Delete Button
        self.buttonlist[2].clicked.connect(self.upload_receipt_button)              # Upload Button
        self.buttonlist[8].clicked.connect(self.clear_inputs)                       # Clear Button
        self.buttonlist[3].clicked.connect(self.display_receipt)                    # Display Button
        self.widgetlist[2].setDate(QDate.currentDate())                             # DateEdit Widget
        self.widgetlist[9].setChecked(True)                                         # Pending RadioButton
        self.buttonlist[9].clicked.connect(self.clear_receipt_action)               # Clear Receipt Input
        self.buttonlist[10].clicked.connect(self.delete_receipt_action)             # Delete Receipt
        self.disp_current_ledger()
        self.initialmoneylist = self.net_ledger_value()
        self.ui.labelL1NV.setText(self.initialmoneylist[1])
        self.set_variable1B()
        self.set_variable2B()
        self.set_l1_appearance()

        self.buttonlist[11].hide()
        self.buttonlist[12].hide()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------opens Outside QDialogs                                                                                ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Creates Modal QDialog for User to Modify Account List -----------------------------------------------------
    def accounts_dialog(self):
        alf = Accounts(self.refUserDB, self.parentType, self.refUser)
        if alf.exec_() == QDialog.Accepted:
            self.widgetlist[0].clear()
            self.fill_combobox(self.widgetlist[0], "ID", "Account_Summary", "ParentType", self.parentType)
            self.set_variable1B()
            self.set_variable2B()
            self.trigger_refresh()

    # --- -- Creates Modal QDialog for User to Modify Category List ----------------------------------------------------
    def categories_dialog(self):
        molly = TransactionForm(self.refUserDB, self.parentType)
        if molly.exec_() == QDialog.Accepted:
            self.widgetlist[5].clear()
            self.fill_combobox(self.widgetlist[5], "Method", "Categories", "ParentType", self.parentType)

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------General Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Adjusts the Ledgers Appearance for differen ParentTypes ---------------------------------------------------
    def set_l1_appearance(self):
        if self.parentType == "Bank":
            self.ui.frameRight.hide()
            self.ui.labelVariable2A.hide()
            self.ui.labelVariable2B.hide()
            self.ui.frameLeft.setGeometry(QtCore.QRect(325, 60, 275, 40))
            self.ui.frameMiddle.setGeometry(QtCore.QRect(610, 60, 225, 40))
        elif self.parentType == "CD" or self.parentType == "Treasury":
            pass
        elif self.parentType == "Credit":
            self.ui.frameRight.hide()
            self.ui.labelVariable2A.hide()
            self.ui.labelVariable2B.hide()
            self.ui.labelVariable1A.setText("Credit Limit:")
            self.ui.frameLeft.setGeometry(QtCore.QRect(325, 60, 275, 40))
            self.ui.frameMiddle.setGeometry(QtCore.QRect(610, 60, 225, 40))
        elif self.parentType == "Debt":
            self.ui.labelVariable2A.setText(" Starting Balance:")
        else:
            self.ui.frameMiddle.hide()
            self.ui.frameRight.hide()
            self.ui.frameLeft.setGeometry(QtCore.QRect(467, 60, 275, 40))

    # --- -- Determines the status of the transaction and turns it into a string ---------------------------------------
    def transaction_status(self, status1, status2):
        if status1.isChecked() is True:
            currentStatus1 = "Pending"
            return currentStatus1
        elif status2.isChecked() is True:
            currentStatus2 = "Posted"
            return currentStatus2
        else:
            currentStatus3 = "Unknown"
            return currentStatus3

    # --- -- used to check user inputs to ensure no DB issues ----------------------------------------------------------
    def check_transactions(self):
        if check_characters(self.widgetlist[3].text()) is False:
            return False    # TM Has Non Alphanumeric characters
        elif check_characters(self.widgetlist[4].text()) is False:
            return False    # TD Has Non Alphanumeric characters
        elif self.widgetlist[4].text() == "" or self.widgetlist[4].text() == " ":
            return False    # TD is Blank
        elif check_characters(self.widgetlist[6].text()) is False:
            return False    # Debit is a non alphanumeric character
        elif check_characters(self.widgetlist[7].text()) is False:
            return False    # Credit is a non alphanumeric character
        elif check_characters(self.widgetlist[8].toPlainText()) is False:
            return False    # Notes Has Non Alphanumeric characters
        elif self.check_numerical_inputs(self.widgetlist[6].text()) is True and self.check_numerical_inputs(self.widgetlist[7].text()) is True:
            return False
        elif len(self.widgetlist[8].toPlainText()) > 150:
            return False
        elif self.widgetlist[6].text() == "" and self.widgetlist[7].text() == "":
            return True     # Debit and Credit are blank
        elif self.check_numerical_inputs(self.widgetlist[6].text()) is True and self.widgetlist[7].text() == "":
            return True     # Debit is Numerical and Credit is Blank
        elif self.widgetlist[6].text() == "" is True and self.check_numerical_inputs(self.widgetlist[7].text()):
            return True     # Debit is Blank and Credit is Numerical
        else:
            return True

    # --- -- Checks to ensure the input is numerical -------------------------------------------------------------------
    def check_numerical_inputs(self, userInput):
        try:
            float(userInput)
            return True
        except ValueError:
            return False

    # --- -- Error Message ---------------------------------------------------------------------------------------------
    def input_error_msg(self, message):
        reply = QMessageBox.warning(self, 'Input Error', message, QMessageBox.Ok, QMessageBox.NoButton)
        if reply == QMessageBox.Ok:
            pass
        else:
            pass

    # --- -- Input Dialog to obtain which row to select // Select//Update//Delete --------------------------------------
    def user_selection_input(self, tableWidget, text1, text2):
        row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
        if ok and row:
            return row
        else:
            row = 0
            return row

    # --- -- Clear User Inputs -----------------------------------------------------------------------------------------
    def clear_inputs(self):
        self.widgetlist[2].setDate(QDate.currentDate())
        self.widgetlist[3].setText("")
        self.widgetlist[4].setText("")
        self.widgetlist[5].setCurrentIndex(0)
        self.widgetlist[6].setText("")
        self.widgetlist[7].setText("")
        self.widgetlist[8].setPlainText("")
        self.widgetlist[9].setChecked(True)
        self.clear_receipt_action()
        self.widgetlist[3].setFocus()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------SQLite Based Functions                                                                                ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Displays the current ledger // Also refreshes ledger when updated -----------------------------------------
    def disp_current_ledger(self):
        disp_ledgerV1(self.widgetlist[0], self.widgetlist[1], self.refUserDB)
        initialmoneylist = self.net_ledger_value()
        self.ui.labelL1NV.setText(initialmoneylist[1])
        self.set_variable1B()
        self.set_variable2B()

    # --- -- Adds the transaction to the ledger ------------------------------------------------------------------------
    def add_transaction(self):
        if self.widgetlist[0].currentText() == "":
            noLedger_msg = "Create a new Ledger"
            self.input_error_msg(noLedger_msg)
        else:
            if self.check_transactions() is True:
                from datetime import datetime
                ledgerName = self.widgetlist[0].currentText()
                modifiedLN = modify_for_sql(ledgerName)
                modDebit = decimal_places(self.widgetlist[6].text(), 2)
                modCredit = decimal_places(self.widgetlist[7].text(), 2)
                status = self.transaction_status(self.widgetlist[9], self.widgetlist[10])
                currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                # 2- date -- 3- T Method -- 4- T Description -- 5- Category
                # 6- Debit -- 7- Credit -- 8- Notes -- 9- Status -- 10- UserDate -- 11- Receipt
                addStatement = "INSERT INTO " + modifiedLN + " VALUES('"\
                               + self.widgetlist[2].date().toString("yyyy/MM/dd") + "', '"\
                               + self.widgetlist[3].text() + "', '"\
                               + self.widgetlist[4].text() + "', '"\
                               + self.widgetlist[5].currentText() + "', '"\
                               + str(modDebit) + "', '"\
                               + str(modCredit) + "', '"\
                               + self.widgetlist[8].toPlainText() + "', '"\
                               + status + "', '"\
                               + self.widgetlist[11].text() + "', '"\
                               + currentDate + "', '"\
                               + currentDate + "')"
                self.post_transaction_sql(addStatement)
                ledgerValue = self.net_ledger_value()
                self.ui.labelL1NV.setText(ledgerValue[1])
                balanceStatement = "UPDATE Account_Summary SET Balance='" + ledgerValue[0] + "' WHERE ID='" + self.widgetlist[0].currentText() + "'"
                specific_sql_statement(balanceStatement, self.refUserDB)
                self.clear_inputs()
                self.trigger_refresh()
            else:
                input_error = """
                    Transaction Input Instructions:

                1  :  (*) Denotes required input field
                2  :  Alphanumeric inputs only
                3  :  Check the character length of your
                      additional notes input

                """
                self.input_error_msg(input_error)

    # --- -- Used to post the transaction to the DB --------------------------------------------------------------------
    def post_transaction_sql(self, statement):
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(statement)
            except Error:
                print(statement)
                print("Error Ledger 1: 297")
            finally:
                conn.close()
            self.disp_current_ledger()

    # --- -- Allows user to select a transaction for editing -----------------------------------------------------------
    def select_transaction(self):
        self.clear_inputs()
        inputText1 = "Select Row"
        inputText2 = "Enter Row #: "
        row = self.user_selection_input(self.widgetlist[1], inputText1, inputText2) - 1
        if row == -1:
            self.clear_inputs()
        else:
              for col in range(0, 10):
                widget = col + 2
                dataPoint = self.widgetlist[1].item(row, col).text()
                if widget == 2:
                    # col 0 = TDate
                    self.widgetlist[widget].setDate(QDate.fromString(dataPoint, "yyyy/MM/dd"))
                elif widget == 3:
                    # col 1 = TM
                    self.widgetlist[widget].setText(dataPoint)
                elif widget == 4:
                    # col 2 = TD
                    self.widgetlist[widget].setText(dataPoint)
                elif widget == 5:
                    # col 3 = Category
                    categoryIndex = self.widgetlist[widget].findText(dataPoint)
                    if categoryIndex >= 0:
                        self.widgetlist[widget].setCurrentIndex(categoryIndex)
                    else:
                        lostCategory = "You appear to have deleted that Category. \n\n" + \
                                       "Re-add that Category to select the desired entry.  \n\n" + \
                                       "In the future remove all instances of a given  \n" + \
                                       "Category prior to deleting it from your \n" + \
                                       "options list"
                        self.input_error_msg(lostCategory)
                        self.clear_inputs()
                        break
                elif widget == 6:
                    # col 4 = Amount
                    dataPoint = dataPoint[4:]
                    if dataPoint == "":
                        self.widgetlist[widget].setText(dataPoint)
                    elif dataPoint == " -  ":
                        self.widgetlist[widget].setText("0")
                    elif dataPoint[len(dataPoint) - 1:] == ")":
                        dataPoint = dataPoint[1:]
                        dataPoint = dataPoint[:len(dataPoint) - 1]
                        displayValue = remove_comma(dataPoint)
                        self.widgetlist[widget].setText(displayValue)
                    elif dataPoint[len(dataPoint) - 1:] == " ":
                        dataPoint = dataPoint[:len(dataPoint) - 1]
                        displayValue = remove_comma(dataPoint)
                        adjustment = widget + 1
                        self.widgetlist[adjustment].setText(displayValue)
                elif widget == 7:
                    pass
                elif widget == 8:
                    # col 6 = Status
                    adjustment = widget + 1
                    adjustment2 = widget + 2
                    if dataPoint == "Pending":
                        self.widgetlist[adjustment].setChecked(True)
                    elif dataPoint == "Posted":
                        self.widgetlist[adjustment2].setChecked(True)
                    else:
                        self.widgetlist[adjustment].setChecked(True)
                elif widget == 9:
                    # col 7 = Receipt
                    adjustment = widget + 2
                    self.widgetlist[adjustment].setText(dataPoint)
                elif widget == 10:
                    # col 8 = Note
                    adjustment = widget - 2
                    self.widgetlist[adjustment].setPlainText(dataPoint)
        return row

    # --- -- SQL Statement to update DB --------------------------------------------------------------------------------
    def update_sql(self, row):
        from datetime import datetime
        status = self.transaction_status(self.widgetlist[9], self.widgetlist[10])
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        modDebit = str(decimal_places(self.widgetlist[6].text(), 2))
        modCredit = str(decimal_places(self.widgetlist[7].text(), 2))
        currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        updateStatement = "Update " + modifiedLN \
                          + " SET Transaction_Date='" + self.widgetlist[2].date().toString("yyyy/MM/dd") \
                          + "', Transaction_Method='" + self.widgetlist[3].text() \
                          + "', Transaction_Description='" + self.widgetlist[4].text() \
                          + "', Category='" + self.widgetlist[5].currentText() \
                          + "', Debit='" + modDebit \
                          + "', Credit='" + modCredit \
                          + "', Note='" + self.widgetlist[8].toPlainText() \
                          + "', Status='" + status \
                          + "', Receipt='" + self.widgetlist[11].text() \
                          + "', Update_Date='" + currentDate \
                          + "' WHERE Post_Date='" + self.widgetlist[1].item(row, 9).text() + "'"
        self.post_transaction_sql(updateStatement)

    # --- -- Requests which row then updates to current inputs ---------------------------------------------------------
    def update_transaction(self):
        inputText1 = "Update Transaction"
        inputText2 = "Enter Row #: "
        if self.check_transactions() is True:
            row = self.user_selection_input(self.widgetlist[1], inputText1, inputText2) - 1
            if row == -1:
                self.clear_inputs()
            else:
                updateMessage = "Selecting 'OK' will update target row #: " + str(row + 1) + \
                                "\nto the current input values designated"
                reply = QMessageBox.warning(self, 'Verify', updateMessage, QMessageBox.Ok, QMessageBox.Cancel)
                if reply == QMessageBox.Ok:
                    self.update_sql(row)
                    self.clear_inputs()
                    self.disp_current_ledger()
                    ledgerValue = self.net_ledger_value()
                    self.ui.labelL1NV.setText(ledgerValue[1])
                    balanceStatement = "UPDATE Account_Summary SET Balance='" + ledgerValue[0] + "' WHERE ID='" + self.widgetlist[0].currentText() + "'"
                    specific_sql_statement(balanceStatement, self.refUserDB)
                    self.trigger_refresh()
                else:
                    pass
        else:
            input_error = """
                Transaction Input Instructions:

            1  :  (*) Denotes required input field
            2  :  Alphanumeric inputs only
            3  :  Check the character length of your
                  additional notes input

            """
            self.input_error_msg(input_error)

    # --- -- Requests which row then deletes and clears input ----------------------------------------------------------
    def delete_transaction(self):
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        inputText1 = "Delete Transaction"
        inputText2 = "Enter Row #: "
        row = self.user_selection_input(self.widgetlist[1], inputText1, inputText2) - 1
        deleteMessage = "Selecting 'OK' will permanently remove " + \
                        "\nrow #: " + str(row + 1) + " from the ledger"
        confirm = QMessageBox.warning(self, 'Confirm', deleteMessage, QMessageBox.Ok, QMessageBox.Cancel)
        if confirm == QMessageBox.Ok:
            deleteStatement = "DELETE FROM " + modifiedLN + " WHERE " \
                              + "Post_Date='" + self.widgetlist[1].item(row, 9).text() + "'"

            specific_sql_statement(deleteStatement, self.refUserDB)
            self.clear_inputs()
            self.disp_current_ledger()
            ledgerValue = self.net_ledger_value()
            self.ui.labelL1NV.setText(ledgerValue[1])
            balanceStatement = "UPDATE Account_Summary SET Balance='" + ledgerValue[0] + "' WHERE ID='" + self.widgetlist[0].currentText() + "'"
            specific_sql_statement(balanceStatement, self.refUserDB)
            self.trigger_refresh()
        else:
            pass

    # --- Fill ComboBoxes ----------------------------------------------------------------------------------------------
    def fill_combobox(self, combobox, col, tablename, coltwo, cat):
        sortTable = "SELECT " + col + " FROM " + tablename + " WHERE " + coltwo + "= '" + cat + "'"
        # ORDER BY " + col + " ASC LIMIT 0, 49999"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                conn.row_factory = lambda cursor, row: row[0]
                cur = conn.cursor()
                cur.execute(sortTable)
                comboTuple = cur.fetchall()
        except Error:
            print("Error Ledger: 470")
        finally:
            conn.close()
            combobox.addItems(comboTuple)
            combobox.model().sort(0)
            combobox.setCurrentIndex(0)

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------Functions Associated with the Ledger Frames and the values                                            ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Sets frameRight - Label NetValue --------------------------------------------------------------------------
    def net_ledger_value(self):
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        if ledgerName == "":
            netValue = ["0.00", "0.00"]
            return netValue
        else:
            netValueStatement = "SELECT SUM(Credit - Debit) FROM " + modifiedLN
            qtyMoney = obtain_sql_value(netValueStatement, self.refUserDB)
            if qtyMoney[0] is None:
                qtyMoney = "$ 0.00"
                moneylist = [qtyMoney, qtyMoney]
                return moneylist
            elif qtyMoney[0] < 0:
                moneyWComma = add_comma(qtyMoney[0], 2)
                moneyWOComma = "-" + remove_comma(moneyWComma)
                formatString = "($ " + moneyWComma + ")"
                moneylist = [moneyWOComma, formatString]
                return moneylist
            else:
                moneyWComnma = add_comma(qtyMoney[0], 2)
                moneyWOComma = remove_comma(moneyWComnma)
                formatString = "$ " + moneyWComnma
                moneylist = [moneyWOComma, formatString]
                return moneylist

    # --- -- Sets frameMiddle - labelVariable1B ------------------------------------------------------------------------
    def set_variable1B(self):
        detailsTable = self.parentType_dict[self.parentType]
        setInterest = ["Bank", "CD", "Treasury", "Debt"]
        setCreditLimit = ["Credit"]
        if self.parentType in setInterest:
            interestStatement = "SELECT Interest_Rate FROM " + detailsTable + " WHERE Account_Name='" + self.widgetlist[0].currentText() + "'"
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(interestStatement)
                    interest = cur.fetchone()
            except Error:
                print("Error Ledger: 523")
            finally:
                conn.close()
            if interest is None:
                interest = "Unknown"
            else:
                interest = str(decimal_places(interest[0], 2))
                interest = interest + "%"
            self.ui.labelVariable1B.setText(interest)
        elif self.parentType in setCreditLimit:
            limitStatement = "SELECT Credit_Limit FROM " + detailsTable + " WHERE Account_Name='" + self.widgetlist[0].currentText() + "'"
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(limitStatement)
                    limit = cur.fetchone()
            except Error:
                print("Error Ledger: 541")
            finally:
                conn.close()
            if limit is None:
                limit = [0.00]
            limit = add_comma(limit[0], 2)
            limit = "$ " + limit
            self.ui.labelVariable1B.setText(limit)
        else:
            pass

    # --- -- Sets frameRight - labelVariable2B -------------------------------------------------------------------------
    def set_variable2B(self):
        detailsTable = self.parentType_dict[self.parentType]
        setMaturity = ["CD", "Treasury"]
        setStart = ["Debt"]
        if self.parentType in setMaturity:
            maturityStatement = "SELECT Maturity_Date FROM " + detailsTable + " WHERE Account_Name='" + self.widgetlist[0].currentText() + "'"
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(maturityStatement)
                    maturity = cur.fetchone()
            except Error:
                print("Error Ledger: 566")
            finally:
                conn.close()
            if maturity is None:
                maturity = ["Unknown"]
            self.ui.labelVariable2B.setText(maturity[0])
        elif self.parentType in setStart:
            StartStatement = "SELECT Starting_Balance FROM " + detailsTable + " WHERE Account_Name='" + self.widgetlist[0].currentText() + "'"
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(StartStatement)
                    startingBalance = cur.fetchone()
            except Error:
                print("Error Ledger: 581")
            finally:
                conn.close()
            if startingBalance is None:
                startingBalance = [0]
            sBalance = add_comma(startingBalance[0], 2)
            sBalance = "$ " + sBalance
            self.ui.labelVariable2B.setText(sBalance)
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------Functions Associated with Receipts/invoices                                                           ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Button function to initiate upload-------------------------------------------------------------------------
    def upload_receipt_button(self):
        if self.widgetlist[0].currentText() == "":
            noLedger_msg = "Create a New Ledger"
            self.input_error_msg(noLedger_msg)
        elif self.widgetlist[11].text() != "":
            replace_message = """
            DELETE or CLEAR the receipt before uploading a new one.    
            """
            present = QMessageBox.information(self, 'A Receipt Already Exists', replace_message, QMessageBox.Ok)
            if present == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            self.upload_receipt_action()

    # --- -- Upload Image into the ledger -----------------------------------------------------------------------------
    def upload_receipt_action(self):
        suffixlist = ['.jpg', '.jpeg', 'JPEG', '.gif', '.pdf', '.png']
        rname, _ = QFileDialog.getOpenFileName(self, 'Target Receipt', '/home',
                                               'Images (*.png *.jpg  *.jpeg *.gif);; PDF (*.pdf)')
        if rname:
            rname_path = Path(rname)
            suffix = PurePath(rname_path).suffix
            if suffix not in suffixlist:
                wrongType = "Sorry, those files types are not support yet."
                self.input_error_msg(wrongType)
            else:
                nRName = self.rename_image() + str(suffix)
                nRName_path = Path(receipt_pathway(self.parentType, self.widgetlist[0].currentText(), nRName,
                                                   self.refUser))
                nRName_path = Path.cwd() / nRName_path
                copy(rname_path, nRName_path)
                self.widgetlist[11].setText(nRName)
        else:
            self.widgetlist[11].setText("")

    # --- -- Clear Receipt Name from LineEdit --------------------------------------------------------------------------
    def clear_receipt_action(self):
        if self.widgetlist[11].text() == "":
            pass
        else:
            oRName = self.widgetlist[11].text()
            self.widgetlist[11].setText("")
            rowList = self.find_mult_row(7, oRName)
            # if no rows are found with the file. The image is just deleted
            if len(rowList) == 0:
                self.widgetlist[11].setText("")
                oRName_path = Path(receipt_pathway(self.parentType, self.widgetlist[0].currentText(), oRName, self.refUser))
                oRName_path = Path.cwd() / oRName_path
                os.remove(oRName_path)
            # If >= 1 row is found with the file name. Then the lineEdit is just cleared
            else:
                self.widgetlist[11].setText("")

    # --- -- Delete Receipt From Records--------------------------------------------------------------------------------
    def delete_receipt_action(self):
        if self.widgetlist[11].text() == "":
            pass
        else:
            row = self.find_mult_row(7, self.widgetlist[11].text())
            if len(row) == 0:
                self.clear_receipt_action()
            elif len(row) >= 1:
                target_row = self.select_transaction()
                self.clear_receipt_action()
                self.update_sql(target_row)
            else:
                self.clear_receipt_action()

    # --- -- Delete Unwanted Receipts upon close -----------------------------------------------------------------------
    def receipt_check_on_close(self):
        if self.widgetlist[11].text() != "":
            self.clear_receipt_action()

    # --- -- Finds the row in the QTableWidget for a given String ------------------------------------------------------
    def find_row(self, col_num, string):
        allrows = self.widgetlist[1].rowCount() + 1
        for row in range(allrows):
            cell = self.widgetlist[1].item(row, col_num).text()
            if cell == string:
                return row

    def find_mult_row(self, col_num, string):
        allrows = self.widgetlist[1].rowCount()
        rowList = []
        for row in range(allrows):
            cell = self.widgetlist[1].item(row, col_num).text()
            if cell == string:
                rowList.append(cell)
        return rowList

    # --- -- Rename the Image File -------------------------------------------------------------------------------------
    def rename_image(self):
        from datetime import datetime
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        category = self.widgetlist[5].currentText()
        currentDate = datetime.now().strftime("%y%j%H%M%S")
        newImageName = modifiedLN[:5] + " - " + category + " - " + currentDate
        return newImageName

    # --- -- Display jpeg, gif, png images -----------------------------------------------------------------------------
    def display_receipt(self):
        ledger = self.widgetlist[0].currentText()
        fileName = self.widgetlist[11].text()
        suffix = PurePath(fileName).suffix
        pathway = receipt_pathway(self.parentType, ledger, fileName, self.refUser)
        pathway = Path.cwd() / pathway
        if fileName == "":
            noReceipt = "Sorry, No Receipt Uploaded"
            self.input_error_msg(noReceipt)
        elif suffix == ".pdf":
            os.startfile(pathway)
        else:
            ion = Receipt(str(pathway), fileName)
            if ion.exec_() == QDialog.Accepted:
                pass

    # --- PyQt5 signal to refresh QMainWindow Label for NetWorth -------------------------------------------------------
    def trigger_refresh(self):
        self.refresh_signal.emit("1")

    def trigger_del_tab(self):
        self.remove_tab.emit(self.parentType)

    def closeEvent(self, event):
        event.ignore()
        self.receipt_check_on_close()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = LedgerV1('781i205l4ly.db', "Treasury")
    lily.show()
    sys.exit(app.exec_())
