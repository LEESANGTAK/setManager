import pymel.core as pm
from .set import Set


class Manager:
    def __init__(self):
        self.__sets = []
        pass

    @property
    def sets(self):
        return self.__sets

    def addSet(self, objectSet):
        set = Set(objectSet=objectSet)
        self.__sets.append(set)
        return set

    def createSet(self, name):
        set = Set(name=name)
        self.__sets.append(set)
        return set

    def removeSet(self, set):
        self.__sets.remove(set)
        del(set)
