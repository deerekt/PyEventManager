from enum import IntEnum


class Priority(IntEnum):
    HIGH = 1
    STANDARD = 2
    LOW = 3


class TriggerInfo():
    def __init__(self, index_trigger_generator, priority, is_critical, from_current_index=False):
        self.index_trigger_generator = index_trigger_generator
        self.priority = priority
        self.is_critical = is_critical
        self.current_index = None
        self.from_current_index = from_current_index
        self.offset = 0

    def _offset_with_current_index(self, offset):
        if self.from_current_index:
            self.offset = offset

    def is_handler_critical(self):
        return self.is_critical

    def get_priority(self):
        return self.priority

    def get_current_index(self):
        if self.current_index is None:
            return self.get_next_trigger_index()
        else:
            return self.current_index

    def get_next_trigger_index(self):
        try:
            self.current_index = self.offset + next(self.index_trigger_generator)
        except StopIteration:
            self.current_index = None
        finally:
            return self.current_index

    def __str__(self):
        return "TriggerInfo(%s, %s)" % (self.priority, self.current_index)

    def __lt__(self, other):
        return self.priority < other.priority \
               or self.is_critical < other.is_critical \
               or self.index_trigger_generator.__name__ < other.index_trigger_generator.__name__

    def __eq__(self, other):
        """
        Note, that we comparing index_trigger_generator's using their names due to
        complexity of actually comparing two generators (especially if they are infinite)
        """
        return self.index_trigger_generator.__name__ == other.index_trigger_generator.__name__ \
               and self.priority == other.priority \
               and self.is_critical == other.is_critical


class IndexedEvent():
    def __init__(self, event, index=-1):
        self._event = event
        self._index = index

    def get_event(self):
        return self._event

    def get_index(self):
        return self._index

    def __eq__(self, other):
        return self._event == other._event and self._index == other._index
