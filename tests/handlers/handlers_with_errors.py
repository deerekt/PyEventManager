from manager.decorator import *


@handle_event(concrete_indexes(4), is_critical=True)
def throw_exception_on_4th(event):
    raise Exception("Exception on 10th!")


@handle_event(once, is_critical=False)
def swallow_exception_on_1st_event(event):
    raise Exception("Exception should be swallowed!")
