import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap, QTransform
from ReceiptUi import Ui_Dialog
from StyleSheets import UniversalStyleSheet


class Receipt(QDialog):
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, pathway, image):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.degree = 0
        self.receiptImage = QPixmap(pathway)
        self.receiptAdjustment = self.receiptImage.transformed(QTransform().rotate(self.degree)).scaled(500, 600, 1, 1)
        self.ui.labelPicture.setPixmap(self.receiptAdjustment)
        self.ui.pushButtonRotate.clicked.connect(self.rotate_image)
        self.ui.labelFileName.setText(image)
        self.setStyleSheet(UniversalStyleSheet)
        self.show()

    def rotate_image(self):
        self.degree += 90
        modifiedImage = self.receiptImage.transformed(QTransform().rotate(self.degree)).scaled(500, 600, 1, 1)
        self.ui.labelPicture.setPixmap(modifiedImage)
        if self.degree > 270:
            self.degree = 0

    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = Receipt('IMG_1853.jpg')
    lily.show()
    sys.exit(app.exec_())