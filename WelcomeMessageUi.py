# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WelcomeMessageUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 401)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(380, 430))
        self.labelWelcome = QtWidgets.QLabel(Dialog)
        self.labelWelcome.setGeometry(QtCore.QRect(40, 10, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelWelcome.setFont(font)
        self.labelWelcome.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWelcome.setObjectName("labelWelcome")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 60, 340, 290))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.labelLogo = QtWidgets.QLabel(self.frame)
        self.labelLogo.setGeometry(QtCore.QRect(10, 190, 90, 90))
        self.labelLogo.setText("")
        self.labelLogo.setObjectName("labelLogo")
        self.labelMessage = QtWidgets.QLabel(self.frame)
        self.labelMessage.setGeometry(QtCore.QRect(10, 10, 321, 220))
        self.labelMessage.setText("")
        self.labelMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName("labelMessage")
        self.labelSigniture = QtWidgets.QLabel(self.frame)
        self.labelSigniture.setGeometry(QtCore.QRect(100, 190, 231, 90))
        self.labelSigniture.setText("")
        self.labelSigniture.setObjectName("labelSigniture")
        self.labelReminder = QtWidgets.QLabel(self.frame)
        self.labelReminder.setGeometry(QtCore.QRect(10, 230, 321, 50))
        self.labelReminder.setText("")
        self.labelReminder.setObjectName("labelReminder")
        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setGeometry(QtCore.QRect(260, 355, 100, 30))
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.pushButtonNext = QtWidgets.QPushButton(Dialog)
        self.pushButtonNext.setGeometry(QtCore.QRect(160, 355, 100, 30))
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.frame.raise_()
        self.labelWelcome.raise_()
        self.pushButtonClose.raise_()
        self.pushButtonNext.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Welcome  Message"))
        self.labelWelcome.setText(_translate("Dialog", "Welcome New User"))
        self.pushButtonClose.setText(_translate("Dialog", "Close"))
        self.pushButtonNext.setText(_translate("Dialog", "Next"))


