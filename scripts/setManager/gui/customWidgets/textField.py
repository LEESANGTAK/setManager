from PySide2 import QtWidgets
from . import baseWidget


class TextField(baseWidget.BaseWidget):
    def __init__(self, text='', parent=None):
        super(TextField, self).__init__(parent)

        self.__lineEdit.setText(text)

    def _createWidgets(self):
        self.__lineEdit = QtWidgets.QLineEdit()

    def _layoutWidgets(self):
        self._mainLayout = QtWidgets.QGridLayout(self)
        self._mainLayout.addWidget(self.__lineEdit, 0, 1)

    def _connectWidgets(self):
        self.__lineEdit.editingFinished.connect(self.__setText)

    def __setText(self):
        self.text = self.__lineEdit.text()

    @property
    def text(self):
        return self.__lineEdit.text()

    @text.setter
    def text(self, text):
        self.__lineEdit.setText(text)

    @property
    def placeHolderText(self):
        return self.__lineEdit.placeholderText()

    @placeHolderText.setter
    def placeHolderText(self, text):
        self.__lineEdit.setPlaceholderText(text)

    def setChangedCommand(self, function):
        self.__lineEdit.textChanged.connect(function)

    def setEnterCommand(self, function):
        self.__lineEdit.editingFinished.connect(function)
