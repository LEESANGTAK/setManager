import functools
from PySide2 import QtWidgets

from shiboken2 import wrapInstance
from shiboken2 import getCppPointer

import maya.OpenMayaUI as omui
import pymel.core as pm


def mayaUI(WidgetClass):
    """Set widget's parent to the maya main window."""
    origInit = WidgetClass.__init__
    def __init__(self):  # Wrapper method
        functools.update_wrapper(__init__, WidgetClass.__init__)  # Make wrapper method to like wrapped method

        mayaWinWidget = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)

        origInit(self, mayaWinWidget)  # Call warpped method
    WidgetClass.__init__ = __init__  # Replace wrapped method to wrapper method
    return WidgetClass


def dockable(wscName, label):
    """Convert QtWidget to dockable maya ui.

    :param wscName: Workspace control name
    :type wscName: str
    :param label: Tab label
    :type label: str
    """
    def decorator(WidgetClass):
        origShow = WidgetClass.show
        def show(self):  # Wrapper method
            functools.update_wrapper(show, WidgetClass.show)  # Make wrapper method to like wrapped method

            if pm.workspaceControl(wscName, q=True, exists=True):
                pm.deleteUI(wscName)
            pm.workspaceControl(wscName, label=label)
            omui.MQtUtil.addWidgetToMayaLayout(int(getCppPointer(self)[0]), int(omui.MQtUtil.findControl(wscName)))

            origShow(self)  # Call warpped method
        WidgetClass.show = show  # Replace wrapped method to wrapper method
        return WidgetClass
    return decorator
