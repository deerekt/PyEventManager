from manager.decorator import *


@handle_event(concrete_indexes(10))
def print_10nd_event(event):
    print "Concrete: This is 10 event!"


@handle_event(concrete_indexes(3, 7))
def print_3rd_and_7nd_event(event):
    print "Concrete: This is 3 or 7 event!"
