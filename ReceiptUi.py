# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReceiptUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 700)
        Dialog.setMinimumSize(QtCore.QSize(600, 700))
        Dialog.setMaximumSize(QtCore.QSize(600, 700))
        Dialog.setModal(True)
        self.labelPicture = QtWidgets.QLabel(Dialog)
        self.labelPicture.setGeometry(QtCore.QRect(50, 50, 500, 600))
        self.labelPicture.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPicture.setObjectName("labelPicture")
        self.pushButtonRotate = QtWidgets.QPushButton(Dialog)
        self.pushButtonRotate.setGeometry(QtCore.QRect(250, 660, 100, 25))
        self.pushButtonRotate.setObjectName("pushButtonRotate")
        self.labelFileName = QtWidgets.QLabel(Dialog)
        self.labelFileName.setGeometry(QtCore.QRect(50, 20, 500, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFileName.sizePolicy().hasHeightForWidth())
        self.labelFileName.setSizePolicy(sizePolicy)
        self.labelFileName.setObjectName("labelFileName")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Receipt"))
        self.labelPicture.setText(_translate("Dialog", "TextLabel"))
        self.pushButtonRotate.setText(_translate("Dialog", "Rotate"))
        self.labelFileName.setText(_translate("Dialog", "TextLabel"))


