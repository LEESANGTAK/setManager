from maya import cmds
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
        self.__addButton.setIcon(QtGui.QIcon(":refresh.png"))
        self.__addButton.setToolTip("Add selected or existing object sets in the scene.")
        self.__removeButton = QtWidgets.QPushButton("Remove")
        self.__removeButton.setIcon(QtGui.QIcon(":out_objectSet.png"))
        self.__removeButton.setToolTip("Remove selected object sets in the list.")
        self.__newButton = QtWidgets.QPushButton("New")
        self.__newButton.setIcon(QtGui.QIcon(":out_objectSet.png"))
        self.__newButton.setToolTip("Create a new object set with selected objects.")
        self.__delButton = QtWidgets.QPushButton("Delete")
        self.__delButton.setIcon(QtGui.QIcon(":delete.png"))
        self.__delButton.setToolTip("Delete selected object sets in the list.")

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
        layoutBtns.addWidget(self.__removeButton)
        layoutBtns.addWidget(self.__newButton)
        layoutBtns.addWidget(self.__delButton)
        mainLayout.addLayout(layoutBtns)

        mainLayout.addWidget(self.__treeWidget)

    def __connectWidgets(self):
        self.__addButton.clicked.connect(self.__addExistingSet)
        self.__removeButton.clicked.connect(self.__removeSelectedSets)
        self.__newButton.clicked.connect(lambda x: self.__createNewSet())
        self.__delButton.clicked.connect(self.__deleteSelectedSet)
        self.__treeWidget.itemDoubleClicked.connect(self.__renameSelectedSet)
        self.__treeWidget.itemSelectionChanged.connect(self.__selectionChangedCallback)
        self.__treeWidget.customContextMenuRequested.connect(self.__showPopupMenu)

    def __showPopupMenu(self, pos):
        selItems = self.__treeWidget.selectedItems()

        menu = QtWidgets.QMenu(self.__treeWidget)
        menu.setToolTipsVisible(True)
        if len(selItems) == 0:
            addExistingSetsAction = menu.addAction(QtGui.QIcon(":refresh.png"), 'Refresh', self.__addExistingSet)
            addExistingSetsAction.setToolTip('Add selected or existing object sets in the scene.')
        elif len(selItems) == 1:
            addAction = menu.addAction(QtGui.QIcon(":setEdAddCmd.png"), 'Add', self.__addSelectedElements)
            addAction.setToolTip('Add selected objects to the set.')
            removeAction = menu.addAction(QtGui.QIcon(":setEdRemoveCmd.png"), 'Remove', self.__removeSelectedElements)
            removeAction.setToolTip('Remove selected objects from the set.')
            clearAction = menu.addAction(QtGui.QIcon(":clearCanvas.png"), 'Clear', self.__clearSelectedSet)
            clearAction.setToolTip('Remove all items in the set.')
            selectAction = menu.addAction(QtGui.QIcon(":aselect.png"), 'Select', self.__selectMembers)
            selectAction.setToolTip('Select members in a selected set.')
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

    def __clearSelectedSet(self):
        selItem = self.__treeWidget.selectedItems()[0]
        selItem.set.clear()

    def __selectMembers(self):
        selItem = self.__treeWidget.selectedItems()[0]
        selItem.set.select()

    def __selectionChangedCallback(self):
        for i in range(self.__treeWidget.topLevelItemCount()):
            item = self.__treeWidget.topLevelItem(i)
            if not item.isSelected() and item.isEditingName:
                item.exitEditNameMode()

    def __renameSelectedSet(self):
        selItems = self.__treeWidget.selectedItems()
        if len(selItems) == 1:
            selItems[0].enterEditNameMode()

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
        selObjSets = cmds.ls(sl=True, type="objectSet")
        if not selObjSets:
            selObjSets = [node for node in cmds.ls(type="objectSet") if cmds.nodeType(node) == "objectSet"]

        # Remove deformer sets in the list
        deformerSets = []
        for objSet in selObjSets:
            inputs = cmds.listConnections("{}.usedBy".format(objSet), d=False)
            if inputs:
                deformerSets.append(objSet)
        selObjSets = list(set(selObjSets) - set(deformerSets))
        # Remove default sets in the list
        selObjSets = [item for item in selObjSets if not "default" in item]

        existingSetNames = [setInst.name for setInst in self.__manager.sets]
        for objSet in selObjSets:
            objSet = pm.PyNode(objSet)
            if objSet.name() in ManagerGUI.INVALID_OBJECT_SET_NAMES or objSet.name() in existingSetNames:
                continue
            setInst = self.__manager.addSet(objSet)
            SetGUI(setInst, self.__treeWidget)

    def __removeSelectedSets(self):
        root = self.__treeWidget.invisibleRootItem()
        for item in self.__treeWidget.selectedItems():
            self.__manager.removeSet(item.set)
            root.removeChild(item)

    def __createNewSet(self, name="newSet"):
        set = self.__manager.createSet(name)
        SetGUI(set, self.__treeWidget)

    def __deleteSelectedSet(self):
        root = self.__treeWidget.invisibleRootItem()
        for item in self.__treeWidget.selectedItems():
            self.__manager.deleteSet(item.set)
            root.removeChild(item)

    def closeEvent(self, event):
        self.__treeWidget.clear()
        event.accept()
        super(ManagerGUI, self).closeEvent(event)
