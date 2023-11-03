from imp import reload

from . import set; reload(set)
from . import manager; reload(manager)

from .set import Set
from .manager import Manager
