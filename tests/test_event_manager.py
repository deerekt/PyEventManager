import unittest

from mock import *

from manager.decorator import *
from manager.event_manager import EventManager
from tests.handlers import *
from tests.utils import count


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()

    def test_em_register_handler(self):
        test_handler = count(print_10nd_event)
        self._register_decorated_func(self.event_manager, test_handler)

        for i in xrange(4):
            self.event_manager.notify(object)
        self.assertEqual(test_handler.counter, 0)

        for i in xrange(8):
            self.event_manager.notify(object)
        self.assertEqual(test_handler.counter, 1)

    def test_em_unregister_existing_handler(self):
        test_handler = count(print_10nd_event)
        self._register_decorated_func(self.event_manager, test_handler)
        for i in xrange(4):
            self.event_manager.notify(object)

        self.event_manager.unregister_handler(test_handler)
        for i in xrange(8):
            self.event_manager.notify(object)

        self.assertEqual(test_handler.counter, 0)

    def test_em_unregister_not_existing_handler(self):
        def test_handler():
            pass
        self.event_manager.unregister_handler(test_handler)

    def test_em_unregister_and_register(self):
        test_handler = count(print_10nd_event)
        self._register_decorated_func(self.event_manager, test_handler)
        for i in xrange(4):
            self.event_manager.notify(object)

        self.event_manager.unregister_handler(test_handler)
        self._register_decorated_func(self.event_manager, test_handler)

        for i in xrange(8):
            self.event_manager.notify(object)

        self.assertEqual(test_handler.counter, 1)

    def test_em_delayed_once_register(self):
        mock = Mock()
        mock.test_handler_mock = Mock()

        for i in xrange(4):
            self.event_manager.notify(object)

        self.event_manager.register_handler(mock.test_handler_mock,
                                            TriggerInfo(once(), Priority.STANDARD, False, True))

        for i in xrange(4):
            self.event_manager.notify(object)

        expected_result = [call.test_handler_mock(IndexedEvent(object, 4))]

        self.assertEqual(mock.mock_calls, expected_result)

    def test_em_register_priority_handlers(self):
        mock = Mock()
        mock.low = Mock()
        mock.standard = Mock()
        mock.high = Mock()

        self.event_manager.register_handler(mock.standard,
                                            TriggerInfo(once(), Priority.STANDARD, False))
        self.event_manager.register_handler(mock.low,
                                            TriggerInfo(once(), Priority.LOW, False))
        self.event_manager.register_handler(mock.high,
                                            TriggerInfo(once(), Priority.HIGH, False))

        self.event_manager.notify(object)

        event = IndexedEvent(object, 0)
        expected_result = [call.high(event), call.standard(event), call.low(event)]
        self.assertEqual(mock.mock_calls, expected_result)

    def test_em_register_repeat_handlers(self):
        mock = Mock()
        mock.repeat_handler_mock = Mock()

        self.event_manager.register_handler(mock.repeat_handler_mock,
                                            TriggerInfo(repeat_index(3)(), Priority.STANDARD, False))

        for i in xrange(9):
            self.event_manager.notify(object)

        expected_result = []
        for i in xrange(2, 9, 3):
            event = IndexedEvent(object, i)
            expected_result.append(call.repeat_handler_mock(event))

        self.assertEqual(mock.mock_calls, expected_result)

    def test_em_register_repeat_with_max_retry_count_handlers(self):
        mock = Mock()
        mock.repeat_handler_mock = Mock()

        self.event_manager.register_handler(mock.repeat_handler_mock,
                                            TriggerInfo(repeat_index(3, repeat_count=3)(), Priority.STANDARD, False))

        for i in xrange(100):
            self.event_manager.notify(object)

        expected_result = []
        for i in xrange(2, 9, 3):
            event = IndexedEvent(object, i)
            expected_result.append(call.repeat_handler_mock(event))

        self.assertEqual(mock.mock_calls, expected_result)

    def test_em_register_non_critical_handler(self):
        self._register_decorated_func(self.event_manager, swallow_exception_on_1st_event)
        self.event_manager.notify(object)

    def test_em_register_critical_handler(self):
        self._register_decorated_func(self.event_manager, throw_exception_on_4th)

        def trigger_exception_routine():
            for i in xrange(10):
                self.event_manager.notify(object)

        self.assertRaises(Exception, trigger_exception_routine)

    def _register_decorated_func(self, event_manager, func):
        event_manager.register_handler(func,
                                       EventHandlerDecorator.extract_trigger_info_from_function(func))


if __name__ == "__main__":
    unittest.main()
