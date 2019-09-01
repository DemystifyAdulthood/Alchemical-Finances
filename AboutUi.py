# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1210, 801)
        self.FrameLogo = QtWidgets.QFrame(Dialog)
        self.FrameLogo.setGeometry(QtCore.QRect(175, 200, 400, 400))
        self.FrameLogo.setFrameShape(QtWidgets.QFrame.Panel)
        self.FrameLogo.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.FrameLogo.setLineWidth(2)
        self.FrameLogo.setObjectName("FrameLogo")
        self.labelLogo = QtWidgets.QLabel(self.FrameLogo)
        self.labelLogo.setGeometry(QtCore.QRect(10, 10, 381, 381))
        self.labelLogo.setObjectName("labelLogo")
        self.FrameProgram = QtWidgets.QFrame(Dialog)
        self.FrameProgram.setGeometry(QtCore.QRect(625, 200, 400, 400))
        self.FrameProgram.setFrameShape(QtWidgets.QFrame.Panel)
        self.FrameProgram.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.FrameProgram.setLineWidth(2)
        self.FrameProgram.setObjectName("FrameProgram")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.FrameProgram)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 381))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelVersion = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelVersion.setFont(font)
        self.labelVersion.setObjectName("labelVersion")
        self.verticalLayout.addWidget(self.labelVersion)
        self.labelDeveloper = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelDeveloper.setFont(font)
        self.labelDeveloper.setObjectName("labelDeveloper")
        self.verticalLayout.addWidget(self.labelDeveloper)
        self.labelReleaseDate = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelReleaseDate.setFont(font)
        self.labelReleaseDate.setObjectName("labelReleaseDate")
        self.verticalLayout.addWidget(self.labelReleaseDate)
        self.labelSupport = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelSupport.setFont(font)
        self.labelSupport.setObjectName("labelSupport")
        self.verticalLayout.addWidget(self.labelSupport)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelDescription = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelDescription.setFont(font)
        self.labelDescription.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelDescription.setLineWidth(1)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout.addWidget(self.labelDescription)
        self.labelProgram = QtWidgets.QLabel(Dialog)
        self.labelProgram.setGeometry(QtCore.QRect(180, 50, 841, 70))
        self.labelProgram.setObjectName("labelProgram")
        self.labelTagLine = QtWidgets.QLabel(Dialog)
        self.labelTagLine.setGeometry(QtCore.QRect(180, 120, 841, 50))
        self.labelTagLine.setObjectName("labelTagLine")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.labelLogo.setText(_translate("Dialog", "TextLabel"))
        self.labelVersion.setText(_translate("Dialog", "Version: Beta 1.0"))
        self.labelDeveloper.setText(_translate("Dialog", "Developed By: Beaker Labs llc. [Coming Soon]"))
        self.labelReleaseDate.setText(_translate("Dialog", "Release Date: June 24th 2019"))
        self.labelSupport.setText(_translate("Dialog", "Support: Contact@demystifyAdulthood.com"))
        self.labelDescription.setText(_translate("Dialog", "Background Information:"))
        self.labelProgram.setText(_translate("Dialog", "TextLabel"))
        self.labelTagLine.setText(_translate("Dialog", "TextLabel"))


