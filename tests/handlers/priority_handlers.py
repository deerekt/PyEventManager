from manager.decorator import *


@handle_event(any_event, priority=Priority.LOW)
def print_event_with_low_priority(event):
    print "LOW PRIORITY"


@handle_event(any_event, priority=Priority.HIGH)
def print_event_with_high_priority(event):
    print "HIGH PRIORITY"


@handle_event(any_event, priority=Priority.STANDARD)
def print_event_with_standard_priority(event):
    print "STANDARD PRIORITY"
