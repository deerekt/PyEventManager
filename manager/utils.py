import inspect
import os
import types
import importlib
from heapq import heappush, heappop
from itertools import count


def __is_iterable(obj):
    """
    _is_iterable checks if given obj is iterable.
    """
    try:
        iterator = iter(obj)
    except TypeError:
        return False
    else:
        return True


def flatten(nested_iterable):
    stack = [iter(nested_iterable)]
    while len(stack) > 0:
        try:
            element = stack[-1].next()
            if __is_iterable(element) and not isinstance(element, str):
                stack.append(iter(element))
            else:
                yield element
        except StopIteration:
            stack.pop()


def get_current_module_dir_path():
    frame = inspect.stack()[1]
    caller_module = inspect.getmodule(frame[0])
    return os.path.dirname(os.path.abspath(caller_module.__file__))

def get_module_by_name(module_name):
    mod = importlib.import_module(module_name)
    return mod

class PriorityQueue:
    __removed_entry = '<removed-entry>'  # placeholder for a removed task

    def __init__(self, given_items=(), max_heap=False):
        self.max_heap = max_heap
        self.items = []
        self.item_finder = {}  # mapping of tasks to entries
        self.counter = count()  # unique sequence count
        for item in given_items:
            self.add(item)

    def _tune_priority(self, priority):
        if self.max_heap:
            return -1 * priority
        else:
            return priority

    def add(self, item, priority):
        """
        Add a new item  or update the priority of an existing one.
        """
        if item in self.item_finder:
            self.remove(item)
        priority = self._tune_priority(priority)
        count = next(self.counter)
        entry = [priority, count, item]
        self.item_finder[item] = entry
        heappush(self.items, entry)

    def remove(self, item):
        """
        Mark an existing item as removed.
        """
        entry = self.item_finder.pop(item)
        if entry:
            entry[-1] = PriorityQueue.__removed_entry

    def pop(self):
        """
        Remove and return item on top of priority heap.
        """
        while self.items:
            priority, count, item = heappop(self.items)
            if item is not PriorityQueue.__removed_entry:
                del self.item_finder[item]
                return item
        return None


def is_python_file(file_path):
    return file_path[-3:] == ".py"


def is_generator_function(func):
    return isinstance(func, types.FunctionType) and isinstance(func(), types.GeneratorType)
