# This QDialog was designed to allow user to input new accounts with details.
# Admittedly the details are only accessible in this dialog at this point in time.

import sys
import sqlite3
import os

from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QListWidgetItem
from PyQt5 import QtCore, QtWidgets
from sqlite3 import Error
from AccountsDialogUi import Ui_Dialog
from Question import ATypeQuestion
from UPK import check_characters, modify_for_sql, find_character, first_character_check, decimal_places,\
    switch_sql_tables, directory_pathway, check_characters_login
from StyleSheets import UniversalStyleSheet, generalError


class Accounts(QDialog):
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, dbname, parentType, user):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ Class Global Variables                                                                           ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        self.refUserDB = dbname
        self.parentType = parentType
        self.refUser = user

        self.parentType_dict = {"Bank": "Bank_Account_Details", "Equity": "Equity_Account_Details",
                                "Retirement": "Retirement_Account_Details", "CD": "CD_Account_Details",
                                "Treasury": "Treasury_Account_Details", "Debt": "Debt_Account_Details",
                                "Credit": "Credit_Account_Details", "Cash": "Cash_Account_Details"}

        self.accountDTable = self.parentType_dict[self.parentType]

        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ QDialog Functionality and initial Appearance                                                     ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        self.ui.pushButtonModify.hide()
        self.ui.pushButtonNew.clicked.connect(self.new_account)
        self.ui.pushButtonDelete.clicked.connect(self.delete_account)
        self.ui.pushButtonEdit.clicked.connect(self.edit_account)
        self.ui.pushButtonSubmit.clicked.connect(self.submit_account)
        self.ui.pushButtonModify.clicked.connect(self.submit_edit)
        self.ui.pushButtonMod.clicked.connect(self.type_modifier)
        self.ui.pushButtonArchive.clicked.connect(self.archive_account)
        self.fill_widget(self.ui.comboBoxATypes, "SubType", "AccountSubType", "ParentType")
        self.fill_widget(self.ui.listWidgetAccount, "ID", "Account_Summary", "ParentType")
        self.ui.listWidgetAccount.setCurrentRow(0)
        self.disp_current_selection()
        self.ui.listWidgetAccount.itemClicked.connect(self.disp_current_selection)
        self.ui.listWidgetAccount.itemClicked.connect(self.disable_widgets)
        self.show()
        self.setStyleSheet(UniversalStyleSheet)
        self.initial_appearance()

    def initial_appearance(self):
        if self.parentType == "Bank":
            self.ui.labelVariable2.hide()
            self.ui.lineEditVariable2.hide()
            self.resize(400, 420)
            self.setMinimumSize(QtCore.QSize(400, 420))
            self.setMaximumSize(QtCore.QSize(400, 420))
            self.ui.pushButtonSubmit.setGeometry(QtCore.QRect(257, 380, 125, 25))
            self.ui.pushButtonModify.setGeometry(QtCore.QRect(257, 380, 125, 25))
            self.ui.labelError.setGeometry(QtCore.QRect(30, 380, 211, 25))
        elif self.parentType == "Cash":
            self.ui.labelVariable1.hide()
            self.ui.labelVariable2.hide()
            self.ui.lineEditVariable1.hide()
            self.ui.lineEditVariable2.hide()
            self.resize(400, 390)
            self.setMinimumSize(QtCore.QSize(400, 390))
            self.setMaximumSize(QtCore.QSize(400, 390))
            self.ui.pushButtonSubmit.setGeometry(QtCore.QRect(257, 350, 125, 25))
            self.ui.pushButtonModify.setGeometry(QtCore.QRect(257, 350, 125, 25))
            self.ui.labelError.setGeometry(QtCore.QRect(30, 350, 211, 25))
        elif self.parentType == "CD" or self.parentType == "Treasury":
            pass
        elif self.parentType == "Credit":
            self.ui.labelVariable1.setText("Credit Limit")
            self.ui.labelVariable2.hide()
            self.ui.lineEditVariable2.hide()
            self.resize(400, 420)
            self.setMinimumSize(QtCore.QSize(400, 420))
            self.setMaximumSize(QtCore.QSize(400, 420))
            self.ui.pushButtonSubmit.setGeometry(QtCore.QRect(257, 380, 125, 25))
            self.ui.pushButtonModify.setGeometry(QtCore.QRect(257, 380, 125, 25))
            self.ui.labelError.setGeometry(QtCore.QRect(30, 380, 211, 25))
        elif self.parentType == "Debt":
            self.ui.labelVariable2.setText("Starting Balance")
        else:  # Equity and Retirement
            self.ui.labelVariable1.setText("Ticker Symbol")
            self.ui.labelVariable2.setText("Ticker Price")

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ Button Functions                                                                                     ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- Activates widgets to allow user to add a new account ---------------------------------------------------------
    def new_account(self):
        self.disable_widgets()
        self.enable_widgets()
        self.clear_widgets()

    # --- Deletes the ccount from the User's  Database -----------------------------------------------------------------
    def delete_account(self):
        question = "Are you sure you want to delete this account?"
        reply = QMessageBox.question(self, "Confirmation", question, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_account_sql(self.ui.lineEditAccount.text())
            self.ui.listWidgetAccount.clear()
            self.fill_widget(self.ui.listWidgetAccount, "ID", "Account_Summary", "ParentType")
            self.clear_widgets()
            self.ui.listWidgetAccount.setCurrentRow(0)
            self.disp_current_selection()
        else:
            pass

    # --- Enables the user to edit an accounts details -----------------------------------------------------------------
    def edit_account(self):
        self.ui.pushButtonSubmit.hide()
        self.enable_widgets()
        self.ui.pushButtonSubmit.setEnabled(False)
        self.ui.pushButtonModify.show()
        self.ui.pushButtonModify.setEnabled(True)

    # --- Submits the Changes to the database --------------------------------------------------------------------------
    # --- -- Also checks the information to ensure safe for SQL --------------------------------------------------------
    def submit_account(self):
        accountName = self.ui.lineEditAccount.text()
        accountSubType = self.ui.comboBoxATypes.currentText()
        accountOwner = self.ui.lineEditPrimary.text()
        accountBank = self.ui.lineEditBank.text()
        accountVariable1 = self.ui.lineEditVariable1.text()
        accountVariable2 = self.ui.lineEditVariable2.text()
        checkStatement1 = "SELECT Account_Name FROM " + self.accountDTable + " Where Account_Name ='" + accountName + "'"
        checkStatement2 = "SELECT ID FROM Account_Summary Where ID ='" + accountName + "'"
        oneVariable = ["Bank", "Credit"]
        bothVariable = ["CD", "Treasury", "Debt", "Equity", "Retirement"]
        if accountName == "" or accountOwner == "" or accountBank == "":
            self.ui.labelError.setText("Do Not Leave a Field Blank")
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
            self.ui.lineEditPrimary.setStyleSheet(generalError)
            self.ui.lineEditBank.setStyleSheet(generalError)
            self.ui.lineEditVariable1.setStyleSheet(generalError)
            self.ui.lineEditVariable2.setStyleSheet(generalError)
        elif len(accountName) >= 38:
            self.ui.labelError.setText("Try a Nickname for your Account")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
        elif find_character(accountName) is False\
                or find_character(accountOwner) is False\
                or find_character(accountBank) is False:
            self.ui.labelError.setText("Do Not Leave a Field Blank")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
            self.ui.lineEditPrimary.setStyleSheet(generalError)
            self.ui.lineEditBank.setStyleSheet(generalError)
        elif first_character_check(accountName) is False:
            self.ui.labelError.setText("Start Account Name with Letter")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
        elif check_characters(accountName) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
        elif check_characters(accountSubType) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
        elif check_characters(accountOwner) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditPrimary.setStyleSheet(generalError)
        elif check_characters(accountBank) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditBank.setStyleSheet(generalError)
        elif self.check_duplicate(checkStatement1) is False:
            self.ui.labelError.setText("Duplicate Account: Try Unique Names")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
        elif self.check_duplicate(checkStatement2) is False:
            self.ui.labelError.setText("Duplicate Account: Try Unique Names")
            self.setStyleSheet(UniversalStyleSheet)
            self.ui.labelError.setStyleSheet(generalError)
            self.ui.lineEditAccount.setStyleSheet(generalError)
        elif check_characters_login(accountVariable1) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        elif "," in str(accountVariable2):
            self.ui.labelError.setText("No comma's necessary")
        elif check_characters_login(accountVariable2) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        else:
            self.add_account_information()
            self.ui.listWidgetAccount.addItem(accountName)
            self.setStyleSheet(UniversalStyleSheet)
            self.disable_widgets()

    # --- Modify Account Types ---- Opens the Question Dialog Window----------------------------------------------------
    def type_modifier(self):
        molly = ATypeQuestion(self.refUserDB, self.parentType)
        if molly.exec_() == QDialog.Accepted:
            self.ui.comboBoxATypes.clear()
            self.fill_widget(self.ui.comboBoxATypes, "SubType", "AccountSubType", "ParentType")

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ Functions for controlling active/in-active/cleared widgets                                           ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    def enable_widgets(self):
        self.ui.lineEditAccount.setEnabled(True)
        self.ui.comboBoxATypes.setEnabled(True)
        self.ui.lineEditPrimary.setEnabled(True)
        self.ui.lineEditBank.setEnabled(True)
        self.ui.pushButtonSubmit.setEnabled(True)
        self.ui.pushButtonMod.setEnabled(True)
        if self.parentType == "Bank":
            self.ui.lineEditVariable1.setEnabled(True)
        elif self.parentType == "Cash":
            pass
        elif self.parentType == "CD" or self.parentType == "Treasury":
            self.ui.lineEditVariable1.setEnabled(True)
            self.ui.lineEditVariable2.setEnabled(True)
        elif self.parentType == "Credit":
            self.ui.lineEditVariable1.setEnabled(True)
        elif self.parentType == "Debit":
            self.ui.lineEditVariable1.setEnabled(True)
            self.ui.lineEditVariable2.setEnabled(True)
        else:  # Equity and Retirement
            self.ui.lineEditVariable1.setEnabled(True)
            self.ui.lineEditVariable2.setEnabled(True)

    def disable_widgets(self):
        self.ui.lineEditAccount.setEnabled(False)
        self.ui.comboBoxATypes.setEnabled(False)
        self.ui.lineEditPrimary.setEnabled(False)
        self.ui.lineEditBank.setEnabled(False)
        self.ui.pushButtonSubmit.setEnabled(False)
        self.ui.pushButtonModify.setEnabled(False)
        self.ui.pushButtonMod.setEnabled(False)
        self.ui.pushButtonModify.hide()
        self.ui.pushButtonSubmit.show()
        if self.parentType == "Bank":
            self.ui.lineEditVariable1.setEnabled(False)
        elif self.parentType == "Cash":
            pass
        elif self.parentType == "CD" or self.parentType == "Treasury":
            self.ui.lineEditVariable1.setEnabled(False)
            self.ui.lineEditVariable2.setEnabled(False)
        elif self.parentType == "Credit":
            self.ui.lineEditVariable1.setEnabled(False)
        elif self.parentType == "Debit":
            self.ui.lineEditVariable1.setEnabled(False)
            self.ui.lineEditVariable2.setEnabled(False)
        else:  # Equity and Retirement
            self.ui.lineEditVariable1.setEnabled(False)
            self.ui.lineEditVariable2.setEnabled(False)

    def clear_widgets(self):
        self.ui.lineEditAccount.setText("")
        self.ui.lineEditPrimary.setText("")
        self.ui.lineEditBank.setText("")
        self.ui.labelError.setText("")
        self.ui.lineEditVariable1.setText("")
        self.ui.lineEditVariable2.setText("")

    def edit_combo_item(self, text):
        row = self.ui.listWidgetAccount.currentRow()
        newText = text.title()
        self.ui.listWidgetAccount.takeItem(row)
        self.ui.listWidgetAccount.insertItem(row, QListWidgetItem(newText))

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------ SQLite3 Functions                                                                                    ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- Fills a combobox or listwidget -------------------------------------------------------------------------------
    def fill_widget(self, combobox, col, tablename, coltwo):
        listStatement = "SELECT " + col + " FROM " + tablename + " WHERE " + coltwo + "= '" + self.parentType + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                conn.row_factory = lambda cursor, row: row[0]
                cur = conn.cursor()
                cur.execute(listStatement)
                comboTuple = cur.fetchall()
        except Error:
            self.ui.labelError.setText("Error: 85")
        finally:
            conn.close()
            combobox.addItems(comboTuple)

    # --- Checks to see if a table exists ------------------------------------------------------------------------------
    def check_bank_table(self):
        if self.parentType == "Bank":
            detailsTable = "CREATE TABLE IF NOT EXISTS " + self.accountDTable + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Interest_Rate REAL)"
        elif self.parentType == "Cash":
            detailsTable = "CREATE TABLE IF NOT EXISTS " + self.accountDTable + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT)"
        elif self.parentType == "CD" or self.parentType == "Treasury":
            detailsTable = "CREATE TABLE IF NOT EXISTS " + self.accountDTable + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Interest_Rate REAL, Maturity_Date NUMERIC)"
        elif self.parentType == "Credit":
            detailsTable = "CREATE TABLE IF NOT EXISTS " + self.accountDTable + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Credit_Limit INTEGER)"
        elif self.parentType == "Debt":
            detailsTable = "CREATE TABLE IF NOT EXISTS " + self.accountDTable + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Interest_Rate REAL, Starting_Balance REAL)"
        else:  # self.parentType == "Equity" or self.parentType == "Retirement":
            detailsTable = "CREATE TABLE IF NOT EXISTS " + self.accountDTable + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Ticker_Symbol TEXT, Stock_Price REAL)"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(detailsTable)
        except Error:
            self.ui.labelError.setText("Error: Could Not Locate User Database")
        finally:
            conn.close()

    # --- Checks to ensure an account name doesn't already exist for the user ------------------------------------------
    def check_duplicate(self, statement):
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(statement)
                row = cur.fetchone()
                if row is None:
                    print("Jake has Zero Trikes")
                    return True
                else:
                    return False
        except Error:
            self.ui.labelError.setText("Error: Issues Checking Account Names")
        finally:
            conn.close()

    # --- Submits the edits --------------------------------------------------------------------------------------------
    def submit_edit(self):
        variant1 = ["Bank", "Credit"]
        variant2 = ["CD", "Treasury", "Debt", "Equity", "Retirement"]

        accountName = self.ui.lineEditAccount.text()
        accountSubType = self.ui.comboBoxATypes.currentText()
        accountOwner = self.ui.lineEditPrimary.text()
        accountBank = self.ui.lineEditBank.text()
        accountVariable1 = self.ui.lineEditVariable1.text()
        accountVariable2 = self.ui.lineEditVariable2.text()

        if accountName == "" or accountOwner == "" or accountBank == "":
            self.ui.labelError.setText("Do Not Leave a Field Blank")
        elif len(accountName) >= 38:
            self.ui.labelError.setText("Try a Nickname for your Account")
        elif find_character(accountName) is False\
                or find_character(accountOwner) is False\
                or find_character(accountBank) is False:
            self.ui.labelError.setText("Do Not Leave a Field Blank")
        elif first_character_check(accountName) is False:
            self.ui.labelError.setText("Start Account Name with Letter")
        elif check_characters(accountName) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        elif check_characters(accountSubType) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        elif check_characters(accountOwner) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        elif check_characters(accountBank) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        elif check_characters_login(accountVariable1) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")
        elif "," in str(accountVariable2):
            self.ui.labelError.setText("No comma's necessary")
        elif check_characters_login(accountVariable2) is False:
            self.ui.labelError.setText("Alphanumeric Characters only")

        else:
            currentLedgerName = modify_for_sql(self.ui.listWidgetAccount.currentItem().text())
            newLedgerName = modify_for_sql(accountName)
            summaryUpdate = "UPDATE Account_Summary SET ID='" + accountName \
                            + "', SubType='" + accountSubType \
                            + "' WHERE ID='" + self.ui.listWidgetAccount.currentItem().text() + "'"
            deleteOldDetails = "DELETE FROM " + self.accountDTable + " WHERE Account_Name ='" + accountName + "'"
            if self.parentType in variant1:
                detailsUpdate = "INSERT INTO " + self.accountDTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + \
                                "', '" + accountVariable1 + "')"
            elif self.parentType in variant2:
                detailsUpdate = "INSERT INTO " + self.accountDTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + \
                                "', '" + accountVariable1 + \
                                "', '" + accountVariable2 + "')"
            else:  # Cash
                detailsUpdate = "INSERT INTO " + self.accountDTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + "')"
            if currentLedgerName != newLedgerName:
                ledgerUpdate = "ALTER TABLE " + currentLedgerName + " RENAME TO " + newLedgerName
            else:
                ledgerUpdate = "SELECT Subtype FROM AccountSubType WHERE ParentType='" + self.parentType + "'"
            # Above functions exists just to avoid a crash -------------------------------------------------------------
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    cur.execute(summaryUpdate)
                    cur.execute(deleteOldDetails)
                    cur.execute(detailsUpdate)
                    cur.execute(ledgerUpdate)
            except Error:
                self.ui.labelError.setText("Unable to Edit Account")
            finally:
                conn.close()
                old_receipt_dir = directory_pathway(self.parentType, currentLedgerName, self.refUser)
                new_receipt_dir = directory_pathway(self.parentType, newLedgerName, self.refUser)
                os.rename(old_receipt_dir, new_receipt_dir)
            self.edit_combo_item(self.ui.lineEditAccount.text())
            self.ui.listWidgetAccount.setCurrentRow(0)
            self.disp_current_selection()
            self.disable_widgets()
            self.ui.labelError.setText("")

    # --- Function to delete a transaction from the sql database -------------------------------------------------------
    def delete_account_sql(self, accountName):
        modifiedAN = modify_for_sql(accountName)
        deleteDetails = "DELETE FROM " + self.accountDTable + " WHERE Account_Name ='" + accountName + "'"
        deleteSummary = "DELETE FROM Account_Summary WHERE ID ='" + accountName + "'"
        dropLedger = "DROP TABLE IF EXISTS " + modifiedAN
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(deleteDetails)
                cur.execute(deleteSummary)
                cur.execute(dropLedger)
        except Error:
            self.ui.labelError.setText("Error Deleting Account")
        finally:
            conn.close()

    # --- Function to add Bank Account information to Database -----------------------------------------------------
    def add_account_information(self):
        variant1 = ["Bank", "Credit"]
        variant2 = ["CD", "Treasury", "Debt"]
        variant3 = ["Equity", "Retirement"]
        accountName = self.ui.lineEditAccount.text()
        modifiedAN = modify_for_sql(accountName)
        if self.parentType in variant1:
            if self.parentType == "Bank":
                itemType = "Asset"
            else:
                itemType = "Liability"
            accountDetails = "INSERT INTO " + self.accountDTable + \
                             " VALUES('" + self.ui.lineEditAccount.text() + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', '" + self.ui.lineEditPrimary.text() + \
                             "', '" + self.ui.lineEditBank.text() + \
                             "', '" + self.ui.lineEditVariable1.text() + "')"
            accountLedger = "CREATE TABLE IF NOT EXISTS " + modifiedAN + \
                            "(Transaction_Date NUMERIC, Transaction_Method TEXT," \
                            " Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Note TEXT," \
                            " Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            accountSummary = "INSERT INTO Account_Summary VALUES('" + self.ui.lineEditAccount.text() + \
                             "', '" + itemType + "', '" + self.parentType + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', NULL, '0.00')"
        elif self.parentType in variant2:
            if self.parentType == "Debt":
                itemType = "Liability"
            else:
                itemType = "Asset"
            accountDetails = "INSERT INTO " + self.accountDTable + \
                             " VALUES('" + self.ui.lineEditAccount.text() + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', '" + self.ui.lineEditPrimary.text() + \
                             "', '" + self.ui.lineEditBank.text() + \
                             "', '" + self.ui.lineEditVariable1.text() + \
                             "', '" + self.ui.lineEditVariable2.text() + "')"
            accountLedger = "CREATE TABLE IF NOT EXISTS " + modifiedAN + \
                            "(Transaction_Date NUMERIC, Transaction_Method TEXT," \
                            " Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Note TEXT," \
                            " Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            accountSummary = "INSERT INTO Account_Summary VALUES('" + self.ui.lineEditAccount.text() + \
                             "', '" + itemType + "', '" + self.parentType + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', NULL, '0.00')"
        elif self.parentType in variant3:
            tickerPrice = self.ui.lineEditVariable2.text()
            tickerPrice = str(decimal_places(tickerPrice, 4))
            accountDetails = "INSERT INTO " + self.accountDTable + \
                             " VALUES('" + self.ui.lineEditAccount.text() + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', '" + self.ui.lineEditPrimary.text() + \
                             "', '" + self.ui.lineEditBank.text() + \
                             "', '" + self.ui.lineEditVariable1.text().upper() + \
                             "', '" + str(tickerPrice) + "')"
            accountLedger = "CREATE TABLE IF NOT EXISTS " + modifiedAN + \
                            "(Transaction_Date NUMERIC, Transaction_Description TEXT, Category TEXT," \
                            " Debit REAL, Credit REAL, Sold REAL, Purchased REAL, Price REAL, Note TEXT, Status TEXT," \
                            " Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            accountSummary = "INSERT INTO Account_Summary VALUES('" + self.ui.lineEditAccount.text().title() + \
                             "', 'Asset', '" + self.parentType + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', '" + self.ui.lineEditVariable1.text().upper() + "', '0.00')"
        else:  # Cash
            accountDetails = "INSERT INTO " + self.accountDTable + \
                             " VALUES('" + self.ui.lineEditAccount.text() + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', '" + self.ui.lineEditPrimary.text() + \
                             "', '" + self.ui.lineEditBank.text() + "')"
            accountLedger = "CREATE TABLE IF NOT EXISTS " + modifiedAN + \
                            "(Transaction_Date NUMERIC, Transaction_Method TEXT," \
                            " Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Note TEXT," \
                            " Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            accountSummary = "INSERT INTO Account_Summary VALUES('" + self.ui.lineEditAccount.text() + \
                             "', 'Asset', '" + self.parentType + \
                             "', '" + self.ui.comboBoxATypes.currentText() + \
                             "', NULL, '0.00')"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(accountDetails)
                cur.execute(accountLedger)
                cur.execute(accountSummary)
        except Error:
            self.labelError.setText("Error: Could Not Create Bank Account")
        finally:
            conn.close()

    # --- Ability to show attributes of selected account. ----------------------------------------------------------
    def disp_current_selection(self):
        variant1 = ["Bank", "Credit"]
        variant2 = ["CD", "Treasury", "Debt", "Equity", "Retirement"]
        variant3 = "Cash"
        if self.ui.listWidgetAccount.currentItem() is None:
            account = ""
        else:
            account = self.ui.listWidgetAccount.currentItem().text()
        selectStatement = "SELECT * FROM " + self.accountDTable + " WHERE Account_Name ='" + account + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(selectStatement)
                row = cur.fetchone()
        except Error:
            self.ui.labelError.setText("Error: Couldn't Make Selection")
        finally:
            conn.close()
        if row is None:
            self.ui.lineEditAccount.setText("")
            self.ui.comboBoxATypes.setCurrentIndex(0)
            self.ui.lineEditPrimary.setText("")
            self.ui.lineEditBank.setText("")
            self.ui.lineEditVariable1.setText("")
            self.ui.lineEditVariable2.setText("")
        elif self.parentType in variant1:
            self.ui.lineEditAccount.setText(row[0])
            comboItem = row[1]
            self.find_combobox_text(comboItem)
            self.ui.lineEditPrimary.setText(row[2])
            self.ui.lineEditBank.setText(row[3])
            self.ui.lineEditVariable1.setText(str(row[4]))
        elif self.parentType in variant2:
            self.ui.lineEditAccount.setText(row[0])
            comboItem = row[1]
            self.find_combobox_text(comboItem)
            self.ui.lineEditPrimary.setText(row[2])
            self.ui.lineEditBank.setText(row[3])
            self.ui.lineEditVariable1.setText(str(row[4]))
            self.ui.lineEditVariable2.setText(str(row[5]))
        else:
            self.ui.lineEditAccount.setText(row[0])
            comboItem = row[1]
            self.find_combobox_text(comboItem)
            self.ui.lineEditPrimary.setText(row[2])
            self.ui.lineEditBank.setText(row[3])

    # --- Archive Account ----------------------------------------------------------------------------------------------
    def archive_account(self):
        if self.ui.listWidgetAccount.currentItem() is None:
            pass
        else:
            switch_sql_tables("Account_Archive", "Account_Summary", "ID", self.ui.listWidgetAccount.currentItem().text(),
                              self.refUserDB)
            self.ui.listWidgetAccount.clear()
            self.fill_widget(self.ui.listWidgetAccount, "ID", "Account_Summary", "ParentType")
            self.clear_widgets()

    # --- Changes the combobox to the desired input value automatically depending on the account selected --------------
    def find_combobox_text(self, comboItem):
        index = self.ui.comboBoxATypes.findText(comboItem)
        if index >= 0:
            self.ui.comboBoxATypes.setCurrentIndex(index)
        else:
            self.ui.labelError.setText("Error: Unidentified Bank Type")

    # --- Changed notice closeEvent for smooth transition between Dialogs ----------------------------------------------
    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database = "data/account/0cdio570sd64r7.db"
    parentType = "Bank"
    w = Accounts(database, parentType)
    w.show()
    sys.exit(app.exec_())

