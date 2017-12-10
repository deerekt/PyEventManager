from manager.decorator import *


@handle_event(repeat_index(2, repeat_count=5))
def print_every_2nd_event_only_5_times(event):
    print "Special(repeat_count=5): 2nd event was occur"


@handle_event(repeat_index(3, repeat_count=3))
def print_every_3rd_event_3_times(event):
    print "Special(repeat_count=3): 3rd event was occur"


@handle_event(repeat_index(5, repeat_count=2))
def print_every_5th_event_2_times(event):
    print "Special(repeat_count=2): 5th event was occur"
