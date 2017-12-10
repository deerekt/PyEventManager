from manager.decorator import *


@handle_event(any_event)
def method_1(event):
    pass


@handle_event(once, priority=Priority.HIGH, is_critical=True)
def method_2(event):
    pass


@handle_event(concrete_indexes(1, 3, 5), priority=Priority.LOW, is_critical=False)
def method_3(event):
    pass
