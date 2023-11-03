from PySide2 import QtWidgets
from . import baseWidget


class IntField(baseWidget.BaseWidget):
    def __init__(self, value=0, minValue=-1000000, maxValue=100000, step=1, parent=None):
        self.__value = value
        self.__minValue = minValue
        self.__maxValue = maxValue
        self.__step = step

        super(IntField, self).__init__(parent)

    def _createWidgets(self):
        self.__lineEdit = QtWidgets.QLineEdit(str(self.__value))

    def _layoutWidgets(self):
        self._mainLayout = QtWidgets.QGridLayout(self)
        self._mainLayout.addWidget(self.__lineEdit, 0, 1)

    def _connectWidgets(self):
        self.__lineEdit.editingFinished.connect(self.__setValue)

    def __setValue(self):
        try:
            self.value = int(float(self.__lineEdit.text()))
        except ValueError as e:
            self.value = 0

    @property
    def value(self):
        self.value = int(self.__lineEdit.text())
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = max(min(val, self.__maxValue), self.__minValue)
        self.__lineEdit.setText(str(self.__value))

    @property
    def minValue(self):
        return self.__minValue

    @minValue.setter
    def minValue(self, val):
        self.__minValue = val

    @property
    def maxValue(self):
        return self.__maxValue

    @maxValue.setter
    def maxValue(self, val):
        self.__maxValue = val

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, val):
        self.__step = val

    def setChangedCommand(self, function):
        self.__lineEdit.textChanged.connect(function)

    def setEnterCommand(self, function):
        self.__lineEdit.editingFinished.connect(function)
