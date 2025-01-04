from PySide2 import QtWidgets
from .customWidgets.iconButton import IconButton


class SetGUI(QtWidgets.QTreeWidgetItem):
    def __init__(self, set, parent=None):
        super(SetGUI, self).__init__(parent)

        self.__set = set
        self.__isEditingName = False

        self._createWidgets()
        self._layoutWidgets()
        self._connectWidgets()

    @property
    def set(self):
        return self.__set

    @property
    def isEditingName(self):
        return self.__isEditingName

    def _createWidgets(self):
        self.__eyeIcon = IconButton(":eye.png", checkable=True)
        self.__eyeIcon.setChecked(True)
        self.__eyeIcon.setToolTip("Hide/Show set members.")
        self.__isoIcon = IconButton(":UVEditorIsolate.png", checkable=True)
        self.__isoIcon.setToolTip("Isolate set members.")
        self.__nameLabel = QtWidgets.QLabel(self.__set.name)
        self.__nameLE = QtWidgets.QLineEdit()
        self.__nameStack = QtWidgets.QStackedWidget()
        self.__nameStack.addWidget(self.__nameLabel)
        self.__nameStack.addWidget(self.__nameLE)

    def _layoutWidgets(self):
        treeWidget = self.treeWidget()
        treeWidget.setItemWidget(self, 0, self.__eyeIcon)
        treeWidget.setItemWidget(self, 1, self.__isoIcon)
        treeWidget.setItemWidget(self, 2, self.__nameStack)

    def _connectWidgets(self):
        self.__eyeIcon.toggled.connect(self.__eyeToggledCallback)
        self.__isoIcon.toggled.connect(self.__isoToggledCallback)
        self.__nameLE.editingFinished.connect(self.exitEditNameMode)

    def __eyeToggledCallback(self):
        if self.__eyeIcon.isChecked():
            self.__set.show()
        else:
            self.__set.hide()

    def __isoToggledCallback(self):
        if self.__isoIcon.isChecked():
            self.__set.isolate()
        else:
            self.__set.unisolate()

    def enterEditNameMode(self):
        self.__nameLE.setText(self.__nameLabel.text())
        self.__nameLE.setFocus()
        self.__nameLE.selectAll()
        self.__nameStack.setCurrentIndex(1)
        self.__isEditingName = True

    def exitEditNameMode(self):
        self.__set.name = self.__nameLE.text()
        self.__nameLabel.setText(self.__set.name)
        self.__nameStack.setCurrentIndex(0)
        self.__isEditingName = False