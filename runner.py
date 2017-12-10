import importlib
from manager.event_manager import *
from manager.utils import *

if __name__ == "__main__":
    mod = get_module_by_name("tests.handlers")
    manager = EventManager(debug=True)
    manager.bind_handlers_from_module(mod)

    for i in xrange(20):
        manager.notify(object)
