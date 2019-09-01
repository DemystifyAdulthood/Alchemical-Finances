# Ledger Design for Bank, CD, TB, Cash, Debt, Credit Card
# Structured to allow for future modification for other uses.

import sys
import sqlite3
import os


from PyQt5.QtWidgets import QMessageBox, QDialog, QInputDialog, QFileDialog, QApplication
from PyQt5.QtCore import QDate
from PyQt5 import QtCore, QtWidgets
from sqlite3 import Error
from pathlib import Path, PurePath
from shutil import copy
from AccountsDialog import Accounts
from CategoriesDialog import TransactionForm
from Receipt import Receipt
from Ledger2Ui import Ui_Dialog
from UPK import receipt_pathway, obtain_sql_value, modify_for_sql, check_characters, specific_sql_statement,\
    decimal_places, add_comma, remove_comma, disp_ledgerV2
from StyleSheets import uFrameStyleSheet, uTitleStyleSheet


class LedgerV2(QDialog):
    refresh_signal_L2 = QtCore.pyqtSignal(str)
    remove_tab_L2 = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, database, parentType, user):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parentType)
        self.show()

        # --- Class Global Variables -----------------------------------------------------------------------------------
        self.refUserDB = database
        self.parentType = parentType
        self.refUser = user

        self.widgetlist = [self.ui.comboBoxL2, self.ui.tableWidgetL2, self.ui.dateEditL2,
                           self.ui.lineEditL2TD, self.ui.comboBoxL2C, self.ui.lineEditL2Debit,
                           self.ui.lineEditL2Credit, self.ui.lineEditL2Purchase, self.ui.lineEditL2Sold,
                           self.ui.textEditL2Notes, self.ui.radioButtonL2Pending, self.ui.radioButtonL2Posted,
                           self.ui.lineEditReceiptL2, self.ui.lineEditL2Price]
        # 11 widgets
        self.buttonlist = [self.ui.pushButtonNewL2, self.ui.pushButtonCatL2, self.ui.pushButtonUploadL2,
                           self.ui.pushButtonDisplayL2, self.ui.pushButtonAddL2, self.ui.pushButtonSelectL2,
                           self.ui.pushButtonUpdateL2, self.ui.pushButtonDeleteL2, self.ui.pushButtonClearL2,
                           self.ui.pushButtonUpdatePriceL2, self.ui.pushButtonRClearL2, self.ui.pushButtonRDeleteL2,
                           self.ui.pushButtonSearchL1, self.ui.pushButtonDispRangL1]

        self.parentType_dict = {"Bank": "Bank_Account_Details", "Equity": "Equity_Account_Details",
                                "Retirement": "Retirement_Account_Details", "CD": "CD_Account_Details",
                                "Treasury": "Treasury_Account_Details", "Debt": "Debt_Account_Details",
                                "Credit": "Credit_Account_Details", "Cash": "Cash_Account_Details"}

        # --- Prepare Widgets for use ----------------------------------------------------------------------------------
        self.fill_combobox(self.widgetlist[0], "ID", "Account_Summary", "ParentType", self.parentType)
        self.fill_combobox(self.widgetlist[4], "Method", "Categories", "ParentType", self.parentType)

        self.ui.frameLeft.setStyleSheet(uFrameStyleSheet)
        self.ui.frameMiddle.setStyleSheet(uFrameStyleSheet)
        self.ui.frameRight.setStyleSheet(uFrameStyleSheet)
        self.ui.labelStaticL12.setStyleSheet(uTitleStyleSheet)
        self.ui.labelL2NV.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable1A.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable1B.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable2A.setStyleSheet(uTitleStyleSheet)
        self.ui.labelVariable2B.setStyleSheet(uTitleStyleSheet)

        # --- Ledger Button Functions ----------------------------------------------------------------------------------
        # --- -- Prepares Functionality of the Ledger Variant 1 --------------------------------------------------------
        self.widgetlist[0].currentIndexChanged.connect(self.disp_current_ledger)    # Account Combobox
        self.buttonlist[0].clicked.connect(self.accounts_dialog)                    # Modify Button Account Combobox
        self.buttonlist[1].clicked.connect(self.categories_dialog)                  # Modify Button Category Combobox
        self.buttonlist[2].clicked.connect(self.upload_receipt_button)              # Upload Receipt Button
        self.buttonlist[3].clicked.connect(self.display_receipt)                    # Display Receipt Button
        self.buttonlist[4].clicked.connect(self.add_transaction)                    # Add Transaction Button
        self.buttonlist[5].clicked.connect(self.select_transaction)                 # Select Transaction Button
        self.buttonlist[6].clicked.connect(self.update_transaction)                 # Update Transaction Button
        self.buttonlist[7].clicked.connect(self.delete_transaction)                 # Delete Transaction Button
        self.buttonlist[8].clicked.connect(self.clear_inputs)                       # Clear Transaction Button
        self.buttonlist[9].clicked.connect(self.update_ticker_price)
        self.widgetlist[2].setDate(QDate.currentDate())                             # DateEdit Widget
        self.widgetlist[10].setChecked(True)                                        # Pending RadioButton
        self.buttonlist[10].clicked.connect(self.clear_receipt_action)               # Clear Receipt Input
        self.buttonlist[11].clicked.connect(self.delete_receipt_action)             # Delete Receipt

        self.buttonlist[12].hide()
        self.buttonlist[13].hide()

        self.tickerPrice = self.obtain_ticker_price()
        self.ui.labelVariable2B.setText("$ " + self.tickerPrice)
        self.disp_current_ledger()

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
            self.disp_current_ledger()
            self.trigger_refresh()

    # --- -- Creates Modal QDialog for User to Modify Category List ----------------------------------------------------
    def categories_dialog(self):
        molly = TransactionForm(self.refUserDB, self.parentType)
        if molly.exec_() == QDialog.Accepted:
            self.widgetlist[4].clear()
            self.fill_combobox(self.widgetlist[4], "Method", "Categories", "ParentType", self.parentType)

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------General Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Determines the status of the transaction and turns it into a string ---------------------------------------
    def tranaction_status(self, status1, status2):
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
        listA = [3, 13]
        listB = [5, 6, 7, 8, 13]
        for widget in listA:
            if check_characters(self.widgetlist[widget].text()) is False:
                return False  # Input Has Non Alphanumeric characters
            elif self.widgetlist[widget].text() == "" or self.widgetlist[widget].text() == " ":
                return False  # Input is Blank
            else:
                continue
        for widget in listB:
            if check_characters(self.widgetlist[widget].text()) is False:
                return False  # Debit is a non alphanumeric character
            else:
                continue
        if check_characters(self.widgetlist[9].toPlainText()) is False:
            return False  # Notes Has Non Alphanumeric characters
        elif len(self.widgetlist[9].toPlainText()) > 150:
            return False  # Limit the Additional Notes field
        elif self.check_numerical_inputs(self.widgetlist[5].text()) is True and self.check_numerical_inputs(
                self.widgetlist[6].text()) is True:
            return False  # Simultaneous Credit and Debit inputs
        elif self.check_numerical_inputs(self.widgetlist[7].text()) is True and self.check_numerical_inputs(
                self.widgetlist[8].text()) is True:
            return False  # Simultaneous Credit and Debit inputs
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
        self.widgetlist[4].setCurrentIndex(0)
        self.widgetlist[5].setText("")
        self.widgetlist[6].setText("")
        self.widgetlist[7].setText("")
        self.widgetlist[8].setText("")
        self.widgetlist[9].setPlainText("")
        self.widgetlist[10].setChecked(True)
        self.clear_receipt_action()
        self.widgetlist[13].setText("")
        self.widgetlist[3].setFocus()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------SQLite Based Functions                                                                                ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Displays the current ledger // Also refreshes ledger when updated -----------------------------------------
    def disp_current_ledger(self):
        disp_ledgerV2(self.widgetlist[0], self.widgetlist[1], self.refUserDB)
        ledgerValue = self.net_ledger_value()
        self.ui.labelL2NV.setText(ledgerValue[1])
        self.ui.labelVariable1B.setText(self.net_share_balance())
        self.tickerPrice = self.obtain_ticker_price()
        self.ui.labelVariable2B.setText("$ " + self.tickerPrice)

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
                modDebit = decimal_places(self.widgetlist[5].text(), 2)
                modCredit = decimal_places(self.widgetlist[6].text(), 2)
                modPurchased = decimal_places(self.widgetlist[7].text(), 4)
                modSold = decimal_places(self.widgetlist[8].text(), 4)
                modPrice = decimal_places(self.widgetlist[13].text(), 4)
                status = self.tranaction_status(self.widgetlist[10], self.widgetlist[11])
                currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                # 2- date -- 3- T Description -- 4- Category -- 5- Debit
                # 6- credit -- 8- sold -- 7- Purchased -- 10/11- Status -- ## - UserDate -- 12- Receipt
                addStatement = "INSERT INTO " + modifiedLN + " VALUES('"\
                               + self.widgetlist[2].date().toString("yyyy/MM/dd") + "', '"\
                               + self.widgetlist[3].text() + "', '"\
                               + self.widgetlist[4].currentText() + "', '"\
                               + str(modDebit) + "', '"\
                               + str(modCredit) + "', '"\
                               + str(modSold) + "', '"\
                               + str(modPurchased) + "', '" \
                               + str(modPrice) + "', '" \
                               + self.widgetlist[9].toPlainText() + "', '"\
                               + status + "', '"\
                               + self.widgetlist[12].text() + "', '"\
                               + currentDate + "', '"\
                               + currentDate + "')"
                self.post_transaction_sql(addStatement)
                ledgerValue = self.net_ledger_value()
                self.ui.labelL2NV.setText(ledgerValue[1])
                self.ui.labelVariable1B.setText(self.net_share_balance())
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
                print("error: 317")
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
              for col in range(0, 9):
                widget = col + 2
                dataPoint = self.widgetlist[1].item(row, col).text()
                if widget == 2:
                    # col 0 = T Date
                    self.widgetlist[widget].setDate(QDate.fromString(dataPoint, "yyyy/MM/dd"))
                elif widget == 3:
                    # col 1 = T Description
                    self.widgetlist[widget].setText(dataPoint)
                elif widget == 4:
                    # col 2 = Category
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
                elif widget == 5:
                    # col 3 = Amount
                    dataPoint = dataPoint[4:]
                    if dataPoint == "":
                        self.widgetlist[widget].setText(dataPoint)
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
                elif widget == 6:
                    # col 4 = Shares (+/-)
                    purchasedwidget = widget + 1
                    soldwidget = widget + 2
                    if dataPoint == "":
                        self.widgetlist[purchasedwidget].setText(dataPoint)
                    elif dataPoint[:1] == "-":
                        dataPoint = dataPoint[1:]
                        noCommaValue = remove_comma(dataPoint)
                        self.widgetlist[soldwidget].setText(noCommaValue)
                    elif dataPoint[:1] != "-":
                        noCommaValue = remove_comma(dataPoint)
                        self.widgetlist[purchasedwidget].setText(noCommaValue)
                elif widget == 7:
                    # col 5 = Price/Share
                    priceadjustment = widget + 6
                    if dataPoint == "":
                        self.widgetlist[priceadjustment].setText(dataPoint)
                    elif dataPoint[:2] == " $":
                        dataPoint = dataPoint[3:len(dataPoint)-1]
                        noCommaValue = str(remove_comma(dataPoint))
                        self.widgetlist[13].setText(noCommaValue)
                elif widget == 8:
                    # col 6 = Status
                    pendadjustment = widget + 2
                    postadjustment = widget + 3
                    if dataPoint == "Pending":
                        self.widgetlist[pendadjustment].setChecked(True)
                    elif dataPoint == "Posted":
                        self.widgetlist[postadjustment].setChecked(True)
                    else:
                        self.widgetlist[pendadjustment].setChecked(True)
                elif widget == 9:
                    # col 7 = Receipt
                    receiptadjustment = widget + 3
                    self.widgetlist[receiptadjustment].setText(dataPoint)
                elif widget == 10:
                    # col 8 = Note
                    notesadjustment = widget - 1
                    self.widgetlist[notesadjustment].setPlainText(dataPoint)
        return row

    # --- -- SQL Statement to update DB --------------------------------------------------------------------------------
    def update_sql(self, row):
        from datetime import datetime
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        modDebit = str(decimal_places(self.widgetlist[5].text(), 2))
        modCredit = str(decimal_places(self.widgetlist[6].text(), 2))
        modPurchased = str(decimal_places(self.widgetlist[7].text(), 4))
        modSold = str(decimal_places(self.widgetlist[8].text(), 4))
        modPrice = str(decimal_places(self.widgetlist[13].text(), 4))
        status = self.tranaction_status(self.widgetlist[10], self.widgetlist[11])
        currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        updateStatement = "Update " + modifiedLN \
                          + " SET Transaction_Date='" + self.widgetlist[2].date().toString("yyyy/MM/dd") \
                          + "', Transaction_Description='" + self.widgetlist[3].text() \
                          + "', Category='" + self.widgetlist[4].currentText() \
                          + "', Debit='" + modDebit \
                          + "', Credit='" + modCredit \
                          + "', Sold='" + modSold \
                          + "', Purchased='" + modPurchased \
                          + "', Price='" + modPrice \
                          + "', Note='" + self.widgetlist[9].toPlainText() \
                          + "', Status='" + status \
                          + "', Receipt='" + self.widgetlist[12].text() \
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
                    ledgerValue = self.net_ledger_value()
                    self.ui.labelL2NV.setText(ledgerValue[1])
                    self.ui.labelVariable1B.setText(self.net_share_balance())
                    balanceStatement = "UPDATE Account_Summary SET Balance='" + ledgerValue[0] + "' WHERE ID='" + \
                                       self.widgetlist[0].currentText() + "'"
                    specific_sql_statement(balanceStatement, self.refUserDB)
                    self.clear_inputs()
                    self.disp_current_ledger()
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
            self.ui.labelL2NV.setText(ledgerValue[1])
            self.ui.labelVariable1B.setText(self.net_share_balance())
            balanceStatement = "UPDATE Account_Summary SET Balance='" + ledgerValue[0] + "' WHERE ID='" + self.widgetlist[0].currentText() + "'"
            specific_sql_statement(balanceStatement, self.refUserDB)
            self.trigger_refresh()
        else:
            pass

    # --- Update Stock Price -------------------------------------------------------------------------------------------
    def update_ticker_price(self):
        tickerPrice = self.get_ticker_price()
        tickerPrice = decimal_places(tickerPrice, 4)
        tickerUpdate = "UPDATE " + self.parentType_dict[self.parentType] + " SET Stock_Price='" + str(tickerPrice) \
                       + "' WHERE Account_Name='" + self.widgetlist[0].currentText() + "'"
        updateLedgerValue = tickerPrice * decimal_places(self.ui.labelVariable1B.text(), 4)
        balanceUpdate = "UPDATE Account_Summary SET Balance='" + str(updateLedgerValue) + "' WHERE ID='" + self.widgetlist[0].currentText() + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(tickerUpdate)
                cur.execute(balanceUpdate)
        finally:
            conn.close()
        newledgerValue = self.net_ledger_value()
        self.ui.labelL2NV.setText(newledgerValue[1])
        self.ui.labelVariable2B.setText("$ " + str(tickerPrice))
        self.trigger_refresh()

    # --- Update Stock Price -------------------------------------------------------------------------------------------
    def refresh_ticker_price(self):
        tickerUpdate = "SELECT Stock_Price FROM " + self.parentType_dict[self.parentType] + " WHERE Account_Name='" + self.widgetlist[0].currentText() + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(tickerUpdate)
                tickerPrice = cur.fetchone()
                updateLedgerValue = decimal_places(tickerPrice[0], 4) * decimal_places(self.ui.labelVariable1B.text(), 4)
                updateLedgerValue = decimal_places(updateLedgerValue, 2)
                balanceUpdate = "UPDATE Account_Summary SET Balance='" + str(updateLedgerValue) + "' WHERE ID='" + \
                                self.widgetlist[0].currentText() + "'"
                cur.execute(balanceUpdate)
        finally:
            conn.close()
        newledgerValue = self.net_ledger_value()
        self.ui.labelL2NV.setText(newledgerValue[1])
        self.ui.labelVariable2B.setText("$ " + str(decimal_places(tickerPrice[0], 4)))
        self.trigger_refresh()

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
            self.statusBar().showMessage("Error Ledger2: 521")
        finally:
            conn.close()
            combobox.addItems(comboTuple)
            combobox.model().sort(0)
            combobox.setCurrentIndex(0)

    # --- -- Set Label for Net Share Balance of Active Ledger ----------------------------------------------------------
    def net_share_balance(self):
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        if ledgerName == "":
            shareBalance = "0.0000"
            return shareBalance
        else:
            netSBalance = "SELECT SUM(Purchased - Sold) FROM " + modifiedLN
            shareBalance = obtain_sql_value(netSBalance, self.refUserDB)
            if shareBalance[0] is None:
                shareBalance = "0.0000"
                return shareBalance
            elif shareBalance[0] < 0:
                shareBalance = "ERROR <0"
                return shareBalance
            else:
                formatedShares = decimal_places(shareBalance[0], 4)
                formatedStrShares = str(formatedShares)
                return formatedStrShares

    # --- -- Set Label for Net Value of Active Ledger ------------------------------------------------------------------
    def net_ledger_value(self):
        ledgerName = self.widgetlist[0].currentText()
        modifiedLN = modify_for_sql(ledgerName)
        if ledgerName == "":
            netValue = ["0.00", "0.00"]
            return netValue
        else:
            netValueStatement = "SELECT SUM(Purchased - Sold) FROM " + modifiedLN
            qtyShares = obtain_sql_value(netValueStatement, self.refUserDB)
            if qtyShares[0] is None:
                netValue = "0.00"
                return netValue
            elif qtyShares[0] < 0:
                moneyWComma = add_comma(qtyShares[0], 2)
                moneyWOComma = "-" + remove_comma(moneyWComma)
                formatString = "($ " + moneyWComma + ")"
                moneylist = [moneyWOComma, formatString]
                return moneylist
            else:
                self.tickerPrice = self.obtain_ticker_price()
                accountValue = decimal_places(self.tickerPrice, 4) * decimal_places(qtyShares[0], 4)
                moneyWComnma = add_comma(accountValue, 4)
                moneyWOComma = remove_comma(moneyWComnma)
                formatString = "$ " + moneyWComnma
                moneylist = [moneyWOComma, formatString]
                return moneylist

    # --- Returns the existing Ticker Price from the Account Details Page ----------------------------------------------
    def obtain_ticker_price(self):
        tickerPriceStatement = "SELECT Stock_Price FROM " + self.parentType_dict[self.parentType] +\
                                    " WHERE Account_Name ='" + self.widgetlist[0].currentText() + "'"
        tickerPrice = obtain_sql_value(tickerPriceStatement, self.refUserDB)
        if tickerPrice is None:
            tickerPrice = "Unknown"
        else:
            tickerPrice = str(decimal_places(tickerPrice[0], 4))
        return tickerPrice

    # --- User Input Function to obtain a new ticker Price -------------------------------------------------------------
    def get_ticker_price(self):
        price, ok = QInputDialog.getDouble(self, "Ticker Price", "Market Price:", 1.0000, 0, 1000000, 4)
        if ok and price != "":
            return price
        else:
            price = "1.0000"
            return price

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
        elif self.widgetlist[12].text() != "":
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
        suffixlist = ['.jpg', '.jpeg', 'JPEG', '.gif', '.pdf']
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
                nRName_path = Path(receipt_pathway(self.parentType, self.widgetlist[0].currentText(), nRName, self.refUser))
                nRName_path = Path.cwd() / nRName_path
                copy(rname_path, nRName_path)
                self.widgetlist[12].setText(nRName)
        else:
            self.widgetlist[12].setText("")

    # --- -- Clear Receipt Name from LineEdit --------------------------------------------------------------------------
    def clear_receipt_action(self):
        if self.widgetlist[12].text() == "":
            pass
        else:
            oRName = self.widgetlist[11].text()
            self.widgetlist[12].setText("")
            rowList = self.find_mult_row(6, oRName)
            # if no rows are found with the file. The image is just deleted
            if len(rowList) == 0:
                self.widgetlist[11].setText("")
                oRName_path = Path(receipt_pathway(self.parentType, self.widgetlist[0].currentText(), oRName, self.refUser))
                oRName_path = Path.cwd() / oRName_path
                os.remove(oRName_path)
            # If >= 1 row is found with the file name. Then the lineEdit is just cleared
            else:
                self.widgetlist[12].setText("")

    # --- -- Delete Receipt From Records--------------------------------------------------------------------------------
    def delete_receipt_action(self):
        if self.widgetlist[12].text() == "":
            pass
        else:
            row = self.find_mult_row(6, self.widgetlist[11].text())
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
        if self.widgetlist[12].text() != "":
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
        category = self.widgetlist[4].currentText()
        currentDate = datetime.now().strftime("%y%j%H%M%S")
        newImageName = modifiedLN[:5] + " - " + category + " - " + currentDate
        return newImageName

    # --- -- Display jpeg, gif, png images -----------------------------------------------------------------------------
    def display_receipt(self):
        ledger = self.widgetlist[0].currentText()
        fileName = self.widgetlist[12].text()
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
        self.refresh_signal_L2.emit("1")

    # --- PyQt5 signal to remove ParentType Ledger from tabdic ---------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_L2.emit(self.parentType)

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = LedgerV2('781i205l4ly.db', "Equity")
    lily.show()
    sys.exit(app.exec_())
