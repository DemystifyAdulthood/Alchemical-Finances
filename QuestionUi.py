# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QuestionUi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Question(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(278, 97)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonAdd = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout.addWidget(self.pushButtonAdd, 1, 0, 1, 1)
        self.pushButtonRemove = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.gridLayout.addWidget(self.pushButtonRemove, 1, 1, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout.addWidget(self.pushButtonCancel, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Account Type Modifier"))
        self.pushButtonAdd.setText(_translate("Dialog", "Add"))
        self.pushButtonRemove.setText(_translate("Dialog", "Remove"))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "Would You like to Add or Remove an Account Type?"))

