from PySide2 import QtWidgets, QtGui
from . import baseWidget


class FloatField(baseWidget.BaseWidget):
    def __init__(self, value=0.0, minValue=-1000000.0, maxValue=100000.0, step=1.0, parent=None):
        self.__value = value
        self.__minValue = minValue
        self.__maxValue = maxValue
        self.__step = step

        super(FloatField, self).__init__(parent)

    def _createWidgets(self):
        self.__lineEdit = QtWidgets.QLineEdit()
        self.__lineEdit.setValidator(QtGui.QDoubleValidator())

    def _layoutWidgets(self):
        self._mainLayout = QtWidgets.QGridLayout(self)
        self._mainLayout.addWidget(self.__lineEdit, 0, 1)

    def _connectWidgets(self):
        self.__lineEdit.editingFinished.connect(self.__setValue)

    def __setValue(self):
        try:
            self.value = float(self.__lineEdit.text())
        except ValueError as e:
            self.value = 0.0

    @property
    def value(self):
        self.value = float(self.__lineEdit.text())
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
