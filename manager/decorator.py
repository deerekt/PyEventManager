import functools

from index_generators import *
from models import *
from utils import is_generator_function


class EventHandlerDecorator(object):
    __unique_decorator_key = "is_event_handler"

    @staticmethod
    def is_decorates(f):
        return f.func_dict.has_key(EventHandlerDecorator.__unique_decorator_key)

    @staticmethod
    def from_decorated_function(f):
        return f.func_dict[EventHandlerDecorator.__unique_decorator_key]

    @staticmethod
    def extract_trigger_info_from_function(f):
        return f.func_dict[EventHandlerDecorator.__unique_decorator_key].get_trigger_info()

    def __init__(self, index_trigger_generator_func=any_event, priority=Priority.STANDARD,
                 is_critical=False):
        assert is_generator_function(index_trigger_generator_func), \
            "Param 'index_trigger_generator_func' should be function that return generator!"
        self.index_trigger_generator_func = index_trigger_generator_func
        self.priority = priority
        self.is_critical = is_critical  # If true, any Exception in handler will not be swallowed.
        # Otherwise, it will fall silently.

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        if wrapped.func_dict.has_key(EventHandlerDecorator.__unique_decorator_key):
            raise Exception("Function already decorated with EventHandlerDecorator!")
        else:
            wrapped.func_dict[EventHandlerDecorator.__unique_decorator_key] = self
        return wrapped

    def get_trigger_info(self):
        # Refactor!
        from_current_index = False
        try:
            from_current_index = self.index_trigger_generator_func.from_current_index
        except:
            pass
        return TriggerInfo(self.index_trigger_generator_func(), self.priority, self.is_critical, from_current_index)


handle_event = EventHandlerDecorator
