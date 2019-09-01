# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArchiveUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 798)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.labelStaticLA = QtWidgets.QLabel(Dialog)
        self.labelStaticLA.setGeometry(QtCore.QRect(20, 20, 115, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelStaticLA.setFont(font)
        self.labelStaticLA.setObjectName("labelStaticLA")
        self.tableWidgetL1 = QtWidgets.QTableWidget(Dialog)
        self.tableWidgetL1.setGeometry(QtCore.QRect(20, 95, 1170, 651))
        self.tableWidgetL1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidgetL1.setLineWidth(2)
        self.tableWidgetL1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetL1.setAlternatingRowColors(True)
        self.tableWidgetL1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidgetL1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetL1.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidgetL1.setShowGrid(False)
        self.tableWidgetL1.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetL1.setObjectName("tableWidgetL1")
        self.tableWidgetL1.setColumnCount(0)
        self.tableWidgetL1.setRowCount(0)
        self.tableWidgetL1.horizontalHeader().setStretchLastSection(True)
        self.pushButtonRestore = QtWidgets.QPushButton(Dialog)
        self.pushButtonRestore.setGeometry(QtCore.QRect(560, 20, 100, 25))
        self.pushButtonRestore.setObjectName("pushButtonRestore")
        self.comboBoxA = QtWidgets.QComboBox(Dialog)
        self.comboBoxA.setGeometry(QtCore.QRect(140, 20, 400, 24))
        self.comboBoxA.setObjectName("comboBoxA")
        self.pushButtonDelete = QtWidgets.QPushButton(Dialog)
        self.pushButtonDelete.setGeometry(QtCore.QRect(660, 20, 100, 25))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonDisplay = QtWidgets.QPushButton(Dialog)
        self.pushButtonDisplay.setGeometry(QtCore.QRect(760, 20, 100, 25))
        self.pushButtonDisplay.setObjectName("pushButtonDisplay")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBoxA, self.pushButtonRestore)
        Dialog.setTabOrder(self.pushButtonRestore, self.tableWidgetL1)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelStaticLA.setText(_translate("Dialog", "Active Account:"))
        self.tableWidgetL1.setSortingEnabled(False)
        self.pushButtonRestore.setText(_translate("Dialog", "Restore"))
        self.pushButtonDelete.setText(_translate("Dialog", "Delete"))
        self.pushButtonDisplay.setText(_translate("Dialog", "Display Receipt"))


