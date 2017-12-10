import functools


### Decorators ###

def from_current_index(func):
    """
    Indicates that decorated index generator function would like
    to add current EventManager index to generated indexes.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.from_current_index = True
    return wrapper

### Index Generators Functions ###


@from_current_index
def once():
    yield 0


@from_current_index
def any_event():
    current_index = -1
    while True:
        current_index += 1
        yield current_index


def concrete_indexes(*indexes):
    def func():
        for ind in sorted(indexes):
            yield ind
    return func



def repeat_index(period, start_index=-1, repeat_count=None):
    _start_index = start_index
    @from_current_index
    def func():
        start_index = _start_index
        while (start_index < 0):
            start_index += period

        current_index = start_index
        if repeat_count is None:
            while True:
                yield current_index
                current_index += period
        else:
            stop_index = start_index + repeat_count * period
            for index in xrange(start_index, stop_index, period):
                yield index
    return func
