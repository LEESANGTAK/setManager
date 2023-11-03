import pymel.core as pm

from ..api import Manager
from ..api import Set

from PySide2 import QtCore, QtGui, QtWidgets
from .customWidgets import decorators as deco
from .setGUI import SetGUI


@deco.mayaUI
# @deco.dockable('setMngWS', 'Set Manager')
class ManagerGUI(QtWidgets.QWidget):
    INVALID_OBJECT_SET_NAMES = ["defaultLightSet", "defaultObjectSet", "initialParticleSE", "initialShadingGroup"]

    def __init__(self, parent=None):
        super(ManagerGUI, self).__init__(parent)

        self.__manager = Manager()

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowIcon(QtGui.QIcon(":out_objectSet.png"))
        self.setWindowTitle("Set Manager")
        self.resize(640, 480)

        self.__createWidgets()
        self.__layoutWidgets()
        self.__connectWidgets()

    def __createWidgets(self):
        # Buttons
        self.__addButton = QtWidgets.QPushButton("Add")
        self.__addButton.setIcon(QtGui.QIcon(":createSelectionSet.png"))
        self.__addButton.setToolTip("Add existing object sets.")
        self.__newButton = QtWidgets.QPushButton("New")
        self.__newButton.setIcon(QtGui.QIcon(":out_objectSet.png"))
        self.__newButton.setToolTip("Create a new object set with selected objects.")
        self.__delButton = QtWidgets.QPushButton("Delete")
        self.__delButton.setIcon(QtGui.QIcon(":delete.png"))
        self.__delButton.setToolTip("Delete selected object sets.")

        # Tree Wdiget
        self.__treeWidget = QtWidgets.QTreeWidget()

        self.__treeWidget.setColumnCount(3)
        self.__treeWidget.setColumnWidth(0, 100)
        self.__treeWidget.setColumnWidth(1, 100)

        model = self.__treeWidget.model()
        model.setHeaderData(0, QtCore.Qt.Horizontal, QtGui.QIcon(":visible.png"), QtCore.Qt.DecorationRole)
        model.setHeaderData(1, QtCore.Qt.Horizontal, QtGui.QIcon(":UVEditorIsolate.png"), QtCore.Qt.DecorationRole)
        self.__treeWidget.setHeaderLabels(["", "", "Name"])
        self.__treeWidget.header().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.__treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.__treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def __layoutWidgets(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        # Layout for Buttons
        layoutBtns = QtWidgets.QHBoxLayout()
        layoutBtns.addWidget(self.__addButton)
        layoutBtns.addWidget(self.__newButton)
        layoutBtns.addWidget(self.__delButton)
        mainLayout.addLayout(layoutBtns)

        mainLayout.addWidget(self.__treeWidget)

    def __connectWidgets(self):
        self.__addButton.clicked.connect(self.__addExistingSet)
        self.__newButton.clicked.connect(lambda x: self.__createNewSet())
        self.__delButton.clicked.connect(self.__deleteSelectedSet)
        self.__treeWidget.itemSelectionChanged.connect(self.__selectChangedCallback)
        self.__treeWidget.customContextMenuRequested.connect(self.__showPopupMenu)

    def __showPopupMenu(self, pos):
        selItems = self.__treeWidget.selectedItems()

        if not selItems:
            return

        menu = QtWidgets.QMenu(self.__treeWidget)
        menu.setToolTipsVisible(True)
        if len(selItems) == 1:
            addAction = menu.addAction(QtGui.QIcon(":setEdAddCmd.png"), 'Add', self.__addSelectedElements)
            addAction.setToolTip('Add selected objects to the set.')
            removeAction = menu.addAction(QtGui.QIcon(":setEdRemoveCmd.png"), 'Remove', self.__removeSelectedElements)
            removeAction.setToolTip('Remove selected objects from the set.')
            resetAction = menu.addAction(QtGui.QIcon(":menuIconReset.png"), 'Reset', self.__resetSelectedElements)
            resetAction.setToolTip('Reset with selected objects.')
        else:
            unionAction = menu.addAction(QtGui.QIcon(":nurbsShellUnion.png"), 'Union', self.__unionSelectedSets)
            unionAction.setToolTip('Make a new union set with selected sets.')
            diffAction = menu.addAction(QtGui.QIcon(":nurbsShellSubtract.png"), 'Difference', self.__differenceSelectedSets)
            diffAction.setToolTip('Make a new diffrence set with selected sets.')
            interAction = menu.addAction(QtGui.QIcon(":nurbsShellIntersect.png"), 'Intersection', self.__intersectionSelectedSets)
            interAction.setToolTip('Make a new Intersect set with selected sets.')
            if len(selItems) > 2:
                diffAction.setVisible(False)

        menu.exec_(self.__treeWidget.mapToGlobal(pos))

    def __addSelectedElements(self):
        selItem = self.__treeWidget.selectedItems()[0]
        sels = pm.selected()
        selItem.set.add(sels)

    def __removeSelectedElements(self):
        selItem = self.__treeWidget.selectedItems()[0]
        sels = pm.selected()
        selItem.set.remove(sels)

    def __resetSelectedElements(self):
        selItem = self.__treeWidget.selectedItems()[0]
        sels = pm.selected()
        selItem.set.reset(sels)

    def __unionSelectedSets(self):
        selSets = [item.set for item in self.__treeWidget.selectedItems()]
        pm.select(selSets[0].union(selSets[1:]), r=True)
        setName = "union_" + "_".join([set.name for set in selSets])
        self.__createNewSet(setName)

    def __differenceSelectedSets(self):
        selSets = [item.set for item in self.__treeWidget.selectedItems()]
        pm.select(selSets[0].difference(selSets[1]), r=True)
        setName = "diff_" + "_".join([set.name for set in selSets])
        self.__createNewSet(setName)

    def __intersectionSelectedSets(self):
        selSets = [item.set for item in self.__treeWidget.selectedItems()]
        pm.select(selSets[0].intersection(selSets[1:]), r=True)
        setName = "inter_" + "_".join([set.name for set in selSets])
        self.__createNewSet(setName)

    def __addExistingSet(self):
        selObjSets = pm.selected(type="objectSet")

        if not selObjSets:
            selObjSets = pm.ls(type="objectSet")

        allSetNames = [set.name for set in self.__manager.sets]
        for objSet in selObjSets:
            if objSet.name() in ManagerGUI.INVALID_OBJECT_SET_NAMES or objSet.name() in allSetNames:
                continue
            set = self.__manager.addSet(objSet)
            SetGUI(set, self.__treeWidget)

    def __createNewSet(self, name="newSet"):
        set = self.__manager.createSet(name)
        SetGUI(set, self.__treeWidget)

    def __deleteSelectedSet(self):
        root = self.__treeWidget.invisibleRootItem()
        for item in self.__treeWidget.selectedItems():
            self.__manager.removeSet(item.set)
            root.removeChild(item)

    def closeEvent(self, event):
        self.__treeWidget.clear()
        event.accept()
        super(ManagerGUI, self).closeEvent(event)

    def __selectChangedCallback(self):
        selItems = self.__treeWidget.selectedItems()
        if not selItems:
            pm.select(clear=True)
        elif len(selItems) == 1:
            selItems[0].set.select()
        else:
            selSets = []
            for i in range(self.__treeWidget.topLevelItemCount()):
                item = self.__treeWidget.topLevelItem(i)
                if item.isSelected():
                    selSets.append(item.set)
            pm.select(cl=True)
            pm.select(selSets[0].union(selSets[1:]), r=True)
