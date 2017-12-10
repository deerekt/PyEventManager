from collections import defaultdict

from collector import Collector
from error_handling import handle_error_context
from models import IndexedEvent
from utils import PriorityQueue


class EventManager():
    def __init__(self, debug=False, collector=Collector()):
        self.debug = debug
        self.collector = collector
        self.counter = 0
        self.index_to_handlers = defaultdict(PriorityQueue)  # index -> list of function
        self.handler_to_trigger_info = {}  # function -> trigger_info

    def notify(self, event):
        indexedEvent = IndexedEvent(event, self.counter)
        self._process_event(indexedEvent)
        self.counter += 1

    def bind_handlers_from_module(self, mod):
        handlers_with_info = self.collector.scan_module_for_handlers(mod)
        for (handler, info) in handlers_with_info:
            self.register_handler(handler, info)

    def bind_handlers_from_path(self, path):
        handlers_with_info = self.collector.scan_folders_for_handlers(path)
        for (handler, info) in handlers_with_info:
            self.register_handler(handler, info)

    def register_handler(self, handler, trigger_info):
        trigger_info._offset_with_current_index(self.counter)
        if self.debug:
            print "Register handler: %s with info: %s" % (handler, trigger_info)
        self.handler_to_trigger_info[handler] = trigger_info
        index = trigger_info.get_next_trigger_index()
        while index < self.counter and index != None:
            index = trigger_info.get_next_trigger_index()
        self.index_to_handlers[index].add(handler, trigger_info.get_priority())

    def unregister_handler(self, handler):
        if self.debug:
            print "Unregister handler: %s" % handler
        if handler in self.handler_to_trigger_info:
            trigger_info = self.handler_to_trigger_info[handler]
            current_index = trigger_info.get_current_index()
            self.index_to_handlers[current_index].remove(handler)
            self.handler_to_trigger_info.pop(handler)

    def _process_event(self, indexedEvent):
        index = indexedEvent.get_index()
        if self.debug:
            print "Notify: %s" % index
        handler = self.index_to_handlers[index].pop()
        while handler:
            info = self.handler_to_trigger_info[handler]
            is_critical = info.is_handler_critical() if info is not None else False
            with handle_error_context(re_raise=is_critical, log_traceback=True):
                handler(indexedEvent)
            self._refresh_handler_for_index(index, handler)
            handler = self.index_to_handlers[index].pop()
        self.index_to_handlers.pop(index)

    def _refresh_handler_for_index(self, index, handler):
        trigger_info = self.handler_to_trigger_info[handler]
        next_index = trigger_info.get_next_trigger_index()
        if next_index is not None:
            self.index_to_handlers[next_index].add(handler, trigger_info.get_priority())
        if self.debug:
            print "Replace %s: %s -> %s" % (handler, index, next_index)
