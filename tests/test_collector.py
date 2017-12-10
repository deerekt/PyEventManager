import imp
import unittest

import tests.test_package
import tests.test_package.inner_package.handlers
from manager.collector import Collector
from manager.decorator import EventHandlerDecorator
from tests import handlers
from tests.utils import *


class TestCollector(unittest.TestCase):
    def setUp(self):
        self.collector = Collector()

    def test_collector_parse_package_with_all_functions_being_handlers(self):
        package_path = handlers.__path__[0]

        python_files = filter(is_python_file, get_files_from_dir(package_path))
        amod = None
        for i in python_files:
            amod = imp.load_source("test", i)
        pckg_functions = inspect.getmembers(amod, lambda func: is_module_function(amod, func))
        pckg_functions_names = map(lambda x: x[0], pckg_functions)

        handlers_info = self.collector.scan_folders_for_handlers(package_path)
        handlers_names = map(lambda x: x[0].__name__, handlers_info)

        self.assertListEqual(sorted(pckg_functions_names), sorted(handlers_names))

    def test_collector_parse_package_with_not_all_functions_being_handlers(self):
        package_path = tests.test_package.__path__[0]
        handlers_info = self.collector.scan_folders_for_handlers(package_path)
        collector_results = map(lambda x: x[0].__name__, handlers_info)

        expected_results = ["method_1", "method_2", "method_3", "method_7", "method_9"]

        self.assertListEqual(sorted(collector_results), sorted(expected_results))

    def test_collector_parse_trigger_info_from_handler(self):
        handlers_info = self.collector.scan_module_for_handlers(tests.test_package.inner_package.handlers)
        collector_results = map(lambda x: x[1], handlers_info)
        handlers = [tests.test_package.inner_package.handlers.method_1,
                    tests.test_package.inner_package.handlers.method_2,
                    tests.test_package.inner_package.handlers.method_3]

        expected_results = map(EventHandlerDecorator.extract_trigger_info_from_function, handlers)

        self.assertListEqual(sorted(collector_results), sorted(expected_results))


if __name__ == "__main__":
    unittest.main()
