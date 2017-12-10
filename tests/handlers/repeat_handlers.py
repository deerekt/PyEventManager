from manager.decorator import *


@handle_event(repeat_index(2))
def print_every_2nd_event(event):
    print "Repeat: 2nd event was occur"


@handle_event(repeat_index(3))
def print_every_3rd_event(event):
    print "Repeat: 3rd event was occur"


@handle_event(repeat_index(5))
def print_every_5th_event(event):
    print "Repeat: 5th event was occur"
