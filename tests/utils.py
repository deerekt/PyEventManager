import functools
import inspect
import os
from os import walk


def is_module_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def get_files_from_dir(path):
    try:
        for (dir_path, dir_name, file_names) in walk(path):
            for name in file_names:
                yield os.path.join(dir_path, name)
    finally:
        pass


def is_python_file(file_path):
    return file_path[-3:] == ".py"


def count(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func(*args, **kwargs)

    wrapper.counter = 0
    return wrapper