from imp import reload

from . import customWidgets; reload(customWidgets)
from . import setGUI; reload(setGUI)
from . import managerGUI; reload(managerGUI)

from .setGUI import SetGUI
from .managerGUI import ManagerGUI
