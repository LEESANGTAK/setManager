from PySide2 import QtWidgets
from .customWidgets.iconButton import IconButton


class SetGUI(QtWidgets.QTreeWidgetItem):
    def __init__(self, set, parent=None):
        super(SetGUI, self).__init__(parent)

        self.__set = set

        self._createWidgets()
        self._layoutWidgets()
        self._connectWidgets()

    @property
    def set(self):
        return self.__set

    def _createWidgets(self):
        self.__eyeIcon = IconButton(":visible.png", checkable=True)
        self.__eyeIcon.setChecked(True)
        self.__eyeIcon.setToolTip("Hide/Show set members.")
        self.__isoIcon = IconButton(":UVEditorIsolate.png", checkable=True)
        self.__isoIcon.setToolTip("Isolate set members.")
        self.__nameLabel = QtWidgets.QLabel(self.__set.name)

    def _layoutWidgets(self):
        treeWidget = self.treeWidget()
        treeWidget.setItemWidget(self, 0, self.__eyeIcon)
        treeWidget.setItemWidget(self, 1, self.__isoIcon)
        treeWidget.setItemWidget(self, 2, self.__nameLabel)

    def _connectWidgets(self):
        self.__eyeIcon.toggled.connect(self.__eyeToggledCallback)
        self.__isoIcon.toggled.connect(self.__isoToggledCallback)

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
