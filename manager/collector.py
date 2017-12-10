import imp
import inspect
import os
from os.path import join, isdir, dirname, abspath

from decorator import EventHandlerDecorator
from utils import flatten, is_python_file


class Collector():
    def scan_module_for_handlers(self, mod, only_packages=True):
        try:
            # If module is package
            nested_handlers = self._search_for_handlers(mod.__path__[-1], only_packages)
        except:
            # If module just a single .py file
            nested_handlers = self._retrieve_handlers_from_module(mod)
        return self._extract_handlers_with_info(nested_handlers)

    def scan_folders_for_handlers(self, path, only_packages=True):
        nested_handlers = self._search_for_handlers(path, only_packages)
        return self._extract_handlers_with_info(nested_handlers)

    def _search_for_handlers(self, path, only_packages):
        """
        Couldn't find a better way to import any python module,
        than use 'imp.load_source()' function. That's why there are
        almost no any relative imports in project.
        """
        files_list = []

        if is_python_file(path) and path[-11:] != "__init__.py":
            mod = imp.load_source(path, path)
            files_list.append(self._retrieve_handlers_from_module(mod))
        elif isdir(path):
            files_and_dirs = os.listdir(path)
            if only_packages and "__init__.py" not in files_and_dirs:
                return []
            if self._is_current_module(path):
                return []
            for name in files_and_dirs:
                files_list.append(self._search_for_handlers(join(path, name), only_packages))

        return files_list

    def _retrieve_handlers_from_module(self, mod):
        all_functions = [f for (_, f) in inspect.getmembers(mod, inspect.isfunction)]
        handlers = filter(lambda f: EventHandlerDecorator.is_decorates(f), all_functions)
        return handlers

    def _extract_handlers_with_info(self, tree_structure):
        collected_handlers = flatten(tree_structure)
        return [(f, EventHandlerDecorator.from_decorated_function(f).get_trigger_info()) \
                for f in collected_handlers]

    def _is_current_module(self, path):
        """
        Would like to ignore any file in Collector (EventManager) package.
        """
        return dirname(abspath(__file__)) == path
