# This file is the main hub for the program

import sys
import sqlite3
import os

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from sqlite3 import Error
from AlchemicalFinancesUi import Ui_MainWindow
from Ledger1 import LedgerV1
from Ledger2 import LedgerV2
from Summary import LedgerS
from About import AboutProgram
from Archive import Archive
from pathlib import Path
from UPK import account_pathway, modify_for_sql, specific_sql_statement, set_networth
from StyleSheets import UniversalStyleSheet


class AFBackbone(QMainWindow):
    refresh_signal_summary = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, user, messageCount):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # -- Class Global Variables - restricted to instance of class.
        self.dbPathway = account_pathway("UAInformation.db")
        self.refUser = str(user)
        self.switchCheck = int(messageCount)
        self.refUserDB = None
        self.dataCheck = None

        self.tabdic = {}
        self.setStyleSheet(UniversalStyleSheet)
        netWorthFont = QtGui.QFont()
        netWorthFont.setPixelSize(16)
        netWorthFont.setBold(True)

        self.ui.labelNW.setFont(netWorthFont)
        self.ui.labelStaticNW.setFont(netWorthFont)
        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ Menu bar Functions                                                                               ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        # -- -- File - Summary, Profile, Export [Future], Close
        self.ui.actionSummary.triggered.connect(lambda: self.switch_tab("Summary"))
        # self.ui.actionProfile.triggered.connect(self.toggle_summary)
        self.ui.actionClose.triggered.connect(self.close_app)
        # -- Assets - Bank, Equity, Retirement, CD, TB
        self.ui.actionBank.triggered.connect(lambda: self.switch_tab("Bank"))
        self.ui.actionEquity.triggered.connect(lambda: self.switch_tab("Equity"))
        self.ui.actionRetirement.triggered.connect(lambda: self.switch_tab("Retirement"))
        self.ui.actionCertificate_of_Deposit.triggered.connect(lambda: self.switch_tab("CD"))
        self.ui.actionTreasury_Bonds.triggered.connect(lambda: self.switch_tab("Treasury"))
        self.ui.actionCash.triggered.connect(lambda: self.switch_tab("Cash"))
        # -- Liabilities - Debt, CC, DC[Future], Cash[Future]
        self.ui.actionDebt.triggered.connect(lambda: self.switch_tab("Debt"))
        self.ui.actionCredit_Cards.triggered.connect(lambda: self.switch_tab("Credit"))
        self.ui.actionAbout.triggered.connect(lambda: self.switch_tab("About"))
        self.ui.actionArchive.triggered.connect(lambda: self.switch_tab("Archive"))
        self.ui.actionUserManual.triggered.connect(self.user_manual)

        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ Creation of a New User                                                                           ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        if self.create_profile_db() is True:
            self.account_summary(["Example Banking Account", "Example Equity Account", "Example Retirement Account",
                                  "Example CD Account", "Example Treasury Bond", "Example Debt Account",
                                  "Example Credit Card Account", "Example Wallet"],
                                 ["Bank", "Equity", "Retirement", "CD", "Treasury", "Debt", "Credit", "Cash"], 8)
            self.account_ledger("Example Banking Account", "Bank")
            self.account_ledger("Example CD Account", "CD")
            self.account_ledger("Example Treasury Bond", "Treasury")
            self.account_ledger("Example Debt Account", "Debt")
            self.account_ledger("Example Credit Card Account", "Credit")
            self.account_ledger("Example Wallet", "Cash")
            self.account_ledger("Example Equity Account", "Equity")
            self.account_ledger("Example Retirement Account", "Retirement")
            self.account_subtypes(["Checking", "Savings", "Money Market"], "Bank")
            self.account_subtypes(["Stock", "ETF", "Mutual Fund"], "Equity")
            self.account_subtypes(["Traditional 401K", "Roth 401K", "Traditional IRA", "Roth IRA"], "Retirement")
            self.account_subtypes(["12 Month", "2 Year", "3 Year", "4 Year", "5 Year"], "CD")
            self.account_subtypes(["E Bond", "EE Bond"], "Treasury")
            self.account_subtypes(["Student Loan", "Personal Loan", "Mortgage", "Car Loan"], "Debt")
            self.account_subtypes(["Visa", "Mastercard", "Discover", "American Express"], "Credit")
            self.account_subtypes(["Wallet"], "Cash")
            self.example_account_details("Example Banking Account", "Checking", "Bank")
            self.example_account_details("Example Equity Account", "Stock", "Equity")
            self.example_account_details("Example Retirement Account", "Traditional 401K", "Retirement")
            self.example_account_details("Example CD Account", "12 Month", "CD")
            self.example_account_details("Example Treasury Bond", "E Bond", "Treasury")
            self.example_account_details("Example Debt Account", "Student Loan", "Debt")
            self.example_account_details("Example Credit Card Account", "Visa", "Credit")
            self.example_account_details("Example Wallet", "Wallet", "Cash")
            self.initial_categories(["Initial", "Statement"], ["Bank", "Equity", "Retirement", "CD", "Treasury", "Debt",
                                                               "Credit", "Cash"])
            archiveStatement = "CREATE TABLE IF NOT EXISTS Account_Archive(ID TEXT, ItemType TEXT, ParentType TEXT," \
                               " SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
            specific_sql_statement(archiveStatement, self.refUserDB)

        # --------------------------------------------------------------------------------------------------------------
        # ------                                                                                                  ------
        # ------ Initialize appearance upon Loading                                                               ------
        # ------                                                                                                  ------
        # --------------------------------------------------------------------------------------------------------------
        summary = LedgerS(self, self.refUserDB, self.dataCheck)
        self.ui.mdiArea.addSubWindow(summary)
        summary.remove_tab_LS.connect(self.remove_tab)
        summary.showMaximized()
        self.tabdic.update({"Summary": summary})
        self.statusBar().showMessage("Operational")

        netWorth = set_networth("Account_Summary", self.refUserDB)
        self.ui.labelNW.setText(netWorth[1])
        self.ui.labelTA.setText(netWorth[2])
        self.ui.labelTD.setText(netWorth[3])

        # self.timer = QTimer()
        # self.timer.setInterval(60000)
        # self.timer.timeout.connect(self.tick)
        # self.timer.start()

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------                         General Functions Upon Initialization                                        ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- -- Acquire user Number from UAInformation database -----------------------------------------------------------
    def acquire_key(self):
        keyStatement = "SELECT Number FROM Users WHERE Profile = '" + self.refUser + "'"
        try:
            conn = sqlite3.connect(self.dbPathway[1])
            with conn:
                cur = conn.cursor()
                cur.execute(keyStatement)
                row = cur.fetchone()
                if row is None:
                    self.statusBar().showMessage("Error Alchemical: 146")
                else:
                    key = str(row[0])
        except Error as e:
            self.statusBar().setMessage("Error Alchemical: 150")
        finally:
            conn.close()
        return key

    # --- Create/Open Profile Database ---------------------------------------------------------------------------------
    # --- -- Creates new profile is one does not exist. As the .dat file uses the unaltered key ------------------------
    def create_profile_db(self):
        key = self.acquire_key()
        databaseFN = "db" + key + "rf.dat"                                                  # database File Name
        databaseFN_Pathway = account_pathway(databaseFN)
        databaseN = self.create_db_name()                                                   # database Name
        databaseN_Pathway = account_pathway(databaseN)
        try:
            with open(databaseFN_Pathway[0], mode="rb") as f:
                codedDN = f.read()
                self.refUserDB = codedDN.decode('utf-8')
                self.dataCheck = ("Opened File: " + self.refUserDB + " User Key: "
                                  + key + " User Name: " + str(self.refUser))
                f.close()
                return False
        except IOError:
            with open(databaseFN_Pathway[0], mode="wb") as nf:
                nf.write(databaseN_Pathway[0].encode('utf-8'))
                nf.close()
                self.refUserDB = databaseN_Pathway[0]
                self.dataCheck = ("New File Made: " + str(self.refUserDB))
                return True

    # --- -- Create DB Name: Uses combination of Profile and Key--------------------------------------------------------
    # --- -- -- Creates a database name. Only used in create_profile_db() if new user ----------------------------------
    def create_db_name(self):
        from random import shuffle
        key = self.acquire_key()
        databasename = ""
        nameList = []
        countUser = len(self.refUser) - 1
        countKey = len(key) - 1
        while countUser >= 0:
            nameList.append(self.refUser[countUser])
            countUser -= 1
        while countKey >= 0:
            nameList.append(key[countKey])
            countKey -= 1
        shuffle(nameList)
        for piece in nameList:
            databasename = databasename + piece
        databasename = databasename + ".db"
        return databasename

    # --- -- Shut Down App via the File Menu ---------------------------------------------------------------------------
    def close_app(self, event):
        quit_msg = "Are you sure you want to quit the program?"
        reply = QMessageBox.question(self, 'Quit Message', quit_msg, QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.accept()
        else:
            pass

    # --- -- ErrorMessage for when sub windows are closed improperly. Issue that needs to eventually be resolved. ------
    def error_message(self):
        error_msg = """Sorry, you incorrectly closed this tab.\n
In the future toggle visibility via the file menu. \n
To re-access this tab restart the Application."""
        reply = QMessageBox.warning(self, "404 - Porcelain Prayer", error_msg, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.statusBar().showMessage("Error Occurred: Restart Application")
        else:
            self.statusBar().showMessage("Error Occurred: Restart Application")

    # ------------------------------------------------------------------------------------------------------------------
    # ------                                                                                                      ------
    # ------                         SQLite3 focused functions                                                    ------
    # ------                                                                                                      ------
    # ------------------------------------------------------------------------------------------------------------------
    # --- Creates Dialogs for the different ledgers --------------------------------------------------------------------
    # --- -- works in conjunction with tabdic to limit each tab to a singular use --------------------------------------
    def switch_tab(self, parentType):
        type1 = ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit"]
        type2 = ["Equity", "Retirement"]
        try:
            self.tabdic[parentType].setFocus()
        except KeyError:
            if parentType == "Summary":
                summary = LedgerS(self, self.refUserDB, self.dataCheck)
                self.ui.mdiArea.addSubWindow(summary)
                summary.remove_tab_LS.connect(self.remove_tab)
                summary.showMaximized()
                self.tabdic.update({parentType: summary})
            elif parentType in type1:
                ledger = LedgerV1(self.refUserDB, parentType, self.refUser)
                self.ui.mdiArea.addSubWindow(ledger)
                ledger.refresh_signal.connect(self.refresh_networth)
                ledger.remove_tab.connect(self.remove_tab)
                ledger.showMaximized()
                self.tabdic.update({parentType: ledger})
            elif parentType in type2:
                ledger2 = LedgerV2(self.refUserDB, parentType, self.refUser)
                self.ui.mdiArea.addSubWindow(ledger2)
                ledger2.refresh_signal_L2.connect(self.refresh_networth)
                ledger2.remove_tab_L2.connect(self.remove_tab)
                ledger2.showMaximized()
                self.tabdic.update({parentType: ledger2})
            elif parentType == "About":
                about = AboutProgram()
                self.ui.mdiArea.addSubWindow(about)
                about.remove_tab_about.connect(self.remove_tab)
                about.showMaximized()
                self.tabdic.update({parentType: about})
            elif parentType == "Archive":
                archive = Archive(self.refUserDB, self.refUser)
                self.ui.mdiArea.addSubWindow(archive)
                archive.remove_tab_archive.connect(self.remove_tab)
                archive.showMaximized()
                self.tabdic.update({parentType: archive})
            else:
                print("Error : 227")

    # --- Create Table with two Columns --------------------------------------------------------------------------------
    def check_twocol_table(self, tablename, colone, coltwo):
        checkStatement = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + colone + " TEXT, " + coltwo + " TEXT)"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(checkStatement)
        except Error as e:
            self.statusBar().showMessage("Error Alchemical: 277")
        finally:
            conn.close()

    # --- Unused Function --- Should delete ----------------------------------------------------------------------------
    def check_column(self, tablename, col):
        checkColumn = "SELECT COUNT(*) AS CENTRA FROM PRAGMA_table_info('" + tablename + "') WHERE name='" + col + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(checkColumn)
                row = cur.fetchone()
                if row is None:
                    return True
                else:
                    return False
        except Error:
            self.statusBar().showMessage("Error Alchemical: 295")
        finally:
            conn.close()

    # --- Unused Function --- Should delete ----------------------------------------------------------------------------
    def add_column(self, tablename, col, sqltype):
        alterStatement = "ALTER TABLE " + tablename + " ADD COLUMN " + col + " " + sqltype
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(alterStatement)
        except Error:
            self.statusBar().showMessage("Error Alchemical: 308")
        finally:
            conn.close()

    # --- Used to determine is something already exists ----------------------------------------------------------------
    def check_for_data(self, tablename, colTwo, value):
        checkStatement = "SELECT * FROM " + tablename + " WHERE " + colTwo + " = '" + value + "'"
        # Example = "SELECT ID FROM AccountNames"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(checkStatement)
                row = cur.fetchone()
                if row is None:
                    return True
                else:
                    return False
        except Error as e:
            self.statusBar().showMessage("Error Alchemical: 327")
        finally:
            conn.close()

    # --- Create Account Ledgers ---------------------------------------------------------------------------------------
    def account_ledger(self, accountName, parentType):
        finalName = modify_for_sql(accountName)
        variant1 = ["Bank", "CD", "Treasury", "Debt", "Credit", "Cash"]
        variant2 = ["Equity", "Retirement"]
        if parentType in variant1:
            ledgerStatement = "CREATE TABLE IF NOT EXISTS " + finalName + \
                            "(Transaction_Date NUMERIC, Transaction_Method TEXT," \
                            " Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Note TEXT," \
                            " Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            specific_sql_statement(ledgerStatement, self.refUserDB)
        elif parentType in variant2:
            ledgerStatement = "CREATE TABLE IF NOT EXISTS " + finalName + \
                              "(Transaction_Date NUMERIC, Transaction_Description TEXT, Category TEXT," \
                              " Debit REAL, Credit REAL, Sold REAL, Purchased REAL, Price REAL, Note TEXT, Status TEXT," \
                              " Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            specific_sql_statement(ledgerStatement, self.refUserDB)

    # --- Database Tables ----------------------------------------------------------------------------------------------
    def account_summary(self, accountName, accountType, num):
        x = 0
        summaryStatement = "CREATE TABLE IF NOT EXISTS Account_Summary(ID TEXT, ItemType TEXT, ParentType TEXT," \
                           " SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
        specific_sql_statement(summaryStatement, self.refUserDB)
        if self.check_for_data("Account_Summary", "ParentType", accountType[x]) is True:
            for name in accountName:
                exampleStatement = "INSERT INTO Account_Summary VALUES('" + name + "', NULL, '" + accountType[x] +\
                                   "', NULL, NULL, '0.00')"
                if x <= num:
                    try:
                        conn = sqlite3.connect(self.refUserDB)
                        with conn:
                            cur = conn.cursor()
                            cur.execute(exampleStatement)
                    except Error:
                        self.statusBar().showMessage("Error Alchemical: 366")
                    finally:
                        conn.close()
                    x += 1
                if x > num:
                    break

    # --- This function is used to generate a new users example ledgers ------------------------------------------------
    def example_account_details(self, accountName, subtype, parentType):
        variant1 = ["Bank", "Cash", "CD", "Treasury", "Equity", "Retirement"]
        variant2 = ["Credit", "Debt"]
        if parentType in variant1:
            itemType = "Asset"
        else:  # variant2
            itemType = "Liability"
        from datetime import datetime
        currentDate = datetime.now().strftime("%m/%d/%Y")
        if parentType == "Bank":
            detailsTableName = parentType + "_Account_Details"
            detailsTableStatement = "CREATE TABLE IF NOT EXISTS " + detailsTableName + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Interest_Rate REAL)"
            detailsValueStatement = "INSERT INTO " + detailsTableName + " VALUES('" + accountName + "', '" + subtype + "', '" + self.refUser + "', 'Alchemical Finances Bank', '1.00')"
            summaryStatement = "UPDATE Account_Summary SET SubType='" + subtype + "', ItemType='" + itemType + "' WHERE ID='" + accountName + "'"
            specific_sql_statement(detailsTableStatement, self.refUserDB)
            if self.check_for_data(detailsTableName, "Account_Name", accountName) is True:
                specific_sql_statement(detailsValueStatement, self.refUserDB)
                specific_sql_statement(summaryStatement, self.refUserDB)
        elif parentType == "Cash":
            detailsTableName = parentType + "_Account_Details"
            detailsTableStatement = "CREATE TABLE IF NOT EXISTS " + detailsTableName + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT)"
            detailsValueStatement = "INSERT INTO " + detailsTableName + " VALUES('" + accountName + "', '" + subtype + "', '" + self.refUser + "', 'Alchemical Finances Bank')"
            summaryStatement = "UPDATE Account_Summary SET SubType='" + subtype + "', ItemType='" + itemType + "' WHERE ID='" + accountName + "'"
            specific_sql_statement(detailsTableStatement, self.refUserDB)
            if self.check_for_data(detailsTableName, "Account_Name", accountName) is True:
                specific_sql_statement(detailsValueStatement, self.refUserDB)
                specific_sql_statement(summaryStatement, self.refUserDB)
        elif parentType == "CD" or parentType == "Treasury":
            detailsTableName = parentType + "_Account_Details"
            detailsTableStatement = "CREATE TABLE IF NOT EXISTS " + detailsTableName + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Interest_Rate REAL, Maturity_Date NUMERIC)"
            detailsValueStatement = "INSERT INTO " + detailsTableName + " VALUES('" + accountName + "', '" + subtype + "', '" + self.refUser + "', 'Alchemical Finances Bank', '1.00', '" + currentDate + "')"
            summaryStatement = "UPDATE Account_Summary SET SubType='" + subtype + "', ItemType='" + itemType + "' WHERE ID='" + accountName + "'"
            specific_sql_statement(detailsTableStatement, self.refUserDB)
            if self.check_for_data(detailsTableName, "Account_Name", accountName) is True:
                specific_sql_statement(detailsValueStatement, self.refUserDB)
                specific_sql_statement(summaryStatement, self.refUserDB)
        elif parentType == "Credit":
            detailsTableStatement = "CREATE TABLE IF NOT EXISTS Credit_Account_Details(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Credit_Limit INTEGER)"
            detailsValueStatement = "INSERT INTO Credit_Account_Details VALUES('" + accountName + "', '" + subtype + "', '" + self.refUser + "', 'Alchemical Finances Bank', '10000')"
            summaryStatement = "UPDATE Account_Summary SET SubType='" + subtype + "', ItemType='" + itemType + "' WHERE ID='" + accountName + "'"
            specific_sql_statement(detailsTableStatement, self.refUserDB)
            if self.check_for_data("Credit_Account_Details", "Account_Name", accountName) is True:
                specific_sql_statement(detailsValueStatement, self.refUserDB)
                specific_sql_statement(summaryStatement, self.refUserDB)
        elif parentType == "Debt":
            detailsTableName = parentType + "_Account_Details"
            detailsTableStatement = "CREATE TABLE IF NOT EXISTS " + detailsTableName + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Interest_Rate REAL, Starting_Balance REAL)"
            detailsValueStatement = "INSERT INTO " + detailsTableName + " VALUES('" + accountName + "', '" + subtype + "', '" + self.refUser + "', 'Alchemical Finances Bank', '1.00', '10000')"
            summaryStatement = "UPDATE Account_Summary SET SubType='" + subtype + "', ItemType='" + itemType + "' WHERE ID='" + accountName + "'"
            specific_sql_statement(detailsTableStatement, self.refUserDB)
            if self.check_for_data(detailsTableName, "Account_Name", accountName) is True:
                specific_sql_statement(detailsValueStatement, self.refUserDB)
                specific_sql_statement(summaryStatement, self.refUserDB)
        elif parentType == "Equity" or parentType == "Retirement":
            detailsTableName = parentType + "_Account_Details"
            detailsTableStatement = "CREATE TABLE IF NOT EXISTS " + detailsTableName + "(Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Ticker_Symbol TEXT, Stock_Price REAL)"
            detailsValueStatement = "INSERT INTO " + detailsTableName + " VALUES('" + accountName + "', '" + subtype + "', '" + self.refUser + "', 'Alchemical Finances Bank', 'AFB',  '1.0000')"
            summaryStatement = "UPDATE Account_Summary SET SubType='" + subtype\
                               + "', ItemType='" + itemType + "', Ticker_Symbol='AFB' WHERE ID='" + accountName + "'"
            specific_sql_statement(detailsTableStatement, self.refUserDB)
            if self.check_for_data(detailsTableName, "Account_Name", accountName) is True:
                specific_sql_statement(detailsValueStatement, self.refUserDB)
                specific_sql_statement(summaryStatement, self.refUserDB)

    # --- -- - Transaction/Categories Second ---------------------------------------------------------------------------
    def initial_categories(self, methodList, typeList):
        self.check_twocol_table("Categories", "Method", "ParentType")
        if self.check_for_data("Categories", "ParentType", typeList[0]) is True:
            try:
                conn = sqlite3.connect(self.refUserDB)
                with conn:
                    cur = conn.cursor()
                    for method in methodList:
                        for type in typeList:
                            generalStatement = "INSERT INTO Categories Values('" + method + "', '" + type + "')"
                            cur.execute(generalStatement)
            except Error as e:
                self.statusBar().showMessage("Error Alchemical: 451")
            finally:
                conn.close()
        else:
            pass

    # --- -- - Account SubType Third -----------------------------------------------------------------------------------
    def account_subtypes(self, subTypes, parentType):
        self.check_twocol_table("AccountSubType", "SubType", "ParentType")
        if self.check_for_data("AccountSubType", "ParentType", parentType) is True:
            for account in subTypes:
                dbStatement = "INSERT INTO AccountSubType Values('" + account + "', '" + parentType + "')"
                try:
                    conn = sqlite3.connect(self.refUserDB)
                    with conn:
                        cur = conn.cursor()
                        cur.execute(dbStatement)
                except Error:
                    self.statusBar().showMessage("Error Alchemical: 469")
                finally:
                    conn.close()

    # --- User Manual --------------------------------------------------------------------------------------------------
    def user_manual(self):
        os.startfile("USER_MANUAL.pdf")

    # --- Saved to use later -------------------------------------------------------------------------------------------
    # def mouseReleaseEvent(self, event):
        # if event.button() == QtCore.Qt.LeftButton:
            # self.click += 1
            # self.ui.labelStaticNW.setText("Hello " + str(self.click))

    # --- Saved as Example to use later --------------------------------------------------------------------------------
    # def tick(self):
        # self.click += 1
        # self.ui.labelStaticNW.setText("Hello " + str(self.click))
        # netWorth = str(set_networth("Account_Summary", self.refUserDB))
        # self.ui.labelNW.setText("$ " + netWorth)

    # --- Allows communication between objects. Will be used to limit the number of ledgers open -----------------------
    @pyqtSlot(str)
    def refresh_networth(self, message):
        if message == "1":
            netWorth = set_networth("Account_Summary", self.refUserDB)
            self.ui.labelNW.setText(netWorth[1])
            self.ui.labelTA.setText(netWorth[2])
            self.ui.labelTD.setText(netWorth[3])
            self.trigger_refresh_summary()
        else:
            pass

    @pyqtSlot(str)
    def remove_tab(self, message):
        try:
            self.ui.mdiArea.removeSubWindow(self.tabdic[message])
            self.tabdic.pop(message)
        except KeyError:
            self.statusBar().showMessage("Error Alchemical: 504")

    # --- PyQt5 signal to refresh Summary QDialog Account Balances -----------------------------------------------------
    def trigger_refresh_summary(self):
        self.refresh_signal_summary.emit("2")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = "Place holder"
    lily = AFBackbone(user)
    lily.show()
    sys.exit(app.exec_())

