# This file is incomplete. Will house the user Worth Summary broken down by existing accounts
#     def __init__(self, database, dataCheck):

import sys
import sqlite3

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFrame, QScrollArea, QWidget, QGridLayout,\
    QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QProgressBar
from PyQt5.QtCore import QTimer, pyqtSlot
from sqlite3 import Error
from SummaryUi import Ui_Dialog
from UPK import add_comma, decimal_places, modify_for_sql, obtain_sql_value, obtain_sql_list
from StyleSheets import messagesheet, innerframesheet, progressSheet, parentypeSheet, colheadersheet, subtotalsheet,\
    accountsheet


class LedgerS(QDialog):
    remove_tab_LS = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, parent, database, dataCheck):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.summaryTuple = None
        # label dictionary[AccountName] = label for Account Balances
        self.balancelabeldic = {}
        # label dictionary[ParentType] = label for SubType Balances
        self.subtotaldic = {}
        # label dictionary[AccountName] = label for ProgressBar
        self.progBardic = {}
        self.updateMessages = []
        self.summaryFrame = QFrame(self)
        self.summaryFrame.setGeometry(250, 0, 950, 801)
        self.summaryFrame.setFrameStyle(1)
        # Label Below exists as a method of checking that data was transferring between modules properly.
        # self.ui.labelTest.setText(dataCheck)
        self.ui.labelTest.hide()

        self.obtain_summaryTuple()
        self.create_scrollarea()
        self.setStyleSheet(progressSheet)
        self.show()

        parent.refresh_signal_summary.connect(self.refresh_balance_labels)

    def create_scrollarea(self):
        self.summaryScroll = QScrollArea(self.summaryFrame)
        self.summaryScroll.setFixedWidth(950)
        self.summaryScroll.setFixedHeight(785)
        self.summaryScroll.setFrameStyle(0)
        self.summaryScroll.setWidgetResizable(True)

        widget = QWidget()
        self.summaryScroll.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)
        self.layout_SArea.addWidget(self.generate_layout())
        self.layout_SArea.addStretch(1)

    def obtain_summaryTuple(self):
        summaryStatement = """SELECT ItemType, ParentType, SubType, ID, Balance FROM Account_Summary """ \
                           + """ORDER BY "ItemType", "ParentType", "SubType", "Balance" DESC LIMIT 0, 49999"""
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(summaryStatement)
                summaryDate = cur.fetchall()
                self.summaryTuple = summaryDate
        except Error:
            print("Error Summary Data Collection Failure")
        finally:
            conn.close()

    def generate_layout(self):
        innerFrame = QFrame(self)
        innerFrame.setStyleSheet(innerframesheet)
        summarygridLayout = QGridLayout(innerFrame)

        horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Fixed, QSizePolicy.Expanding)
        # (row, col, rowspn columnspan)
        summarygridLayout.addItem(horizontalSpacer, 0, 0, 1, 1)

        spacerLabel = QLabel(self)
        spacerLabel.setObjectName("SpacerLabel")
        spacerLabel.setText("")
        spacerLabel.setFixedWidth(250)
        summarygridLayout.addWidget(spacerLabel, 1, 5, 1, 1)

        row = 0
        subTotal = 0

        listofBank = [account for account in self.summaryTuple if "Bank" in account]
        listofCD = [account for account in self.summaryTuple if "CD" in account]
        listofCash = [account for account in self.summaryTuple if "Cash" in account]
        listofEquity = [account for account in self.summaryTuple if "Equity" in account]
        listofRetirement = [account for account in self.summaryTuple if "Retirement" in account]
        listofCredit = [account for account in self.summaryTuple if "Credit" in account]
        listofDebt = [account for account in self.summaryTuple if "Debt" in account]
        listofTreasury = [account for account in self.summaryTuple if "Treasury" in account]

        parentType_dict = {
            "Bank": listofBank,
            "Cash": listofCash,
            "Certificate of Deposit": listofCD,
            "Equity": listofEquity,
            "Treasury Bonds": listofTreasury,
            "Retirement": listofRetirement,
            "Credit": listofCredit,
            "Debt": listofDebt
        }

        labelMessage = QLabel(self)
        labelMessage.setObjectName("labelMessages")
        labelMessage.setText("")
        messagefont = QtGui.QFont()
        messagefont.setPointSize(12)
        messagefont.setBold(True)
        messagefont.setUnderline(False)
        messagefont.setWeight(50)
        labelMessage.setFont(messagefont)
        labelMessage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        labelMessage.setFrameShape(QFrame.Panel)
        labelMessage.setFrameShadow(QFrame.Plain)
        summarygridLayout.addWidget(labelMessage, row, 0, 1, 4)
        labelMessage.hide()
        self.updateMessages.append(labelMessage)

        row += 1

        for parentType in parentType_dict:
            listofAccounts = parentType_dict[parentType]
            if len(listofAccounts) > 0:
                labelparent = QLabel(self)
                labelparent.setObjectName("label" + parentType)
                labelparent.setText("  " + parentType.title())
                parentfont = QtGui.QFont()
                parentfont.setPointSize(16)
                parentfont.setBold(True)
                parentfont.setWeight(70)
                labelparent.setFont(parentfont)
                labelparent.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
                labelparent.setFrameShape(QFrame.Panel)
                labelparent.setFrameShadow(QFrame.Sunken)
                labelparent.setStyleSheet(parentypeSheet)
                summarygridLayout.addWidget(labelparent, row, 0, 1, 4)

                row += 1

                labelColheader1 = QLabel(self)
                labelColheader1.setObjectName("labelAN" + parentType + "header")
                labelColheader1.setText("Account Name")
                headerfont = QtGui.QFont()
                headerfont.setPointSize(12)
                headerfont.setBold(True)
                headerfont.setWeight(60)
                labelColheader1.setFont(headerfont)
                labelColheader1.setFrameShape(QFrame.Panel)
                labelColheader1.setFrameShadow(QFrame.Sunken)
                labelColheader1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter)
                labelColheader1.setStyleSheet(colheadersheet)
                summarygridLayout.addWidget(labelColheader1, row, 1, 1, 1)

                labelColheader2 = QLabel(self)
                labelColheader2.setObjectName("labelAT" + parentType + "header")
                labelColheader2.setText("Account Type")
                labelColheader2.setFont(headerfont)
                labelColheader2.setFrameShape(QFrame.Panel)
                labelColheader2.setFrameShadow(QFrame.Sunken)
                labelColheader2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter)
                labelColheader2.setStyleSheet(colheadersheet)
                summarygridLayout.addWidget(labelColheader2, row, 2, 1, 1)

                labelColheader3 = QLabel(self)
                labelColheader3.setObjectName("labelB" + parentType + "header")
                labelColheader3.setText("Balance")
                labelColheader3.setFont(headerfont)
                labelColheader3.setFrameShape(QFrame.Panel)
                labelColheader3.setFrameShadow(QFrame.Sunken)
                labelColheader3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter)
                labelColheader3.setStyleSheet(colheadersheet)
                summarygridLayout.addWidget(labelColheader3, row, 3, 1, 1)

                row += 1

                for account in listofAccounts:
                    # [A/L, ParentType, Subtype, ID, Balance]
                    accountID = modify_for_sql(account[3])
                    verticalSpacer = QSpacerItem(80, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    summarygridLayout.addItem(verticalSpacer, row, 0, 1, 1)

                    labelID = QLabel(self)
                    labelID.setObjectName("labelAN" + accountID)
                    labelID.setText("  " + account[3].title() + "     ")
                    IDfont = QtGui.QFont()
                    IDfont.setPointSize(12)
                    IDfont.setBold(False)
                    IDfont.setUnderline(False)
                    IDfont.setWeight(50)
                    labelID.setFont(IDfont)
                    labelID.setStyleSheet(accountsheet)
                    summarygridLayout.addWidget(labelID, row, 1, 1, 1)

                    labelSubtype = QLabel(self)
                    labelSubtype.setObjectName("labelAT" + accountID)
                    labelSubtype.setText("  " + account[2].title())
                    subtypeFont = QtGui.QFont()
                    subtypeFont.setPointSize(12)
                    subtypeFont.setWeight(50)
                    labelSubtype.setFont(subtypeFont)
                    labelSubtype.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
                    labelSubtype.setStyleSheet(accountsheet)
                    summarygridLayout.addWidget(labelSubtype, row, 2, 1, 1)

                    labelBalance = QLabel(self)
                    labelBalance.setObjectName("labelBal" + accountID)
                    # label dictionary[AccountName] = labelBalance for Account Balances
                    self.balancelabeldic[account[3]] = labelBalance
                    modBalance = decimal_places(account[4], 2)
                    posNeg = modBalance
                    subTotal += modBalance
                    modBalance = add_comma(modBalance, 2)
                    if account[0] == "Liability":
                        if posNeg >= 0:
                            labelBalance.setText("($  " + modBalance + ")     ")
                        else:
                            labelBalance.setText("$  " + modBalance + "     ")
                    else:
                        if posNeg >= 0:
                            labelBalance.setText("$  " + modBalance + "     ")
                        else:
                            labelBalance.setText("($  " + modBalance + ")     ")
                    labelBalance.setFont(IDfont)
                    labelBalance.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                    labelBalance.setStyleSheet(accountsheet)
                    summarygridLayout.addWidget(labelBalance, row, 3, 1, 1)

                    row += 1

                    if parentType == "Debt" or parentType == "Credit":
                        labelprogress = QLabel(self)
                        labelprogress.setObjectName("labelProg" + accountID)
                        if parentType == "Debt":
                            labelprogress.setText("  Percent Remaining:")
                        else:
                            labelprogress.setText("  Credit Available:")
                        progressfont = QtGui.QFont()
                        progressfont.setPointSize(10)
                        progressfont.setBold(True)
                        progressfont.setUnderline(False)
                        progressfont.setWeight(65)
                        labelprogress.setFont(progressfont)
                        labelprogress.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                        summarygridLayout.addWidget(labelprogress, row, 1, 1, 1)

                        debtprogressBar = QProgressBar(self)
                        debtprogressBar.setMinimum(0)
                        debtprogressBar.setMaximum(100)

                        if parentType == "Debt":
                            start = self.obtain_liability_start("Starting_Balance", "Debt_Account_Details", account[3])
                            progress = (decimal_places(account[4], 2) / decimal_places(start, 2)) * 100
                            progress = int(progress)
                        else:
                            start = self.obtain_liability_start("Credit_Limit", "Credit_Account_Details", account[3])
                            progress = 100 - ((decimal_places(account[4], 2) / decimal_places(start, 2)) * 100)
                            progress = int(progress)

                        debtprogressBar.setProperty("value", progress)
                        debtprogressBar.setObjectName("progressBar" + accountID)
                        # label dictionary[AccountName] = label for ProgressBar
                        self.progBardic[account[3]] = debtprogressBar
                        summarygridLayout.addWidget(debtprogressBar, row, 2, 1, 2)

                    row += 1

                labelTotal = QLabel(self)
                labelTotal.setObjectName("label" + parentType + "total")
                labelTotal.setText("Subtotal")
                totalfont = QtGui.QFont()
                totalfont.setPointSize(10)
                totalfont.setBold(True)
                totalfont.setUnderline(False)
                totalfont.setWeight(65)
                labelTotal.setFont(totalfont)
                labelTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                summarygridLayout.addWidget(labelTotal, row, 1, 1, 2)

                labelSubTotal = QLabel(self)
                labelSubTotal.setObjectName("label" + parentType + "Subtotal")
                # label dictionary[ParentType] = label for SubType Balances
                self.subtotaldic[parentType] = labelSubTotal
                subTotal = decimal_places(subTotal, 2)
                subTotal = add_comma(subTotal, 2)
                if parentType == "Debt" or parentType == "Credit":
                    labelSubTotal.setText("($  " + subTotal + ")     ")
                else:
                    labelSubTotal.setText("$  " + subTotal + "     ")
                labelSubTotal.setFont(IDfont)
                labelSubTotal.setFrameShape(QFrame.Panel)
                labelSubTotal.setFrameShadow(QFrame.Sunken)
                labelSubTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                labelSubTotal.setStyleSheet(subtotalsheet)
                summarygridLayout.addWidget(labelSubTotal, row, 3, 1, 1)

                row += 1
                subTotal = 0
            else:
                pass
        return innerFrame

    def obtain_liability_start(self, col, tableName, accountName):
        startStatement = "SELECT " + col + " FROM " + tableName + " WHERE Account_Name='" + accountName + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(startStatement)
                start = cur.fetchone()
        except Error:
            start = 0.00
            return start
        finally:
            conn.close()
            start = start[0]
        return start

    def refresh_balance_labels(self):
        for account in self.balancelabeldic:
            balanceStatement = "SELECT Balance, ItemType, ParentType FROM Account_Summary WHERE ID='" + account + "'"
            accountInfo = obtain_sql_value(balanceStatement, self.refUserDB)
            if accountInfo is None:
                accountInfo = (0.00, "Deleted", "Deleted")
            modBalance = add_comma(accountInfo[0],  2)
            targetlabel = self.balancelabeldic[account]

            if accountInfo[1] == "Liability":
                if accountInfo[0] >= 0:
                    targetlabel.setText("($  " + modBalance + ")     ")
                else:
                    targetlabel.setText("$  " + modBalance + "     ")
            elif accountInfo[1] == "Deleted":
                targetlabel.setText("$ 0.00")
            else:
                if accountInfo[0] >= 0:
                    targetlabel.setText("$  " + modBalance + "     ")
                else:
                    targetlabel.setText("($  " + modBalance + ")     ")

            if account in self.progBardic:
                if accountInfo[2] == "Debt":
                    start = self.obtain_liability_start("Starting_Balance", "Debt_Account_Details", account)
                    progress = (decimal_places(accountInfo[0], 2) / decimal_places(start, 2)) * 100
                    progress = int(progress)
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)
                elif accountInfo[2] == "Deleted":
                    progress = 100
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)
                else:
                    start = self.obtain_liability_start("Credit_Limit", "Credit_Account_Details", account)
                    progress = 100 - ((decimal_places(accountInfo[0], 2) / decimal_places(start, 2)) * 100)
                    progress = int(progress)
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)

        for parentType in self.subtotaldic:
            if parentType == "Certificate of Deposit":
                sqlparentType = "CD"
            elif parentType == "Treasury Bonds":
                sqlparentType = "Treasury"
            else:
                sqlparentType = parentType
            subTotalStatement = "SELECT SUM(Balance), ItemType FROM Account_Summary WHERE ParentType='" + sqlparentType + "'"
            subTotalInfo = obtain_sql_value(subTotalStatement, self.refUserDB)
            preModSubTotal = subTotalInfo[0]
            if preModSubTotal is None:
                preModSubTotal = 0.0
            modSubTotal = add_comma(preModSubTotal, 2)
            targetlabel = self.subtotaldic[parentType]
            if subTotalInfo[1] == "Liability":
                if preModSubTotal >= 0:
                    targetlabel.setText("($  " + modSubTotal + ")     ")
                else:
                    targetlabel.setText("$  " + modSubTotal + "     ")
            else:
                if preModSubTotal >= 0:
                    targetlabel.setText("$  " + modSubTotal + "     ")
                else:
                    targetlabel.setText("($  " + modSubTotal + ")     ")

        self.user_messages()

    def user_messages(self):
        accountStatment = "SELECT ID FROM Account_Summary"
        accountList = obtain_sql_list(accountStatment, self.refUserDB)
        currentQTYaccounts = len(accountList)
        oldQTYaccounts = len(self.summaryTuple)
        messagelabel = self.updateMessages[0]
        messagelabel.setStyleSheet(messagesheet)

        changes = "Reload to Display Changes to Accounts"

        if currentQTYaccounts != oldQTYaccounts:
            messagelabel.setText(changes)
            messagelabel.show()
        else:
            pass

    # --- Receive a message from the MainWindow to refresh -----------------------
    @pyqtSlot(str)
    def refresh_networth(self, message):
        if message == "2":
            self.refresh_Balance_labels()
        else:
            print("Failure Summary 423")

    # --- PyQt5 signal to remove ParentType Ledger from tabdic ---------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_LS.emit("Summary")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = LedgerS()
    lily.show()
    sys.exit(app.exec_())
