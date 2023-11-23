import pymel.core as pm


class SelectMode:
    REPLACE = 0
    ADD = 1


class Set(object):
    SELECT_MODE = SelectMode()

    def __init__(self, name='newSet', objectSet=None):
        if objectSet:
            self.__objectSet = pm.PyNode(objectSet)
        else:
            self.__objectSet = pm.sets(n=name, empty=True)
            sels = pm.selected()
            if sels:
                self.add(sels)

    @property
    def name(self):
        return self.__objectSet.name()

    @name.setter
    def name(self, newName):
        print("rename {} to {}".format(self.name, newName))
        self.__objectSet.rename(newName)

    def add(self, elements):
        pm.sets(self.__objectSet, e=True, forceElement=elements)

    def remove(self, elements):
        pm.sets(self.__objectSet, e=True, remove=elements)

    def clear(self):
        pm.sets(self.__objectSet, e=True, clear=True)

    def reset(self, elements):
        self.clear()
        self.add(elements)

    def select(self, mode=SELECT_MODE.REPLACE):
        if mode == SelectMode.REPLACE:
            pm.select(self.__objectSet, r=True)
        elif mode == SelectMode.ADD:
            pm.select(self.__objectSet, add=True)

    def deselect(self):
        pm.select(self.__objectSet.members(), deselect=True)

    def hide(self):
        pm.select(self.__objectSet, r=True)
        pm.mel.HideSelectedObjects()
        pm.select(cl=True)

    def show(self):
        self.select()
        pm.mel.ShowSelectedObjects()
        pm.select(cl=True)

    def isolate(self):
        self.select()
        curPanel = pm.getPanel(withFocus=True)
        pm.isolateSelect(curPanel, state=True)
        pm.mel.eval('enableIsolateSelect {} {}'.format(curPanel, 1))
        pm.select(cl=True)

    def unisolate(self):
        curPanel = pm.getPanel(withFocus=True)
        pm.isolateSelect(curPanel, state=False)
        pm.mel.eval('enableIsolateSelect {} {}'.format(curPanel, 0))

    def union(self, otherSets):
        return pm.sets(self.name, union=[otherSet.name for otherSet in otherSets])

    def difference(self, otherSet):
        return pm.sets(self.name, subtract=otherSet.name)

    def intersection(self, otherSets):
        return pm.sets(self.name, intersection=[otherSet.name for otherSet in otherSets])
